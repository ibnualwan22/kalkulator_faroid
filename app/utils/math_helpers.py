"""
Math helper functions untuk perhitungan faraid
"""
from __future__ import annotations
from math import gcd
from typing import List, Tuple
from fractions import Fraction


def lcm(a: int, b: int) -> int:
    """
    Hitung Least Common Multiple (KPK) dari dua bilangan
    
    Args:
        a: Bilangan pertama
        b: Bilangan kedua
        
    Returns:
        KPK dari a dan b
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def lcm_multiple(numbers: List[int]) -> int:
    """
    Hitung LCM dari beberapa bilangan
    
    Args:
        numbers: List bilangan
        
    Returns:
        KPK dari semua bilangan
    """
    if not numbers:
        return 1
    
    result = numbers[0]
    for num in numbers[1:]:
        result = lcm(result, num)
    return result


def gcd_multiple(numbers: List[int]) -> int:
    """
    Hitung GCD dari beberapa bilangan
    
    Args:
        numbers: List bilangan
        
    Returns:
        FPB dari semua bilangan
    """
    if not numbers:
        return 1
    
    result = numbers[0]
    for num in numbers[1:]:
        result = gcd(result, num)
    return result


def simplify_fraction(numerator: int, denominator: int) -> Tuple[int, int]:
    """
    Sederhanakan pecahan
    
    Args:
        numerator: Pembilang
        denominator: Penyebut
        
    Returns:
        Tuple (pembilang, penyebut) yang sudah disederhanakan
    """
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")
    
    common_divisor = gcd(abs(numerator), abs(denominator))
    return (numerator // common_divisor, denominator // common_divisor)


def fraction_to_string(numerator: int, denominator: int) -> str:
    """
    Konversi pecahan ke string
    
    Args:
        numerator: Pembilang
        denominator: Penyebut
        
    Returns:
        String representasi pecahan (misal: "1/2")
    """
    if denominator == 1:
        return str(numerator)
    
    # Sederhanakan dulu
    num, den = simplify_fraction(numerator, denominator)
    return f"{num}/{den}"


def parse_fraction(fraction_str: str) -> Tuple[int, int]:
    """
    Parse string pecahan menjadi numerator dan denominator
    
    Args:
        fraction_str: String pecahan (misal: "1/2", "2/3")
        
    Returns:
        Tuple (numerator, denominator)
    """
    if '/' not in fraction_str:
        # Bukan pecahan, mungkin integer
        return (int(fraction_str), 1)
    
    parts = fraction_str.split('/')
    if len(parts) != 2:
        raise ValueError(f"Invalid fraction format: {fraction_str}")
    
    return (int(parts[0]), int(parts[1]))


def add_fractions(f1: Tuple[int, int], f2: Tuple[int, int]) -> Tuple[int, int]:
    """
    Tambahkan dua pecahan
    
    Args:
        f1: Pecahan pertama (numerator, denominator)
        f2: Pecahan kedua (numerator, denominator)
        
    Returns:
        Hasil penjumlahan (numerator, denominator)
    """
    num1, den1 = f1
    num2, den2 = f2
    
    # Cari KPK penyebut
    common_den = lcm(den1, den2)
    
    # Sesuaikan pembilang
    num1 = num1 * (common_den // den1)
    num2 = num2 * (common_den // den2)
    
    # Jumlahkan
    result_num = num1 + num2
    
    # Sederhanakan
    return simplify_fraction(result_num, common_den)


def compare_fractions(f1: Tuple[int, int], f2: Tuple[int, int]) -> int:
    """
    Bandingkan dua pecahan
    
    Args:
        f1: Pecahan pertama (numerator, denominator)
        f2: Pecahan kedua (numerator, denominator)
        
    Returns:
        -1 jika f1 < f2
         0 jika f1 == f2
         1 jika f1 > f2
    """
    num1, den1 = f1
    num2, den2 = f2
    
    # Kalikan silang
    cross1 = num1 * den2
    cross2 = num2 * den1
    
    if cross1 < cross2:
        return -1
    elif cross1 > cross2:
        return 1
    else:
        return 0


def distribute_shares(total: float, shares: List[int]) -> List[float]:
    """
    Distribusikan harta sesuai dengan saham
    
    Args:
        total: Total harta yang akan dibagi
        shares: List saham untuk masing-masing ahli waris
        
    Returns:
        List bagian dalam rupiah untuk masing-masing ahli waris
    """
    total_shares = sum(shares)
    if total_shares == 0:
        return [0.0] * len(shares)
    
    return [total * share / total_shares for share in shares]


def check_aul_valid(ashl: int, total_shares: int) -> bool:
    """
    Cek apakah terjadi 'Aul yang valid
    
    Args:
        ashl: Ashl al-mas'alah awal
        total_shares: Total saham dari dzawil furudh
        
    Returns:
        True jika terjadi 'Aul
    """
    from app.utils.constants import VALID_AUL
    
    if total_shares <= ashl:
        return False
    
    # Cek apakah ashl ada di tabel 'Aul
    if ashl not in VALID_AUL:
        return False
    
    # Cek apakah total_shares adalah nilai 'Aul yang valid
    return total_shares in VALID_AUL[ashl]


def calculate_aul(ashl: int, total_shares: int) -> int:
    """
    Hitung nilai 'Aul (ashl yang di-'aul-kan)
    
    Args:
        ashl: Ashl al-mas'alah awal
        total_shares: Total saham dari dzawil furudh
        
    Returns:
        Nilai ashl setelah 'Aul (sama dengan total_shares jika valid)
    """
    if check_aul_valid(ashl, total_shares):
        return total_shares
    return ashl


def calculate_radd_recipients(shares_dict: dict, dzawil_furudh_ids: List[int]) -> List[int]:
    """
    Tentukan siapa yang berhak menerima Radd
    
    Radd diberikan kepada dzawil furudh kecuali suami/istri
    
    Args:
        shares_dict: Dictionary {heir_id: share_count}
        dzawil_furudh_ids: List ID dzawil furudh yang ada
        
    Returns:
        List ID ahli waris yang berhak menerima Radd
    """
    from app.utils.constants import HeirID
    
    # Suami dan istri tidak mendapat Radd
    excluded = {HeirID.ZAWJ, HeirID.ZAWJAH}
    
    return [hid for hid in dzawil_furudh_ids if hid not in excluded]
