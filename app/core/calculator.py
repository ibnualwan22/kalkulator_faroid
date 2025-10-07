"""
Main Calculator untuk Perhitungan Warisan
Dengan dukungan kasus khusus: Akdariyyah, Jadd ma'al-Ikhwah, dll.

Updated: 2025-10-07
Fixed: Error 500, AshlCalculator call, Schema compatibility, Logging
"""
from __future__ import annotations
from typing import List, Dict, Optional
import logging
from datetime import datetime

from app.schemas.calculation import CalculationInput, CalculationResult, HeirShare
from app.schemas.heir import HeirResponse
from app.core.furudh_engine import FurudhEngine, FurudhResult
from app.core.ashl_calculator import AshlCalculator
from app.utils.constants import HeirID, HEIR_NAMES
from app.utils.math_helpers import fraction_to_string, distribute_shares
from app.utils.inkisar import check_and_apply_inkisar, compute_inkisar_single_group

# ✅ SETUP LOGGING
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('faraid_calculator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FaroidCalculator:
    """Main calculator untuk faraid"""
    
    def __init__(self, calculation_input: CalculationInput):
        self.input = calculation_input
        self.heirs = calculation_input.heirs
        self.tirkah = calculation_input.tirkah
        self.notes = []
        
        # ✅ Log input
        logger.info(f"=== NEW CALCULATION ===")
        logger.info(f"Tirkah: Rp {self.tirkah:,.0f}")
        logger.info(f"Heirs: {len(self.heirs)}")
        
    def calculate(self) -> CalculationResult:
        """
        Lakukan perhitungan lengkap
        
        Returns:
            CalculationResult
        """
        self.notes.append("=== MULAI PERHITUNGAN WARISAN ===")
        self.notes.append(f"Total Harta (Tirkah): Rp {self.tirkah:,.0f}")
        self.notes.append(f"Jumlah Ahli Waris: {len(self.heirs)}")
        self.notes.append("")
        
        # 1. Cek kasus khusus
        special_case = self._check_special_cases()
        
        if special_case:
            return self._calculate_special_case(special_case)
        
        # 2. Perhitungan normal
        return self._calculate_normal()
    
    def _check_special_cases(self) -> Optional[str]:
        """
        Cek apakah termasuk kasus khusus
        
        Returns:
            Nama kasus khusus atau None
        """
        from app.special_cases import (
            is_akdariyyah, is_jadd_ikhwah, is_musytarakah,
            is_gharrawin
        )
        
        if is_akdariyyah(self.heirs):
            return "akdariyyah"
        
        if is_jadd_ikhwah(self.heirs):
            return "jadd_ikhwah"
        
        if is_musytarakah(self.heirs):
            return "musytarakah"
        
        if is_gharrawin(self.heirs):
            return "gharrawin"
        
        return None
    
    def _calculate_normal(self) -> CalculationResult:
        """Perhitungan normal (tanpa kasus khusus)"""
        try:
            from app.utils.constants import HEIR_NAMES
            from app.utils.inkisar import check_and_apply_inkisar, compute_inkisar_single_group
            
            # ===== TRACKING INKISAR =====
            ashl_awal_original = None
            self._inkisar_history = []
            
            # ===== STEP 1: Tentukan Furudh =====
            logger.info("STEP 1: Tentukan Furudh")
            self.notes.append("📋 TAHAP 1: Menentukan Furudh Muqaddarah")
            
            from app.core.furudh_engine import FurudhEngine
            furudh_engine = FurudhEngine(self.heirs)
            furudh_results = furudh_engine.determine_furudh()
            
            logger.info(f"Furudh results: {len(furudh_results)} items")
            
            for furudh in furudh_results:
                heir_name = HEIR_NAMES.get(furudh.heir_id, {}).get("id", "Unknown")
                if furudh.is_ashobah:
                    self.notes.append(f"  • {heir_name}: Ashobah")
                else:
                    self.notes.append(f"  • {heir_name}: {furudh.fardh}")
            self.notes.append("")
            
            if not furudh_results:
                logger.error("Tidak ada ahli waris dengan furudh")
                self.notes.append("   ❌ Tidak ada ahli waris dengan furudh!")
                return self._create_error_result("Tidak ada ahli waris dengan furudh")
            
            # ===== STEP 2: Hitung Ashl =====
            logger.info("STEP 2: Hitung Ashl")
            self.notes.append("📊 TAHAP 2: Menghitung Ashl al-Mas'alah")

            # ✅ FIX: Gunakan static method dengan furudh_results
            ashl_awal, ashl_notes = AshlCalculator.calculate_ashl(furudh_results)
            ashl_awal_original = ashl_awal
            
            # Tambahkan notes dari AshlCalculator
            for note in ashl_notes:
                self.notes.append(f"   {note}")

            ashl = ashl_awal
            logger.info(f"Ashl awal: {ashl}")
            
            # ===== STEP 3: Hitung Saham Furudh =====
            logger.info("STEP 3: Hitung Saham Furudh")

            furudh_saham = []
            total_furudh_saham = 0

            for furudh in furudh_results:
                if not furudh.is_ashobah:
                    # ✅ FIX: Gunakan numerator/denominator, bukan fardh (string)
                    saham = (ashl * furudh.numerator) // furudh.denominator
                    furudh_saham.append((furudh, saham))
                    total_furudh_saham += saham
                    
                    logger.info(f"  {HEIR_NAMES.get(furudh.heir_id, {}).get('id', 'Unknown')}: "
                            f"{furudh.numerator}/{furudh.denominator} = {saham}/{ashl} saham")


            
            # ===== STEP 4: Cek Inkisar Furudh =====
            logger.info("STEP 4: Cek Inkisar Furudh")
            self.notes.append("")
            
            ashl_after_inkisar, furudh_saham, self.notes = check_and_apply_inkisar(
                furudh_saham, ashl, self.notes
            )
            
            if ashl_after_inkisar != ashl:
                self._inkisar_history.append(("Furudh", ashl, ashl_after_inkisar))
                ashl = ashl_after_inkisar
                total_furudh_saham = sum(saham for _, saham in furudh_saham)
            
            logger.info(f"Ashl after inkisar: {ashl_after_inkisar}")
            ashl_akhir = ashl_after_inkisar
            
            # ===== STEP 5: Cek Aul/Radd/Ashobah =====
            logger.info("STEP 5: Cek Aul/Radd/Ashobah")
            
            has_ashobah = any(f.is_ashobah for f in furudh_results)
            all_ashobah = all(f.is_ashobah for f in furudh_results)
            
            self.notes.append("")
            
            if all_ashobah:
                self.notes.append("✅ Semua ahli waris adalah Ashobah")
                sisa_saham = ashl_akhir
                distribution_type = "Ashobah"
            else:
                sisa_saham = ashl_akhir - total_furudh_saham
                logger.info(f"Sisa saham: {sisa_saham}")
                
                if sisa_saham == 0:
                    self.notes.append("✅ Pembagian PAS (Tidak ada sisa)")
                    distribution_type = "Adil"
                elif sisa_saham < 0:
                    ashl_akhir = total_furudh_saham
                    furudh_saham = [(f, saham) for f, saham in furudh_saham]
                    sisa_saham = 0
                    
                    logger.warning(f"AUL: {ashl_after_inkisar} → {ashl_akhir}")
                    
                    self.notes.append(f"⚠️ Terjadi AUL (عول)")
                    self.notes.append(f"   Ashl berubah dari {ashl_after_inkisar} menjadi {ashl_akhir}")
                    
                    # ✅ Validasi 'Aul (jika file aul_validator.py ada)
                    try:
                        from app.utils.aul_validator import validate_aul
                        is_valid, message = validate_aul(ashl_after_inkisar, ashl_akhir)
                        self.notes.append(f"   {message}")
                        if not is_valid:
                            logger.warning(f"Non-standard aul case")
                            self.notes.append(f"   ⚠️ PERINGATAN: Kasus 'aul ini tidak standar!")
                    except ImportError:
                        logger.warning("aul_validator.py not found, skipping validation")
                    
                    distribution_type = "Aul"
                elif has_ashobah:
                    self.notes.append("✅ Pembagian ADIL (Ada Ashobah)")
                    self.notes.append(f"   Sisa {sisa_saham} saham untuk Ashobah")
                    distribution_type = "Adil"
                else:
                    # ✅ RADD: Kembalikan sisa ke Dzawil Furudh
                    self.notes.append(f"✅ Terjadi RADD (رد)")
                    self.notes.append(f"   Sisa {sisa_saham} saham dari ashl {ashl_akhir}")
                    
                    logger.info(f"RADD DETECTED: {sisa_saham} saham sisa")
                    
                    # Cek apakah ada Zauj/Zaujah (ID 3 atau 4)
                    ZAUJ_ZAUJAH_IDS = {3, 4}  # Suami (3), Istri (4)
                    
                    zauj_zaujah_list = [(f, s) for f, s in furudh_saham if f.heir_id in ZAUJ_ZAUJAH_IDS]
                    dzawil_furudh_list = [(f, s) for f, s in furudh_saham if f.heir_id not in ZAUJ_ZAUJAH_IDS]
                    
                    has_zauj_zaujah = len(zauj_zaujah_list) > 0
                    
                    if not has_zauj_zaujah:
                        # ===== KASUS 1: RADD TANPA Zauj/Zaujah =====
                        self.notes.append(f"   📌 Kasus 1: Tidak ada Zauj/Zaujah")
                        total_furudh_saham = sum(saham for _, saham in furudh_saham)
                        ashl_akhir = total_furudh_saham
                        
                        self.notes.append(f"   Ashl Akhir = Total Saham = {ashl_akhir}")
                        logger.info(f"   RADD Kasus 1: ashl_akhir = {ashl_akhir}")
                    
                    elif len(dzawil_furudh_list) == 1:
                        # ===== KASUS 2: Ada Zauj/Zaujah + 1 Ahli Waris =====
                        self.notes.append(f"   📌 Kasus 2: Ada Zauj/Zaujah + 1 Ahli Waris")
                        
                        # Ambil penyebut zauj/zaujah
                        zauj_furudh, zauj_saham = zauj_zaujah_list[0]
                        zauj_denominator = zauj_furudh.denominator
                        
                        self.notes.append(f"   Penyebut Zauj/Zaujah ({zauj_denominator}) → Ashl Mas'alah")
                        
                        # Ashl baru = penyebut zauj
                        ashl_akhir = zauj_denominator
                        
                        # Hitung ulang saham dengan ashl baru
                        new_furudh_saham = []
                        for furudh, old_saham in furudh_saham:
                            # Saham baru = (numerator / denominator) * ashl_baru
                            new_saham = (furudh.numerator * ashl_akhir) / furudh.denominator
                            new_furudh_saham.append((furudh, new_saham))
                            
                            heir_name = HEIR_NAMES.get(furudh.heir_id, {}).get("id", "Unknown")
                            self.notes.append(f"   • {heir_name}: {furudh.numerator}/{furudh.denominator} × {ashl_akhir} = {new_saham}")
                        
                        furudh_saham = new_furudh_saham
                        
                        # Cek apakah masih ada sisa
                        total_saham_baru = sum(s for _, s in furudh_saham)
                        if total_saham_baru < ashl_akhir:
                            # Sisa untuk dzawil furudh (bukan zauj)
                            sisa_baru = ashl_akhir - total_saham_baru
                            self.notes.append(f"   Sisa {sisa_baru} untuk ahli waris (radd)")
                            
                            # Berikan sisa ke dzawil furudh
                            for i, (furudh, saham) in enumerate(furudh_saham):
                                if furudh.heir_id not in ZAUJ_ZAUJAH_IDS:
                                    new_saham = saham + sisa_baru
                                    furudh_saham[i] = (furudh, new_saham)
                                    
                                    heir_name = HEIR_NAMES.get(furudh.heir_id, {}).get("id", "Unknown")
                                    self.notes.append(f"   • {heir_name}: {saham} + {sisa_baru} (radd) = {new_saham}")
                        
                        logger.info(f"   RADD Kasus 2: ashl_akhir = {ashl_akhir}")
                    
                    else:
                        # ===== KASUS 3: Ada Zauj/Zaujah + Lebih dari 1 Ahli Waris =====
                        self.notes.append(f"   📌 Kasus 3: Ada Zauj/Zaujah + {len(dzawil_furudh_list)} Ahli Waris")
                        
                        # Ambil penyebut zauj/zaujah
                        zauj_furudh, zauj_saham = zauj_zaujah_list[0]
                        zauj_denominator = zauj_furudh.denominator
                        zauj_numerator = zauj_furudh.numerator
                        
                        self.notes.append(f"   Penyebut Zauj/Zaujah: {zauj_denominator}")
                        
                        # Kumpulkan penyebut dzawil furudh untuk cari LCM
                        dzawil_denominators = [f.denominator for f, _ in dzawil_furudh_list]
                        
                        from math import gcd
                        from functools import reduce
                        
                        def lcm(a, b):
                            return abs(a * b) // gcd(a, b)
                        
                        # Hitung LCM semua penyebut dzawil furudh
                        ashl_dzawil = reduce(lcm, dzawil_denominators)
                        
                        self.notes.append(f"   LCM penyebut Dzawil Furudh: {ashl_dzawil}")
                        
                        # Hitung saham dzawil furudh dari ashl_dzawil
                        dzawil_saham_map = {}
                        total_radd_saham = 0
                        
                        for furudh, _ in dzawil_furudh_list:
                            saham_radd = (furudh.numerator * ashl_dzawil) // furudh.denominator
                            dzawil_saham_map[furudh.heir_id] = saham_radd
                            total_radd_saham += saham_radd
                            
                            heir_name = HEIR_NAMES.get(furudh.heir_id, {}).get("id", "Unknown")
                            self.notes.append(f"   • {heir_name}: {furudh.numerator}/{furudh.denominator} × {ashl_dzawil} = {saham_radd}")
                        
                        self.notes.append(f"   Total Saham Radd: {total_radd_saham}")
                        
                        # Ashl akhir = total_radd_saham × zauj_denominator
                        ashl_akhir = total_radd_saham * zauj_denominator
                        
                        self.notes.append(f"   Ashl Akhir = {total_radd_saham} × {zauj_denominator} = {ashl_akhir}")
                        
                        # Hitung saham zauj dari ashl akhir
                        zauj_saham_final = (zauj_numerator * ashl_akhir) // zauj_denominator
                        
                        self.notes.append(f"   Zauj/Zaujah: {zauj_numerator}/{zauj_denominator} × {ashl_akhir} = {zauj_saham_final}")
                        
                        # Sisa untuk radd
                        sisa_untuk_radd = ashl_akhir - zauj_saham_final
                        
                        self.notes.append(f"   Sisa untuk Radd: {ashl_akhir} - {zauj_saham_final} = {sisa_untuk_radd}")
                        
                        # Distribusi sisa ke dzawil furudh proporsional
                        new_furudh_saham = []
                        
                        for furudh, old_saham in furudh_saham:
                            if furudh.heir_id in ZAUJ_ZAUJAH_IDS:
                                # Zauj/Zaujah
                                new_saham = zauj_saham_final
                            else:
                                # Dzawil Furudh: proporsional dari sisa
                                saham_radd = dzawil_saham_map[furudh.heir_id]
                                new_saham = (saham_radd / total_radd_saham) * sisa_untuk_radd
                            
                            new_furudh_saham.append((furudh, new_saham))
                            
                            heir_name = HEIR_NAMES.get(furudh.heir_id, {}).get("id", "Unknown")
                            self.notes.append(f"   • {heir_name}: {new_saham} saham (akhir)")
                        
                        furudh_saham = new_furudh_saham
                        
                        logger.info(f"   RADD Kasus 3: ashl_akhir = {ashl_akhir}")
                    
                    sisa_saham = 0
                    distribution_type = "Radd"



            
            # ===== STEP 6-8: Handling Ashobah =====
            if has_ashobah and sisa_saham > 0:
                logger.info("STEP 6-8: Handling Ashobah")
                
                ashobah_list = [f for f in furudh_results if f.is_ashobah]
                needs_inkisar_ashobah = False
                
                for ashobah in ashobah_list:
                    if ashobah.quantity > 1 and sisa_saham % ashobah.quantity != 0:
                        needs_inkisar_ashobah = True
                        break
                
                if needs_inkisar_ashobah and len(ashobah_list) == 1:
                    ashobah = ashobah_list[0]
                    heir_name = HEIR_NAMES.get(ashobah.heir_id, {}).get("id", "Unknown")
                    
                    self.notes.append("")
                    self.notes.append("🔹 INKISAR BERTINGKAT - Tahap 2 (Ashobah)")
                    
                    ashl_after_inkisar_ashobah, self.notes = compute_inkisar_single_group(
                        ruus=ashobah.quantity,
                        saham=int(sisa_saham),
                        ashl=ashl_akhir,
                        notes=self.notes
                    )
                    
                    if ashl_after_inkisar_ashobah != ashl_akhir:
                        self._inkisar_history.append(("Ashobah", ashl_akhir, ashl_after_inkisar_ashobah))
                        
                        multiplier = ashl_after_inkisar_ashobah // ashl_akhir
                        ashl_akhir = ashl_after_inkisar_ashobah
                        
                        furudh_saham = [(f, int(saham * multiplier)) for f, saham in furudh_saham]
                        sisa_saham = int(sisa_saham * multiplier)
                
                self.notes.append("")
                self.notes.append(f"💰 Sisa untuk Ashobah: {sisa_saham} saham")
                
                ashobah_results = self._distribute_ashobah(furudh_results, sisa_saham)
                
                for furudh_item, saham_ashobah in ashobah_results:
                    heir_name = HEIR_NAMES.get(furudh_item.heir_id, {}).get("id", "Unknown")
                    
                    if furudh_item.quantity > 1:
                        saham_per_orang = saham_ashobah / furudh_item.quantity
                        self.notes.append(f"📌 Distribusi Ashobah merata ({furudh_item.quantity} orang)")
                        self.notes.append(f"   • {heir_name}: {saham_ashobah:.2f} saham")
                        if saham_ashobah % furudh_item.quantity == 0:
                            self.notes.append(f"   • Per orang: {saham_ashobah} ÷ {furudh_item.quantity} = {saham_per_orang:.2f} saham/orang")
                    else:
                        self.notes.append(f"📌 Distribusi Ashobah")
                        self.notes.append(f"   • {heir_name}: {saham_ashobah:.2f} saham")
                
                if len(self._inkisar_history) > 0:
                    self.notes.append("")
                    self.notes.append("📋 RINGKASAN INKISAR:")
                    self.notes.append(f"   • Ashl Awal (sebelum inkisar): {ashl_awal_original}")
                    
                    for i, (tahap, ashl_before, ashl_after) in enumerate(self._inkisar_history, 1):
                        self.notes.append(f"   • Setelah Inkisar Tahap {i} ({tahap}): {ashl_before} → {ashl_after}")
                    
                    self.notes.append(f"   • Ashl Akhir: {ashl_akhir}")
                    total_multiplier = ashl_akhir // ashl_awal_original
                    self.notes.append(f"   • Total Multiplier: {total_multiplier}×")
                
                furudh_saham.extend(ashobah_results)
                self.notes.append("")
            
            # ===== STEP 9: Format hasil final =====
            logger.info("STEP 9: Format hasil final")
            
            # ✅ Buat HeirShare objects sesuai schema
            shares_result = []
            for furudh, saham in furudh_saham:
                heir_name = HEIR_NAMES.get(furudh.heir_id, {}).get("id", "Unknown")
                heir_name_ar = HEIR_NAMES.get(furudh.heir_id, {}).get("ar", "Unknown")
                
                # Buat HeirResponse
                heir_response = HeirResponse(
                    id=furudh.heir_id,
                    name_id=heir_name,
                    name_ar=heir_name_ar
                )
                
                # Calculate amounts
                total_amount = (self.tirkah * saham) / ashl_akhir
                percentage = f"{(saham / ashl_akhir) * 100:.2f}%"
                
                # ✅ Buat HeirShare
                heir_share = HeirShare(
                    heir=heir_response,
                    quantity=furudh.quantity,
                    fardh=str(furudh.fardh) if not furudh.is_ashobah else None,
                    share_fraction=f"{int(saham)}/{ashl_akhir}",
                    saham=float(saham),
                    reason=furudh.reason if hasattr(furudh, 'reason') else "Pembagian warisan",
                    share_amount=total_amount,
                    percentage=percentage,
                    is_mahjub=False,
                    mahjub_reason=None
                )
                
                shares_result.append(heir_share)
                
                # Log
                if furudh.quantity > 1:
                    individual_amount = total_amount / furudh.quantity
                    logger.info(f"{heir_name}: Rp {total_amount:,.0f} (@ Rp {individual_amount:,.0f}/orang)")
                else:
                    logger.info(f"{heir_name}: Rp {total_amount:,.0f}")
            
            # Distribusi Tirkah (Notes)
            self.notes.append("💵 TAHAP 4: Distribusi Tirkah")
            
            grouped_heirs = {}
            for share in shares_result:
                heir_id = share.heir.id
                if heir_id not in grouped_heirs:
                    grouped_heirs[heir_id] = {
                        "name": share.heir.name_id,
                        "total_amount": 0,
                        "total_percentage": 0,
                        "count": 0
                    }
                grouped_heirs[heir_id]["total_amount"] += share.share_amount
                grouped_heirs[heir_id]["total_percentage"] += float(share.percentage.rstrip('%'))
                grouped_heirs[heir_id]["count"] += share.quantity
            
            for heir_id, data in grouped_heirs.items():
                heir_name = data["name"]
                total_amount = data["total_amount"]
                total_percentage = data["total_percentage"]
                count = data["count"]
                
                if count > 1:
                    individual_amt = total_amount / count
                    self.notes.append(f"   • {heir_name}: Rp {total_amount:,.0f} ({total_percentage:.2f}%) → @ Rp {individual_amt:,.0f}/orang")
                else:
                    self.notes.append(f"   • {heir_name}: Rp {total_amount:,.0f} ({total_percentage:.2f}%)")
            
            logger.info("Calculation completed successfully")
            
            # ✅ RETURN SESUAI SCHEMA
            total_furudh_saham_final = sum(saham for _, saham in furudh_saham)
            
            return CalculationResult(
                # Required fields
                tirkah=self.tirkah,
                ashlul_masalah_awal=ashl_awal_original if ashl_awal_original else ashl,
                ashlul_masalah_akhir=ashl_akhir,
                total_saham=float(total_furudh_saham_final),
                status=distribution_type,
                
                # Boolean flags
                is_aul=(distribution_type == "Aul"),
                is_radd=(distribution_type == "Radd"),
                is_special_case=False,
                
                # Optional fields
                aul_type=None,
                special_case_name=None,
                calculation_metadata=None,
                
                # Shares list
                shares=shares_result,
                
                # Notes
                notes=self.notes
            )
            
        except Exception as e:
            logger.exception(f"ERROR in calculation: {str(e)}")
            self.notes.append(f"❌ ERROR: {str(e)}")
            return self._create_error_result(str(e))
    
    def _create_error_result(self, error_message: str) -> CalculationResult:
        """
        Buat CalculationResult untuk error case yang SESUAI SCHEMA
        """
        logger.error(f"Creating error result: {error_message}")
        
        return CalculationResult(
            tirkah=self.tirkah,
            ashlul_masalah_awal=0,
            ashlul_masalah_akhir=0,
            total_saham=0,
            status="ERROR",
            is_aul=False,
            is_radd=False,
            is_special_case=False,
            aul_type=None,
            special_case_name=None,
            calculation_metadata=None,
            shares=[],
            notes=self.notes + [f"❌ ERROR: {error_message}"]
        )
    
    def _distribute_ashobah(self, furudh_results: List[FurudhResult], 
                       sisa_saham: float) -> List[tuple]:
        """Distribusikan sisa ke ashobah dengan rasio 2:1 untuk laki-laki:perempuan"""
        ashobah_list = [f for f in furudh_results if f.is_ashobah]
        
        if not ashobah_list:
            return []
        
        MALE_ASABAH_IDS = {1, 5, 2, 6, 7, 8, 10, 11, 12, 13, 14, 15}
        FEMALE_ASABAH_IDS = {16, 17, 21, 22}
        
        has_male = any(ashobah.heir_id in MALE_ASABAH_IDS for ashobah in ashobah_list)
        has_female = any(ashobah.heir_id in FEMALE_ASABAH_IDS for ashobah in ashobah_list)
        
        result = []
        
        if has_male and has_female:
            self.notes.append("  📌 Distribusi Ashobah dengan rasio 2:1 (laki-laki:perempuan)")
            
            total_ratio = 0
            for ashobah in ashobah_list:
                if ashobah.heir_id in MALE_ASABAH_IDS:
                    total_ratio += (2 * ashobah.quantity)
                else:
                    total_ratio += (1 * ashobah.quantity)
            
            self.notes.append(f"  Total rasio: {total_ratio}")
            
            for ashobah in ashobah_list:
                heir_name = HEIR_NAMES.get(ashobah.heir_id, {}).get("id", "Unknown")
                
                if ashobah.heir_id in MALE_ASABAH_IDS:
                    saham_per_person = (sisa_saham * 2) / total_ratio
                    total_saham_heir = saham_per_person * ashobah.quantity
                    
                    result.append((ashobah, total_saham_heir))
                    self.notes.append(f"  • {heir_name} (Laki-laki, rasio 2): {total_saham_heir:.2f} saham")
                    
                else:
                    saham_per_person = (sisa_saham * 1) / total_ratio
                    total_saham_heir = saham_per_person * ashobah.quantity
                    
                    result.append((ashobah, total_saham_heir))
                    self.notes.append(f"  • {heir_name} (Perempuan, rasio 1): {total_saham_heir:.2f} saham")
        
        else:
            total_people = sum(ashobah.quantity for ashobah in ashobah_list)
            saham_per_person = sisa_saham / total_people
            
            self.notes.append(f"  📌 Distribusi Ashobah merata ({total_people} orang)")
            
            for ashobah in ashobah_list:
                total_saham_heir = saham_per_person * ashobah.quantity
                result.append((ashobah, total_saham_heir))
                
                heir_name = HEIR_NAMES.get(ashobah.heir_id, {}).get("id", "Unknown")
                self.notes.append(f"  • {heir_name} (Ashobah): {total_saham_heir:.2f} saham")
        
        return result
    
    def _calculate_special_case(self, case_name: str) -> CalculationResult:
        """Placeholder untuk kasus khusus"""
        logger.warning(f"Special case '{case_name}' not yet implemented")
        self.notes.append(f"⚠️ Kasus khusus '{case_name}' belum diimplementasikan")
        return self._create_error_result(f"Special case '{case_name}' not implemented")


def calculate_inheritance(calculation_input: CalculationInput) -> CalculationResult:
    """Function helper untuk menghitung warisan"""
    logger.info(f"\n{'='*60}")
    logger.info(f"CALCULATION REQUEST at {datetime.now()}")
    logger.info(f"{'='*60}")
    
    calculator = FaroidCalculator(calculation_input)
    return calculator.calculate()
