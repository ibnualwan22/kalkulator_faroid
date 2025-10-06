"""
Calculator untuk Ashl al-Mas'alah (asal masalah)
Berdasarkan Kitab Zahrotul Faridhah
"""
from __future__ import annotations
from typing import List, Tuple
from app.utils.constants import HEIR_NAMES
from app.utils.math_helpers import lcm_multiple, gcd_multiple
from app.core.furudh_engine import FurudhResult


class AshlCalculator:
    """Calculator untuk menghitung Ashl al-Mas'alah"""
    
    @staticmethod
    def calculate_ashl(furudh_results: List[FurudhResult]) -> Tuple[int, List[str]]:
        """
        Hitung Ashl al-Mas'alah (KPK dari penyebut furudh)
        
        Args:
            furudh_results: List hasil furudh
            
        Returns:
            Tuple (ashl, notes)
        """
        notes = []
        
        # Ambil semua penyebut dari furudh (skip ashobah)
        denominators = [
            f.denominator for f in furudh_results 
            if f.denominator > 0 and not f.is_ashobah
        ]
        
        if not denominators:
            # Semua ashobah
            notes.append("Semua ahli waris adalah Ashobah")
            return 1, notes
        
        # Hitung KPK (LCM) dari semua penyebut
        ashl = lcm_multiple(denominators)
        
        # Generate notes tentang proses
        notes.append(f"Penyebut furudh yang ada: {', '.join(map(str, set(denominators)))}")
        
        # Identifikasi tipe relasi antar penyebut
        relation_type = AshlCalculator._identify_relation_type(denominators)
        notes.append(f"Tipe relasi: {relation_type}")
        notes.append(f"Ashl al-Mas'alah = {ashl}")
        
        return ashl, notes
    
    @staticmethod
    def _identify_relation_type(denominators: List[int]) -> str:
        """
        Identifikasi tipe relasi antar penyebut
        
        Returns:
            String: Tamaatsul, Tadaakhul, Tawaafuq, atau Tabaayin
        """
        unique_dens = list(set(denominators))
        
        if len(unique_dens) == 1:
            return "Tamaatsul (sama semua)"
        
        # Sort untuk mudah cek
        unique_dens.sort()
        
        # Cek Tadaakhul (masuk/habis dibagi)
        is_tadaakhul = True
        for i in range(len(unique_dens) - 1):
            if unique_dens[i+1] % unique_dens[i] != 0:
                is_tadaakhul = False
                break
        
        if is_tadaakhul:
            return "Tadaakhul (yang lebih besar habis dibagi yang kecil)"
        
        # Cek Tawaafuq (ada FPB > 1)
        fpb = gcd_multiple(unique_dens)
        if fpb > 1:
            return f"Tawaafuq (ada FPB = {fpb})"
        
        # Tabaayin (relatif prima)
        return "Tabaayin (tidak ada kesamaan faktor)"
    
    @staticmethod
    def calculate_saham(furudh_results: List[FurudhResult], ashl: int) -> List[Tuple[FurudhResult, float]]:
        """
        Hitung saham untuk setiap furudh
        
        Args:
            furudh_results: List hasil furudh
            ashl: Ashl al-mas'alah
            
        Returns:
            List tuple (FurudhResult, saham)
        """
        result = []
        
        for furudh in furudh_results:
            if furudh.is_ashobah:
                # Ashobah akan dihitung nanti (sisa)
                saham = 0
            else:
                # Saham = (numerator * ashl) / denominator
                saham = (furudh.numerator * ashl) / furudh.denominator
            
            result.append((furudh, saham))
        
        return result
    
    @staticmethod
    def check_aul_or_radd(total_saham: int, ashl: int, has_ashobah: bool = False) -> Tuple[str, bool, bool]:
        """
        Cek apakah terjadi 'Aul, Radd, atau Adil
        
        Args:
            total_saham: Total saham dzawil furudh
            ashl: Ashl al-mas'alah
            has_ashobah: Apakah ada ashobah yang mengambil sisa
        
        Returns:
            Tuple (status, is_aul, is_radd)
        """
        # ✅ LOGIC BENAR:
        if total_saham > ashl:
            # 'AUL: Total saham LEBIH BESAR dari ashl
            return "'Aul", True, False
        
        elif total_saham < ashl:
            if has_ashobah:
                # Ada ASHOBAH → ADIL (sisa diambil ashobah)
                return "Adil", False, False
            else:
                # TIDAK ada ashobah → RADD
                return "Radd", False, True
        
        else:
            # PAS (total sama dengan ashl)
            return "Adil", False, False
    
    @staticmethod
    def calculate_ashl_all_ashobah(furudh_results: List[FurudhResult]) -> Tuple[int, List[str]]:
        """
        Calculate ashl ketika SEMUA ashobah (tidak ada dzawil furudh)
        
        Jika ada campuran laki-laki + perempuan: gunakan rasio 2:1
        Jika semua laki-laki: jumlah orang
        
        Args:
            furudh_results: List hasil furudh (semua ashobah)
            
        Returns:
            Tuple (ashl, notes)
        """
        notes = []
        
        # ID untuk laki-laki dan perempuan ashobah
        MALE_ASABAH_IDS = {1, 5, 2, 6, 7, 8, 10, 11, 12, 13, 14, 15}
        FEMALE_ASABAH_IDS = {16, 17, 21, 22}
        
        # Cek apakah ada perempuan
        has_female = any(f.heir_id in FEMALE_ASABAH_IDS for f in furudh_results)
        
        if has_female:
            # Ada perempuan → gunakan rasio 2:1
            total_ratio = 0
            
            for furudh in furudh_results:
                if furudh.heir_id in MALE_ASABAH_IDS:
                    # Laki-laki: 2 per orang
                    total_ratio += (2 * furudh.quantity)
                    heir_name = HEIR_NAMES.get(furudh.heir_id, {}).get('id', 'Unknown')
                    notes.append(f"  • {heir_name} ({furudh.quantity} orang): {2 * furudh.quantity} bagian")
                else:
                    # Perempuan: 1 per orang
                    total_ratio += (1 * furudh.quantity)
                    heir_name = HEIR_NAMES.get(furudh.heir_id, {}).get('id', 'Unknown')
                    notes.append(f"  • {heir_name} ({furudh.quantity} orang): {1 * furudh.quantity} bagian")
            
            notes.insert(0, "Semua Ashobah dengan rasio laki-laki:perempuan = 2:1")
            notes.append(f"Total rasio (Ashl): {total_ratio}")
            
            return total_ratio, notes
        
        else:
            # Semua laki-laki → bagi rata
            total_people = sum(f.quantity for f in furudh_results)
            
            notes.append("Semua Ashobah laki-laki - dibagi rata")
            notes.append(f"Ashl = jumlah orang = {total_people}")
            
            return total_people, notes
