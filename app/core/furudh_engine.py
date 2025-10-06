"""
Engine untuk menentukan Furudh Muqaddarah (bagian tetap)
Berdasarkan Kitab Zahrotul Faridhah
"""
from __future__ import annotations
from typing import List, Dict, Tuple, Optional
from app.schemas.calculation import HeirShare
from app.schemas.heir import HeirInput, HeirResponse
from app.utils.constants import HeirID, HEIR_NAMES, FURUDH_RULES
from app.utils.math_helpers import parse_fraction
import logging

logger = logging.getLogger(__name__)


class FurudhResult:
    """Class untuk menyimpan hasil perhitungan furudh"""
    def __init__(self, heir_id: int, quantity: int, fardh: str, 
                 numerator: int, denominator: int, reason: str):
        self.heir_id = heir_id
        self.quantity = quantity
        self.fardh = fardh
        self.numerator = numerator
        self.denominator = denominator
        self.reason = reason
        self.is_ashobah = (fardh == "Ashobah")


class FurudhEngine:
    """Engine untuk menghitung furudh muqaddarah"""
    
    def __init__(self, heirs: List[HeirInput]):
        self.heirs = heirs
        self.heir_dict = {h.id: h.quantity for h in heirs}
        
    def has_heir(self, heir_id: int) -> bool:
        """Cek apakah ahli waris ada"""
        return heir_id in self.heir_dict and self.heir_dict[heir_id] > 0
    
    def has_any_heir(self, heir_ids: List[int]) -> bool:
        """Cek apakah salah satu ahli waris ada"""
        return any(self.has_heir(hid) for hid in heir_ids)
    
    def count_siblings(self) -> int:
        """Hitung total saudara/i (semua jenis)"""
        sibling_ids = [
            HeirID.AKH_ABAWAYN, HeirID.AKH_AB, HeirID.AKH_UMM,
            HeirID.UKHT_ABAWAYN, HeirID.UKHT_AB, HeirID.UKHT_UMM
        ]
        return sum(self.heir_dict.get(hid, 0) for hid in sibling_ids)
    
    def determine_furudh(self) -> List[FurudhResult]:
        """
        Tentukan furudh untuk semua ahli waris
        
        Returns:
            List FurudhResult
        """
        results = []
        
        logger.info(f"=== MULAI DETERMINE FURUDH ===")
        logger.info(f"Input heirs: {[(h.id, h.quantity) for h in self.heirs]}")
        
        for heir in self.heirs:
            heir_id = heir.id
            quantity = heir.quantity
            heir_name = HEIR_NAMES.get(heir_id, {}).get("id", f"Unknown-{heir_id}")
            
            logger.info(f"\n--- Processing: {heir_name} (ID: {heir_id}, Qty: {quantity}) ---")
            
            # ===== CEK ASHOBAH MURNI (TIDAK PUNYA FARDH) =====
            if heir_id in self._get_pure_ashobah_ids():
                logger.info(f"✓ {heir_name} adalah Pure Ashobah")
                results.append(FurudhResult(
                    heir_id=heir_id,
                    quantity=quantity,
                    fardh="Ashobah",
                    numerator=0,
                    denominator=0,
                    reason=self._get_ashobah_reason(heir_id)
                ))
                continue
            
            # ===== CEK APAKAH ADA ATURAN FURUDH =====
            if heir_id not in FURUDH_RULES:
                logger.warning(f"⚠ {heir_name} tidak ada di FURUDH_RULES - SKIP")
                continue
            
            # Ambil aturan furudh untuk ahli waris ini
            rules = FURUDH_RULES[heir_id]
            logger.info(f"  Ditemukan {len(rules)} aturan furudh")
            
            # Cari aturan yang cocok
            furudh_result = self._apply_rules(heir_id, quantity, rules)
            
            if furudh_result:
                logger.info(f"✓ {heir_name} → {furudh_result.fardh}")
                results.append(furudh_result)
            else:
                logger.warning(f"✗ {heir_name} tidak ada aturan yang cocok (mahjub/ashobah)")
        
        logger.info(f"\n=== SELESAI DETERMINE FURUDH ===")
        logger.info(f"Total results: {len(results)}")
        for r in results:
            heir_name = HEIR_NAMES.get(r.heir_id, {}).get("id", f"Unknown-{r.heir_id}")
            logger.info(f"  - {heir_name}: {r.fardh}")
        
        return results
    
    def _get_pure_ashobah_ids(self) -> List[int]:
        """
        Daftar ID ahli waris yang pure ashobah (tidak punya fardh)
        Berdasarkan Kitab Zahrotul Faridhah
        """
        return [
            HeirID.IBN,              # 1 - Anak Laki-laki
            HeirID.IBN_IBN,          # 5 - Cucu Laki-laki dari anak laki-laki
            # HeirID.ABB,            # 2 - Ayah (TIDAK! Ayah punya fardh 1/6)
            # HeirID.JADD,           # 6 - Kakek (TIDAK! Kakek punya fardh 1/6)
            HeirID.AKH_ABAWAYN,      # 7 - Saudara Laki-laki Kandung
            HeirID.AKH_AB,           # 8 - Saudara Laki-laki Seayah
            HeirID.IBN_AKH_ABAWAYN,  # 10 - Keponakan Laki-laki dari sdr lk kandung
            HeirID.IBN_AKH_AB,       # 11 - Keponakan Laki-laki dari sdr lk seayah
            HeirID.AMM_ABAWAYN,      # 12 - Paman Kandung
            HeirID.AMM_AB,           # 13 - Paman Seayah
            HeirID.IBN_AMM_ABAWAYN,  # 14 - Sepupu Laki-laki dari paman kandung
            HeirID.IBN_AMM_AB,       # 15 - Sepupu Laki-laki dari paman seayah
        ]
    
    def _get_ashobah_reason(self, heir_id: int) -> str:
        """Dapatkan alasan untuk ashobah berdasarkan kitab"""
        reasons = {
            HeirID.IBN: (
                "Anak laki-laki menjadi Ashobah bi nafsihi (ashobah dengan dirinya sendiri). "
                "Jika ada anak perempuan, mereka berbagi dengan rasio 2:1 sesuai QS. An-Nisa ayat 11: "
                "للذَّكَرِ مِثْلُ حَظِّ الأُنثَيَيْنِ "
                "(Lilldzakari mitslu hadzhil untsayain - bagi anak laki-laki bagian dua anak perempuan)."
            ),
            HeirID.IBN_IBN: "Cucu laki-laki dari anak laki-laki menjadi Ashobah bi nafsihi.",
            HeirID.AKH_ABAWAYN: "Saudara laki-laki kandung menjadi Ashobah bi nafsihi.",
            HeirID.AKH_AB: "Saudara laki-laki seayah menjadi Ashobah bi nafsihi.",
            HeirID.IBN_AKH_ABAWAYN: "Keponakan laki-laki dari saudara kandung menjadi Ashobah bi nafsihi.",
            HeirID.IBN_AKH_AB: "Keponakan laki-laki dari saudara seayah menjadi Ashobah bi nafsihi.",
            HeirID.AMM_ABAWAYN: "Paman kandung menjadi Ashobah bi nafsihi.",
            HeirID.AMM_AB: "Paman seayah menjadi Ashobah bi nafsihi.",
            HeirID.IBN_AMM_ABAWAYN: "Sepupu laki-laki dari paman kandung menjadi Ashobah bi nafsihi.",
            HeirID.IBN_AMM_AB: "Sepupu laki-laki dari paman seayah menjadi Ashobah bi nafsihi.",
        }
        return reasons.get(heir_id, "Menjadi Ashobah (mengambil sisa setelah dzawil furudh).")
    
    def _apply_rules(self, heir_id: int, quantity: int, 
                     rules: List[Dict]) -> Optional[FurudhResult]:
        """
        Terapkan aturan furudh untuk satu ahli waris
        
        Args:
            heir_id: ID ahli waris
            quantity: Jumlah ahli waris
            rules: List aturan furudh
            
        Returns:
            FurudhResult atau None jika mahjub
        """
        heir_name = HEIR_NAMES.get(heir_id, {}).get("id", f"Unknown-{heir_id}")
        
        for idx, rule in enumerate(rules):
            logger.info(f"  Cek aturan #{idx+1}: {rule.get('fardh', 'N/A')}")
            
            if self._check_rule_conditions(rule, quantity):
                logger.info(f"  ✓ Aturan #{idx+1} COCOK!")
                return self._create_furudh_result(heir_id, quantity, rule)
            else:
                logger.info(f"  ✗ Aturan #{idx+1} tidak cocok")
        
        # Tidak ada aturan yang cocok
        logger.warning(f"  Tidak ada aturan yang cocok untuk {heir_name}")
        return None
    
    def _check_rule_conditions(self, rule: Dict, quantity: int) -> bool:
        """
        Cek apakah kondisi aturan terpenuhi
        
        Args:
            rule: Dictionary aturan
            quantity: Jumlah ahli waris
            
        Returns:
            True jika kondisi terpenuhi
        """
        # Cek kasus khusus
        if "kasus_khusus" in rule:
            result = self._check_special_case(rule["kasus_khusus"])
            logger.info(f"    - Kasus khusus '{rule['kasus_khusus']}': {result}")
            return result
        
        # Cek mahjub
        if "syarat_mahjub" in rule:
            if self.has_any_heir(rule["syarat_mahjub"]):
                logger.info(f"    - MAHJUB oleh: {rule['syarat_mahjub']}")
                return False
        
        # Cek syarat harus ada
        if "syarat_ada" in rule:
            has_required = self.has_any_heir(rule["syarat_ada"])
            
            # Khusus untuk Ibu: cek min_saudara HANYA jika ada saudara
            if "min_saudara" in rule:
                sibling_ids = [
                    HeirID.AKH_ABAWAYN, HeirID.AKH_AB, HeirID.AKH_UMM,
                    HeirID.UKHT_ABAWAYN, HeirID.UKHT_AB, HeirID.UKHT_UMM
                ]
                has_sibling = self.has_any_heir(sibling_ids)
                sibling_count = self.count_siblings()
                
                if has_sibling:
                    # Ada saudara → cek apakah >= min_saudara
                    if sibling_count < rule["min_saudara"]:
                        logger.info(f"    - Saudara {sibling_count} < min {rule['min_saudara']}")
                        return False
                else:
                    # Tidak ada saudara → cek apakah ada anak/cucu
                    has_child_or_grandchild = self.has_any_heir([
                        HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN
                    ])
                    if not has_child_or_grandchild:
                        logger.info(f"    - Tidak ada anak/cucu, tidak ada saudara >= {rule['min_saudara']}")
                        return False
            
            if not has_required:
                logger.info(f"    - Syarat ada tidak terpenuhi: {rule['syarat_ada']}")
                return False
        
        # Cek syarat tidak boleh ada
        if "syarat_tidak_ada" in rule:
            if self.has_any_heir(rule["syarat_tidak_ada"]):
                logger.info(f"    - Syarat tidak ada dilanggar: {rule['syarat_tidak_ada']}")
                return False
        
        # Cek jumlah minimum
        if "jumlah_min" in rule:
            if quantity < rule["jumlah_min"]:
                logger.info(f"    - Jumlah {quantity} < min {rule['jumlah_min']}")
                return False
        
        # Cek jumlah spesifik
        if "jumlah" in rule:
            if quantity != rule["jumlah"]:
                logger.info(f"    - Jumlah {quantity} != required {rule['jumlah']}")
                return False
        
        # Cek max_saudara untuk aturan 1/3 Ibu
        if "max_saudara" in rule:
            sibling_count = self.count_siblings()
            if sibling_count > rule["max_saudara"]:
                logger.info(f"    - Saudara {sibling_count} > max {rule['max_saudara']}")
                return False
        
        logger.info(f"    ✓ Semua kondisi terpenuhi")
        return True

    
    def _check_special_case(self, case_name: str) -> bool:
        """Cek kasus khusus seperti Umariyyatan"""
        if case_name == "umariyyatan":
            has_zawj = self.has_heir(HeirID.ZAWJ)
            has_zawjah = self.has_heir(HeirID.ZAWJAH)
            has_abb = self.has_heir(HeirID.ABB)
            has_umm = self.has_heir(HeirID.UMM)
            
            spouse = has_zawj or has_zawjah
            parents = has_abb and has_umm
            total_heirs = len([h for h in self.heirs if h.quantity > 0])
            
            return spouse and parents and total_heirs == 3
        
        return False
    
    def _create_furudh_result(self, heir_id: int, quantity: int, 
                             rule: Dict) -> FurudhResult:
        """Buat FurudhResult dari aturan"""
        fardh = rule["fardh"]
        reason = rule["alasan"]
        
        if fardh == "Ashobah" or "Ashobah" in fardh:
            return FurudhResult(
                heir_id=heir_id,
                quantity=quantity,
                fardh="Ashobah",
                numerator=0,
                denominator=0,
                reason=reason
            )
        
        if "/" in fardh:
            numerator, denominator = parse_fraction(fardh)
        else:
            if "1/3 sisa" in fardh or "1/3 dari sisa" in fardh:
                numerator, denominator = 1, 3
                reason += " (1/3 dari sisa setelah suami/istri)"
            else:
                numerator, denominator = 1, 1
        
        return FurudhResult(
            heir_id=heir_id,
            quantity=quantity,
            fardh=fardh,
            numerator=numerator,
            denominator=denominator,
            reason=reason
        )


def determine_furudh(heirs: List[HeirInput]) -> List[FurudhResult]:
    """Fungsi helper untuk menentukan furudh"""
    engine = FurudhEngine(heirs)
    return engine.determine_furudh()
