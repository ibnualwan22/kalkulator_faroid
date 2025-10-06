"""
Module untuk menghitung RADD (الرَّدُّ)
Berdasarkan Kitab Zahrotul Faridhah
"""
from typing import List, Tuple, Dict
from app.utils.constants import HeirID
from app.utils.math_helpers import lcm, gcd


class RaddCalculator:
    """Calculator untuk kasus Radd"""
    
    def __init__(self, furudh_results, tirkah: float):
        self.furudh_results = furudh_results
        self.tirkah = tirkah
        
        # ID Zauj dan Zaujah
        self.SPOUSE_IDS = {HeirID.ZAWJ, HeirID.ZAWJAH}
    
    def check_radd_condition(self) -> Tuple[bool, int]:
        """
        Cek apakah terjadi radd dan hitung ashl awal
        
        Returns:
            (is_radd, ashl_awal)
        """
        # Hitung total saham dzawil furudh
        total_saham = sum(
            f.numerator for f in self.furudh_results 
            if not f.is_ashobah
        )
        
        # Hitung ashl (KPK dari penyebut)
        denominators = [
            f.denominator for f in self.furudh_results 
            if not f.is_ashobah and f.denominator > 0
        ]
        ashl = denominators[0]
        for d in denominators[1:]:
            ashl = lcm(ashl, d)
        
        # Radd terjadi jika total < ashl dan tidak ada ashobah
        has_ashobah = any(f.is_ashobah for f in self.furudh_results)
        
        if total_saham < ashl and not has_ashobah:
            return True, ashl
        
        return False, ashl
    
    def calculate_radd(self) -> Tuple[int, int, List[Tuple], List[str]]:
        """
        Hitung Radd berdasarkan 3 kasus
        
        Returns:
            (ashl_awal, ashl_akhir, radd_shares, notes)
        """
        notes = []
        
        # Cek apakah ada zauj/zaujah
        has_spouse = any(
            f.heir_id in self.SPOUSE_IDS 
            for f in self.furudh_results
        )
        
        # Pisahkan ahli waris yang dapat radd (bukan zauj/zaujah)
        radd_heirs = [
            f for f in self.furudh_results 
            if f.heir_id not in self.SPOUSE_IDS and not f.is_ashobah
        ]
        
        if not has_spouse:
            # KASUS 1: Tanpa Zauj/Zaujah
            return self._calculate_radd_without_spouse(radd_heirs, notes)
        
        elif len(radd_heirs) == 1:
            # KASUS 2: Ada Zauj/Zaujah + Ahli Waris Cuma 1
            return self._calculate_radd_one_heir(radd_heirs, notes)
        
        else:
            # KASUS 3: Ada Zauj/Zaujah + Ahli Waris > 1
            return self._calculate_radd_multiple_heirs(radd_heirs, notes)
    
    def _calculate_radd_without_spouse(self, radd_heirs, notes):
        """Kasus 1: Tanpa Zauj/Zaujah"""
        notes.append("🔹 KASUS RADD 1: Tanpa Zauj/Zaujah")
        notes.append("   Jumlah saham dijadikan Ashl Mas'alah")
        
        # Hitung ashl awal (KPK penyebut)
        denominators = [h.denominator for h in radd_heirs]
        ashl_awal = denominators[0]
        for d in denominators[1:]:
            ashl_awal = lcm(ashl_awal, d)
        
        # Hitung saham masing-masing
        total_saham = 0
        shares = []
        for heir in radd_heirs:
            saham = (ashl_awal // heir.denominator) * heir.numerator
            total_saham += saham
            shares.append((heir, saham))
        
        # Ashl akhir = total saham
        ashl_akhir = total_saham
        
        notes.append(f"   Ashl Awal: {ashl_awal}")
        notes.append(f"   Total Saham: {total_saham}")
        notes.append(f"   Ashl Akhir: {ashl_akhir}")
        
        return ashl_awal, ashl_akhir, shares, notes
    
    def _calculate_radd_one_heir(self, radd_heirs, notes):
        """Kasus 2: Ada Zauj/Zaujah + 1 Ahli Waris"""
        notes.append("🔹 KASUS RADD 2: Ada Zauj/Zaujah + 1 Ahli Waris")
        notes.append("   Penyebut zauj dijadikan Ashl, buat perbandingan")
        
        # Get zauj/zaujah
        spouse = next(
            f for f in self.furudh_results 
            if f.heir_id in self.SPOUSE_IDS
        )
        
        # Ashl awal = penyebut zauj
        ashl_awal = spouse.denominator
        
        # Saham zauj
        zauj_saham = (ashl_awal // spouse.denominator) * spouse.numerator
        
        # Sisa untuk radd
        sisa = ashl_awal - zauj_saham
        
        # Ahli waris radd dapat sisa
        heir = radd_heirs[0]
        heir_saham_awal = (ashl_awal // heir.denominator) * heir.numerator
        heir_saham_radd = heir_saham_awal + sisa
        
        shares = [
            (spouse, zauj_saham),
            (heir, heir_saham_radd)
        ]
        
        ashl_akhir = ashl_awal
        
        notes.append(f"   Ashl (dari penyebut zauj): {ashl_awal}")
        notes.append(f"   Zauj: {zauj_saham} saham")
        notes.append(f"   Sisa untuk radd: {sisa}")
        notes.append(f"   Ahli waris radd: {heir_saham_awal} + {sisa} = {heir_saham_radd}")
        
        return ashl_awal, ashl_akhir, shares, notes
    
    def _calculate_radd_multiple_heirs(self, radd_heirs, notes):
        """Kasus 3: Ada Zauj/Zaujah + >1 Ahli Waris (INKISAR)"""
        notes.append("🔹 KASUS RADD 3: Ada Zauj/Zaujah + Ahli Waris > 1")
        
        from app.utils.constants import HEIR_NAMES
        from app.utils.math_helpers import lcm
        
        # Get zauj/zaujah
        spouse = next(
            f for f in self.furudh_results 
            if f.heir_id in self.SPOUSE_IDS
        )
        
        # LANGKAH A: Penyebut zauj dijadikan Ashl zauj
        ashl_zauj = spouse.denominator
        zauj_numerator = spouse.numerator
        notes.append(f"   a) Ashl dari penyebut zauj/zaujah: {ashl_zauj}")
        notes.append(f"   Zauj/Zaujah: {zauj_numerator}/{ashl_zauj}")
        
        # LANGKAH B: Hitung Ashl baru untuk ahli waris radd
        denominators_radd = [h.denominator for h in radd_heirs]
        ashl_radd = denominators_radd[0]
        for d in denominators_radd[1:]:
            ashl_radd = lcm(ashl_radd, d)
        
        notes.append(f"   b) Ashl baru untuk ahli waris radd: {ashl_radd}")
        
        # Hitung saham ahli waris radd (proporsi dari ashl_radd)
        total_saham_radd = 0
        radd_saham_list = []
        for heir in radd_heirs:
            saham = (ashl_radd // heir.denominator) * heir.numerator
            total_saham_radd += saham
            radd_saham_list.append((heir, saham))
            
            heir_name = HEIR_NAMES.get(heir.heir_id, {}).get("id", "Unknown")
            notes.append(f"     • {heir_name}: {saham}/{ashl_radd}")
        
        notes.append(f"   Total saham ahli waris radd: {total_saham_radd}/{ashl_radd}")
        
        # ===== HITUNG AM AWAL (LCM SEMUA PENYEBUT) =====
        # Ini untuk cek "terbagi utuh" dengan benar
        all_denominators = [spouse.denominator] + denominators_radd
        ashl_awal_full = all_denominators[0]
        for d in all_denominators[1:]:
            ashl_awal_full = lcm(ashl_awal_full, d)
        
        notes.append(f"   AM Awal (semua furudh): {ashl_awal_full}")
        
        # Zauj saham di AM Awal
        zauj_saham_di_ashl_awal = (ashl_awal_full // ashl_zauj) * zauj_numerator
        
        # Total saham radd di AM Awal
        total_radd_di_ashl_awal = 0
        for heir in radd_heirs:
            saham = (ashl_awal_full // heir.denominator) * heir.numerator
            total_radd_di_ashl_awal += saham
        
        # Sisa setelah zauj
        sisa = ashl_awal_full - zauj_saham_di_ashl_awal
        notes.append(f"   Zauj di AM Awal: {zauj_saham_di_ashl_awal}, Sisa: {sisa}")
        
        # LANGKAH C: Cek apakah SISA habis dibagi TOTAL_RADD
        if sisa % total_saham_radd == 0:
            # ===== TERBAGI UTUH =====
            ashl_akhir = ashl_awal_full
            faktor_radd = sisa // total_saham_radd
            
            notes.append(f"   c) Sudah bisa terbagi utuh")
            notes.append(f"   Sisa {sisa} ÷ {total_saham_radd} = {faktor_radd} (bulat)")
            notes.append(f"   Ashl Akhir: {ashl_akhir}")
            
            shares = [(spouse, zauj_saham_di_ashl_awal)]
            
            for heir, saham_radd in radd_saham_list:
                final_saham = saham_radd * faktor_radd
                shares.append((heir, final_saham))
                
                heir_name = HEIR_NAMES.get(heir.heir_id, {}).get("id", "Unknown")
                notes.append(f"     • {heir_name}: {saham_radd} × {faktor_radd} = {final_saham}/{ashl_akhir}")
            
            return ashl_zauj, ashl_akhir, shares, notes
        
        else:
            # ===== INKISAR (TIDAK TERBAGI UTUH) =====
            notes.append(f"   d) Belum bisa terbagi utuh → INKISAR (Muqasamah)")
            
            # AM Akhir = total_saham_radd × ashl_zauj
            ashl_akhir = total_saham_radd * ashl_zauj
            notes.append(f"   {total_saham_radd} × {ashl_zauj} = {ashl_akhir}")
            
            # Zauj/Zaujah saham = zauj_numerator × total_saham_radd
            zauj_saham = zauj_numerator * total_saham_radd
            notes.append(f"   Zauj: {zauj_numerator} × {total_saham_radd} = {zauj_saham}/{ashl_akhir}")
            
            # Sisa untuk radd
            sisa_inkisar = ashl_akhir - zauj_saham
            notes.append(f"   Sisa untuk radd: {sisa_inkisar}")
            
            shares = [(spouse, zauj_saham)]
            
            # Distribusi sisa proporsional ke ahli waris radd
            for heir, saham_radd in radd_saham_list:
                # Formula: (saham_radd / total_saham_radd) × sisa
                final_saham = (saham_radd * sisa_inkisar) // total_saham_radd
                shares.append((heir, final_saham))
                
                heir_name = HEIR_NAMES.get(heir.heir_id, {}).get("id", "Unknown")
                notes.append(f"   {heir_name}: ({saham_radd}/{total_saham_radd}) × {sisa_inkisar} = {final_saham}/{ashl_akhir}")
            
            return ashl_zauj, ashl_akhir, shares, notes


