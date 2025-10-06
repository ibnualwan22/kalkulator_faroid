"""
Main Calculator untuk Perhitungan Warisan
Dengan dukungan kasus khusus: Akdariyyah, Jadd ma'al-Ikhwah, dll.
"""
from __future__ import annotations
from typing import List, Dict, Optional

from click import Tuple
from app.schemas.calculation import CalculationInput, CalculationResult, HeirShare
from app.schemas.heir import HeirResponse
from app.core.furudh_engine import FurudhEngine, FurudhResult
from app.core.ashl_calculator import AshlCalculator
from app.utils.constants import HeirID, HEIR_NAMES
from app.utils.math_helpers import fraction_to_string, distribute_shares


class FaroidCalculator:
    """Main calculator untuk faraid"""
    
    def __init__(self, calculation_input: CalculationInput):
        self.input = calculation_input
        self.heirs = calculation_input.heirs
        self.tirkah = calculation_input.tirkah
        self.notes = []
        
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
    
    def _calculate_special_case(self, case_name: str) -> CalculationResult:
        """Handle special cases"""
        from app.special_cases import (
            calculate_akdariyyah,
            calculate_jadd_ikhwah,
            calculate_musytarakah,
            calculate_gharrawin
        )
        
        self.notes.append(f"🔹 Kasus Khusus: {case_name.upper()}")
        self.notes.append("")
        
        if case_name == "akdariyyah":
            return calculate_akdariyyah(self.heirs, self.tirkah, self.notes)
        elif case_name == "jadd_ikhwah":
            return calculate_jadd_ikhwah(self.heirs, self.tirkah, self.notes)
        elif case_name == "musytarakah":
            return calculate_musytarakah(self.heirs, self.tirkah, self.notes)
        elif case_name == "gharrawin":
            return calculate_gharrawin(self.heirs, self.tirkah, self.notes)
        
        # Fallback ke normal jika tidak ada handler
        return self._calculate_normal()
    
    def _calculate_normal(self) -> CalculationResult:
        """
        Perhitungan normal (tanpa kasus khusus)
            
        Returns:
            CalculationResult
        """
        from app.utils.constants import HEIR_NAMES
        from app.core.ashl_calculator import AshlCalculator
        
        # 1. Tentukan Furudh
        self.notes.append("📋 TAHAP 1: Menentukan Furudh Muqaddarah")
        furudh_engine = FurudhEngine(self.heirs)
        furudh_results = furudh_engine.determine_furudh()
        
        for furudh in furudh_results:
            heir_name = HEIR_NAMES.get(furudh.heir_id, {}).get("id", "Unknown")
            if furudh.is_ashobah:
                self.notes.append(f"  • {heir_name}: Ashobah")
            else:
                self.notes.append(f"  • {heir_name}: {furudh.fardh}")
        self.notes.append("")
        
        # 2. Hitung Ashl al-Mas'alah
        self.notes.append("📊 TAHAP 2: Menghitung Ashl al-Mas'alah")
        
        # Cek apakah semua ashobah (tidak ada dzawil furudh)
        all_ashobah = all(f.is_ashobah for f in furudh_results)
        has_ashobah = any(f.is_ashobah for f in furudh_results)
        
        if all_ashobah:
            # ===== KASUS KHUSUS: SEMUA ASHOBAH =====
            MALE_ASABAH_IDS = {1, 5, 2, 6, 7, 8, 10, 11, 12, 13, 14, 15}
            FEMALE_ASABAH_IDS = {16, 17, 21, 22}
            
            has_female = any(f.heir_id in FEMALE_ASABAH_IDS for f in furudh_results)
            
            if has_female:
                ashl_awal = 0
                self.notes.append("Semua Ashobah dengan rasio laki-laki:perempuan = 2:1")
                
                for f in furudh_results:
                    heir_name = HEIR_NAMES.get(f.heir_id, {}).get("id", "Unknown")
                    
                    if f.heir_id in MALE_ASABAH_IDS:
                        bagian = 2 * f.quantity
                        ashl_awal += bagian
                        self.notes.append(f"  • {heir_name} ({f.quantity} orang) × 2 = {bagian} bagian")
                    else:
                        bagian = 1 * f.quantity
                        ashl_awal += bagian
                        self.notes.append(f"  • {heir_name} ({f.quantity} orang) × 1 = {bagian} bagian")
                
                self.notes.append(f"Ashl al-Mas'alah (Total Rasio): {ashl_awal}")
            else:
                ashl_awal = sum(f.quantity for f in furudh_results)
                self.notes.append("Semua Ashobah laki-laki - dibagi rata")
                self.notes.append(f"Ashl al-Mas'alah: {ashl_awal}")
            
            ashl_akhir = ashl_awal
            status = "Adil"
            is_aul = False
            is_radd = False
            
            # Buat shares untuk semua ashobah
            furudh_saham = [(f, ashl_awal // len(furudh_results) if not has_female else 
                            (2 if f.heir_id in MALE_ASABAH_IDS else 1) * f.quantity) 
                        for f in furudh_results]
            
        else:
            # ===== ADA DZAWIL FURUDH =====
            ashl_calculator = AshlCalculator()
            ashl_awal, ashl_notes = ashl_calculator.calculate_ashl(furudh_results)
            self.notes.extend(ashl_notes)
            
            # 3. Hitung Saham Furudh (JANGAN PRINT DULU!)
            furudh_with_fardh = [f for f in furudh_results if not f.is_ashobah]
            furudh_saham = ashl_calculator.calculate_saham(furudh_with_fardh, ashl_awal)
            total_furudh_saham = sum(saham for _, saham in furudh_saham if saham > 0)
            
            # 4. Cek 'Aul, Radd, atau Adil
            status, is_aul, is_radd = ashl_calculator.check_aul_or_radd(
                total_furudh_saham, 
                ashl_awal, 
                has_ashobah
            )
            
            # ✅ PRINT TAHAP 3 - HANDLING BERBEDA UNTUK RADD
            if not is_radd:
                # Kalau BUKAN Radd, print saham normal
                self.notes.append("")
                self.notes.append("🔢 TAHAP 3: Menghitung Saham")
                for furudh, saham in furudh_saham:
                    if saham > 0:
                        heir_name = HEIR_NAMES.get(furudh.heir_id, {}).get("id", "Unknown")
                        self.notes.append(f"  • {heir_name}: {saham} saham")
                
                self.notes.append(f"  Total Saham Furudh: {total_furudh_saham}")
                self.notes.append("")
            
            # 5. Handle status
            if is_aul:
                # ===== 'AUL =====
                ashl_akhir = int(total_furudh_saham)
                self.notes.append("⚠️ TERJADI 'AUL (Kelebihan)")
                self.notes.append(f"  Ashl dinaikkan dari {ashl_awal} menjadi {ashl_akhir}")
                self.notes.append("")
                
            elif is_radd:
                # ===== RADD - 3 KASUS =====
                from app.core.radd import RaddCalculator
                
                radd_calc = RaddCalculator(furudh_results, self.tirkah)
                ashl_awal_radd, ashl_akhir, radd_shares, radd_notes = radd_calc.calculate_radd()
                
                self.notes.append("⚠️ TERJADI RADD (Pengembalian Sisa)")
                self.notes.extend(radd_notes)
                self.notes.append("")
                
                # ✅ Update furudh_saham dengan hasil radd untuk perhitungan tirkah
                furudh_saham = radd_shares
                
            elif has_ashobah:
                # ===== ADIL (Ada Ashobah) =====
                ashl_akhir = ashl_awal
                sisa_saham = ashl_akhir - total_furudh_saham
                
                self.notes.append("")
                self.notes.append("✅ Pembagian ADIL (Ada Ashobah)")
                self.notes.append(f"  Sisa {sisa_saham} saham untuk Ashobah")
                self.notes.append("")
                
                # Distribusi ke Ashobah
                self.notes.append(f"💰 Sisa untuk Ashobah: {sisa_saham} saham")
                ashobah_results = self._distribute_ashobah(furudh_results, sisa_saham)
                furudh_saham.extend(ashobah_results)
                self.notes.append("")
                
            else:
                # ===== PAS (Tidak ada sisa, tidak ada ashobah) =====
                ashl_akhir = ashl_awal
                self.notes.append("")
                self.notes.append("✅ Pembagian PAS (Tepat)")
                self.notes.append("")
        
        # 6. Distribusi ke Rupiah
        self.notes.append("💵 TAHAP 4: Distribusi Tirkah")
        shares = self._create_heir_shares(furudh_saham, ashl_akhir)
        
        # 7. Build result
        return CalculationResult(
            tirkah=self.tirkah,
            ashlul_masalah_awal=ashl_awal,
            ashlul_masalah_akhir=ashl_akhir,
            total_saham=sum(s.saham for s in shares),
            status=status,
            is_aul=is_aul,
            is_radd=is_radd,
            is_special_case=False,
            shares=shares,
            notes=self.notes
        )



    
    def _distribute_ashobah(self, furudh_results: List[FurudhResult], 
                       sisa_saham: float) -> List[Tuple[FurudhResult, float]]:
        """
        Distribusikan sisa ke ashobah dengan rasio 2:1 untuk laki-laki:perempuan
        
        Args:
            furudh_results: List furudh results
            sisa_saham: Sisa saham untuk ashobah
            
        Returns:
            List tuple (FurudhResult, saham)
        """
        ashobah_list = [f for f in furudh_results if f.is_ashobah]
        
        if not ashobah_list:
            return []
        
        # Konstanta ID untuk ashobah laki-laki dan perempuan
        MALE_ASABAH_IDS = {1, 5, 2, 6, 7, 8, 10, 11, 12, 13, 14, 15}
        FEMALE_ASABAH_IDS = {16, 17, 21, 22}
        
        # Cek apakah ada campuran laki-laki + perempuan
        has_male = any(ashobah.heir_id in MALE_ASABAH_IDS for ashobah in ashobah_list)
        has_female = any(ashobah.heir_id in FEMALE_ASABAH_IDS for ashobah in ashobah_list)
        
        result = []
        
        if has_male and has_female:
            # ========== KASUS KHUSUS: RASIO 2:1 ==========
            # Contoh: 1 anak laki-laki + 1 anak perempuan
            # Total rasio = (1 × 2) + (1 × 1) = 3
            # Laki-laki dapat: 2/3, Perempuan dapat: 1/3
            
            self.notes.append("  📌 Distribusi Ashobah dengan rasio 2:1 (laki-laki:perempuan)")
            
            # Hitung total rasio
            total_ratio = 0
            for ashobah in ashobah_list:
                if ashobah.heir_id in MALE_ASABAH_IDS:
                    # Laki-laki: 2 bagian per orang
                    total_ratio += (2 * ashobah.quantity)
                else:
                    # Perempuan: 1 bagian per orang
                    total_ratio += (1 * ashobah.quantity)
            
            self.notes.append(f"  Total rasio: {total_ratio}")
            
            # Distribusi berdasarkan rasio
            for ashobah in ashobah_list:
                heir_name = HEIR_NAMES.get(ashobah.heir_id, {}).get("id", "Unknown")
                
                if ashobah.heir_id in MALE_ASABAH_IDS:
                    # Laki-laki: (2 × quantity) / total_ratio
                    saham_per_person = (sisa_saham * 2) / total_ratio
                    total_saham_heir = saham_per_person * ashobah.quantity
                    
                    result.append((ashobah, total_saham_heir))
                    self.notes.append(f"  • {heir_name} (Laki-laki, rasio 2): {total_saham_heir:.2f} saham")
                    
                else:
                    # Perempuan: (1 × quantity) / total_ratio
                    saham_per_person = (sisa_saham * 1) / total_ratio
                    total_saham_heir = saham_per_person * ashobah.quantity
                    
                    result.append((ashobah, total_saham_heir))
                    self.notes.append(f"  • {heir_name} (Perempuan, rasio 1): {total_saham_heir:.2f} saham")
        
        else:
            # ========== KASUS NORMAL: BAGI RATA ==========
            # Semua laki-laki atau semua perempuan
            
            total_people = sum(ashobah.quantity for ashobah in ashobah_list)
            saham_per_person = sisa_saham / total_people
            
            self.notes.append(f"  📌 Distribusi Ashobah merata ({total_people} orang)")
            
            for ashobah in ashobah_list:
                total_saham_heir = saham_per_person * ashobah.quantity
                result.append((ashobah, total_saham_heir))
                
                heir_name = HEIR_NAMES.get(ashobah.heir_id, {}).get("id", "Unknown")
                self.notes.append(f"  • {heir_name} (Ashobah): {total_saham_heir:.2f} saham")
        
        return result
    
    def _create_heir_shares(self, furudh_saham: List[Tuple[FurudhResult, float]], 
                           ashl: int) -> List[HeirShare]:
        """
        Buat HeirShare objects dengan distribusi rupiah
        
        Args:
            furudh_saham: List tuple (FurudhResult, saham)
            ashl: Ashl akhir
            
        Returns:
            List HeirShare
        """
        shares = []
        
        for furudh, saham in furudh_saham:
            # Get heir info
            heir_info = HEIR_NAMES.get(furudh.heir_id, {"id": "Unknown", "ar": "Unknown"})
            heir_response = HeirResponse(
                id=furudh.heir_id,
                name_id=heir_info["id"],
                name_ar=heir_info["ar"]
            )
            
            # Calculate rupiah
            share_amount = (saham / ashl) * self.tirkah
            percentage = f"{(saham / ashl) * 100:.2f}%"
            
            # Create share
            share = HeirShare(
                heir=heir_response,
                quantity=furudh.quantity,
                fardh=furudh.fardh if not furudh.is_ashobah else None,
                share_fraction=fraction_to_string(int(saham), ashl),
                saham=saham,
                reason=furudh.reason,
                share_amount=share_amount,
                percentage=percentage,
                is_mahjub=False
            )
            
            shares.append(share)
            
            # Add to notes
            self.notes.append(f"  • {heir_info['id']}: Rp {share_amount:,.0f} ({percentage})")
        
        return shares


def calculate_inheritance(calculation_input: CalculationInput) -> CalculationResult:
    """
    Function helper untuk menghitung warisan
    
    Args:
        calculation_input: Input perhitungan
        
    Returns:
        CalculationResult
    """
    calculator = FaroidCalculator(calculation_input)
    return calculator.calculate()
