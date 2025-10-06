from __future__ import annotations

"""
Mas'alah Akdariyyah (المسألة الأكدرية)
Kasus: Zawj + Umm + Jadd + Ukht Kandung (tanpa anak/ayah)
"""

from typing import List
from app.schemas.calculation import CalculationResult, HeirShare
from app.schemas.heir import HeirInput, HeirResponse
from app.utils.constants import HeirID, HEIR_NAMES


def is_akdariyyah(heirs: List[HeirInput]) -> bool:
    """
    Cek apakah kasus Akdariyyah
    
    Syarat:
    - Ada Zawj (suami)
    - Ada Umm (ibu)
    - Ada Jadd (kakek)
    - Ada minimal 1 Ukht Kandung
    - Tidak ada anak/cucu
    - Tidak ada Abb (ayah)
    """
    heir_dict = {h.id: h.quantity for h in heirs}
    
    has_zawj = heir_dict.get(HeirID.ZAWJ, 0) > 0
    has_umm = heir_dict.get(HeirID.UMM, 0) > 0
    has_jadd = heir_dict.get(HeirID.JADD, 0) > 0
    has_ukht = heir_dict.get(HeirID.UKHT_ABAWAYN, 0) > 0
    
    has_abb = heir_dict.get(HeirID.ABB, 0) > 0
    has_kids = any(heir_dict.get(kid_id, 0) > 0 
                   for kid_id in [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN])
    
    return has_zawj and has_umm and has_jadd and has_ukht and not has_abb and not has_kids


def calculate_akdariyyah(heirs: List[HeirInput], tirkah: float, 
                        notes: List[str]) -> CalculationResult:
    """
    Hitung Akdariyyah
    
    Aturan:
    - Zawj: 1/2
    - Umm: 1/6 (dimodifikasi dari 1/3)
    - Jadd + Ukht: Muqasamah pada sisa dengan ratio 2:1
    """
    heir_dict = {h.id: h.quantity for h in heirs}
    num_ukht = heir_dict.get(HeirID.UKHT_ABAWAYN, 0)
    
    # Ratio muqasamah: Jadd=2, Ukht=1
    ratio_jadd = 2
    ratio_ukht = num_ukht
    ratio_total = ratio_jadd + ratio_ukht
    
    # Ashl al-Mas'alah Akdariyyah = 6 × ratio_total
    ashl = 6 * ratio_total
    
    # Hitung saham
    zawj_saham = (ashl * 1) // 2  # 1/2
    umm_saham = (ashl * 1) // 6   # 1/6
    sisa = ashl - zawj_saham - umm_saham
    
    jadd_saham = (sisa * ratio_jadd) // ratio_total
    ukht_saham_total = (sisa * ratio_ukht) // ratio_total
    ukht_saham_each = ukht_saham_total // num_ukht
    
    # Notes
    notes.append("📖 Mas'alah Akdariyyah")
    notes.append(f"   Ashl = 6 × {ratio_total} = {ashl}")
    notes.append(f"   Zawj: {zawj_saham}/{ashl} = 1/2")
    notes.append(f"   Umm: {umm_saham}/{ashl} = 1/6 (dimodifikasi)")
    notes.append(f"   Sisa: {sisa}/{ashl}")
    notes.append(f"   Muqasamah Jadd:Ukht = {ratio_jadd}:{ratio_ukht}")
    notes.append(f"   Jadd: {jadd_saham}/{ashl}")
    notes.append(f"   Ukht ({num_ukht} orang): {ukht_saham_total}/{ashl}")
    notes.append("")
    
    # Create shares
    shares = [
        HeirShare(
            heir=HeirResponse(id=HeirID.ZAWJ, **HEIR_NAMES[HeirID.ZAWJ]),
            quantity=1,
            fardh="1/2",
            share_fraction=f"{zawj_saham}/{ashl}",
            saham=float(zawj_saham),
            reason="Suami mendapat 1/2 (dalam Akdariyyah tetap 1/2)",
            share_amount=(zawj_saham / ashl) * tirkah,
            percentage=f"{(zawj_saham / ashl) * 100:.2f}%"
        ),
        HeirShare(
            heir=HeirResponse(id=HeirID.UMM, **HEIR_NAMES[HeirID.UMM]),
            quantity=1,
            fardh="1/6",
            share_fraction=f"{umm_saham}/{ashl}",
            saham=float(umm_saham),
            reason="Ibu mendapat 1/6 (dimodifikasi dari 1/3 dalam Akdariyyah)",
            share_amount=(umm_saham / ashl) * tirkah,
            percentage=f"{(umm_saham / ashl) * 100:.2f}%"
        ),
        HeirShare(
            heir=HeirResponse(id=HeirID.JADD, **HEIR_NAMES[HeirID.JADD]),
            quantity=1,
            fardh="Muqasamah",
            share_fraction=f"{jadd_saham}/{ashl}",
            saham=float(jadd_saham),
            reason=f"Kakek mendapat {ratio_jadd} bagian dari Muqasamah (ratio {ratio_jadd}:{ratio_ukht})",
            share_amount=(jadd_saham / ashl) * tirkah,
            percentage=f"{(jadd_saham / ashl) * 100:.2f}%"
        ),
        HeirShare(
            heir=HeirResponse(id=HeirID.UKHT_ABAWAYN, **HEIR_NAMES[HeirID.UKHT_ABAWAYN]),
            quantity=num_ukht,
            fardh="Muqasamah",
            share_fraction=f"{ukht_saham_each}/{ashl}",
            saham=float(ukht_saham_each),
            reason=f"Saudari Kandung mendapat 1 bagian dari Muqasamah (ratio {ratio_ukht}:{ratio_jadd}) dalam Akdariyyah",
            share_amount=(ukht_saham_each / ashl) * tirkah,
            percentage=f"{(ukht_saham_each / ashl) * 100:.2f}%",
            is_mahjub=False
        )
    ]
    
    return CalculationResult(
        tirkah=tirkah,
        ashlul_masalah_awal=ashl,
        ashlul_masalah_akhir=ashl,
        total_saham=float(ashl),
        status="Adil (Kasus Khusus: Akdariyyah)",
        is_special_case=True,
        special_case_name="Akdariyyah",
        shares=shares,
        notes=notes
    )
