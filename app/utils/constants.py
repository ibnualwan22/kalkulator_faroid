"""
Konstanta untuk Kalkulator Faroid
Berdasarkan Kitab Zahrotul Faridhah dan Rumus Faroidh
"""

from enum import IntEnum
from typing import Dict, List


class HeirID(IntEnum):
    """ID Ahli Waris"""
    # Laki-laki
    IBN = 1                    # Anak laki-laki
    ABB = 2                    # Ayah
    ZAWJ = 3                   # Suami
    ZAWJAH = 4                 # Istri
    IBN_IBN = 5                # Cucu laki-laki (dari anak laki-laki)
    JADD = 6                   # Kakek (dari ayah)
    AKH_ABAWAYN = 7            # Saudara laki-laki kandung
    AKH_AB = 8                 # Saudara laki-laki seayah
    AKH_UMM = 9                # Saudara laki-laki seibu
    IBN_AKH_ABAWAYN = 10       # Keponakan laki-laki (dari sdr lk kandung)
    IBN_AKH_AB = 11            # Keponakan laki-laki (dari sdr lk seayah)
    AMM_ABAWAYN = 12           # Paman kandung
    AMM_AB = 13                # Paman seayah
    IBN_AMM_ABAWAYN = 14       # Sepupu laki-laki (dari paman kandung)
    IBN_AMM_AB = 15            # Sepupu laki-laki (dari paman seayah)
    
    # Perempuan
    BINT = 16                  # Anak perempuan
    BINT_IBN = 17              # Cucu perempuan (dari anak laki-laki)
    UMM = 18                   # Ibu
    JADDAH_UMM = 19            # Nenek dari ibu
    JADDAH_ABB = 20            # Nenek dari ayah
    UKHT_ABAWAYN = 21          # Saudari kandung
    UKHT_AB = 22               # Saudari seayah
    UKHT_UMM = 23              # Saudari seibu
    
    # Pembebas budak (jarang digunakan)
    MUTIQ = 24                 # Laki-laki pembebas budak
    MUTIQAH = 25               # Perempuan pembebas budak


# Nama ahli waris dalam bahasa Indonesia dan Arab
HEIR_NAMES = {
    HeirID.IBN: {"id": "Anak Laki-laki", "ar": "ابن"},
    HeirID.ABB: {"id": "Ayah", "ar": "أب"},
    HeirID.ZAWJ: {"id": "Suami", "ar": "زوج"},
    HeirID.ZAWJAH: {"id": "Istri", "ar": "زوجة"},
    HeirID.IBN_IBN: {"id": "Cucu Laki-laki", "ar": "ابن ابن"},
    HeirID.JADD: {"id": "Kakek", "ar": "جد"},
    HeirID.AKH_ABAWAYN: {"id": "Saudara Laki-laki Kandung", "ar": "أخ لأبوين"},
    HeirID.AKH_AB: {"id": "Saudara Laki-laki Seayah", "ar": "أخ لأب"},
    HeirID.AKH_UMM: {"id": "Saudara Laki-laki Seibu", "ar": "أخ لأم"},
    HeirID.IBN_AKH_ABAWAYN: {"id": "Keponakan Laki-laki (dari Sdr Lk Kandung)", "ar": "ابن أخ لأبوين"},
    HeirID.IBN_AKH_AB: {"id": "Keponakan Laki-laki (dari Sdr Lk Seayah)", "ar": "ابن أخ لأب"},
    HeirID.AMM_ABAWAYN: {"id": "Paman Kandung", "ar": "عم لأبوين"},
    HeirID.AMM_AB: {"id": "Paman Seayah", "ar": "عم لأب"},
    HeirID.IBN_AMM_ABAWAYN: {"id": "Sepupu Laki-laki (dari Paman Kandung)", "ar": "ابن عم لأبوين"},
    HeirID.IBN_AMM_AB: {"id": "Sepupu Laki-laki (dari Paman Seayah)", "ar": "ابن عم لأب"},
    HeirID.BINT: {"id": "Anak Perempuan", "ar": "بنت"},
    HeirID.BINT_IBN: {"id": "Cucu Perempuan", "ar": "بنت ابن"},
    HeirID.UMM: {"id": "Ibu", "ar": "أم"},
    HeirID.JADDAH_UMM: {"id": "Nenek dari Ibu", "ar": "جدة من الأم"},
    HeirID.JADDAH_ABB: {"id": "Nenek dari Ayah", "ar": "جدة من الأب"},
    HeirID.UKHT_ABAWAYN: {"id": "Saudari Kandung", "ar": "أخت لأبوين"},
    HeirID.UKHT_AB: {"id": "Saudari Seayah", "ar": "أخت لأب"},
    HeirID.UKHT_UMM: {"id": "Saudari Seibu", "ar": "أخت لأم"},
    HeirID.MUTIQ: {"id": "Pria Pembebas Budak", "ar": "معتق"},
    HeirID.MUTIQAH: {"id": "Wanita Pembebas Budak", "ar": "معتقة"},
}


# =============================================================================
# RUMUS FURUDH LENGKAP DENGAN ALASAN (BAHASA INDONESIA)
# Berdasarkan Kitab Zahrotul Faridhah
# =============================================================================

FURUDH_RULES = {
    # =========================================================================
    # SUAMI (ZAWJ)
    # =========================================================================
    HeirID.ZAWJ: [
        {
            "fardh": "1/2",
            "kondisi": "Tidak ada anak atau cucu dari anak laki-laki",
            "alasan": "Suami mendapat 1/2 (setengah) karena pewaris tidak memiliki anak (baik laki-laki maupun perempuan) dan tidak memiliki cucu dari anak laki-laki. Dasar hukum: QS. An-Nisa ayat 12.",
            "syarat_tidak_ada": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN]
        },
        {
            "fardh": "1/4",
            "kondisi": "Ada anak atau cucu dari anak laki-laki",
            "alasan": "Suami mendapat 1/4 (seperempat) karena pewaris memiliki anak (baik laki-laki maupun perempuan) atau cucu dari anak laki-laki. Dasar hukum: QS. An-Nisa ayat 12.",
            "syarat_ada": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN]
        }
    ],
    
    # =========================================================================
    # ISTRI (ZAWJAH)
    # =========================================================================
    HeirID.ZAWJAH: [
        {
            "fardh": "1/4",
            "kondisi": "Tidak ada anak atau cucu dari anak laki-laki",
            "alasan": "Istri mendapat 1/4 (seperempat) karena pewaris tidak memiliki anak (baik laki-laki maupun perempuan) dan tidak memiliki cucu dari anak laki-laki. Jika istri lebih dari satu, bagian 1/4 dibagi rata. Dasar hukum: QS. An-Nisa ayat 12.",
            "syarat_tidak_ada": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN]
        },
        {
            "fardh": "1/8",
            "kondisi": "Ada anak atau cucu dari anak laki-laki",
            "alasan": "Istri mendapat 1/8 (seperdelapan) karena pewaris memiliki anak (baik laki-laki maupun perempuan) atau cucu dari anak laki-laki. Jika istri lebih dari satu, bagian 1/8 dibagi rata. Dasar hukum: QS. An-Nisa ayat 12.",
            "syarat_ada": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN]
        }
    ],
    
    # =========================================================================
    # IBU (UMM)
    # =========================================================================
    HeirID.UMM: [
        {
            "fardh": "1/6",
            "kondisi": "Ada anak, cucu, atau lebih dari satu saudara",
            "alasan": "Ibu mendapat 1/6 (seperenam) karena pewaris memiliki anak (laki-laki atau perempuan), cucu dari anak laki-laki, atau memiliki dua orang saudara atau lebih (baik laki-laki maupun perempuan, kandung, seayah, atau seibu). Dasar hukum: QS. An-Nisa ayat 11.",
            "syarat_ada": [
                HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN,
                HeirID.AKH_ABAWAYN, HeirID.AKH_AB, HeirID.AKH_UMM,
                HeirID.UKHT_ABAWAYN, HeirID.UKHT_AB, HeirID.UKHT_UMM
            ],
            "min_saudara": 2
        },
        {
            "fardh": "1/3",
            "kondisi": "Tidak ada anak, cucu, dan saudara < 2 orang",
            "alasan": "Ibu mendapat 1/3 (sepertiga) karena pewaris tidak memiliki anak, tidak memiliki cucu dari anak laki-laki, dan tidak memiliki dua orang saudara atau lebih. Dasar hukum: QS. An-Nisa ayat 11.",
            "syarat_tidak_ada": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN],
            "max_saudara": 1
        },
        {
            "fardh": "1/3 sisa",
            "kondisi": "Umariyyatan (hanya suami/istri, ayah, dan ibu)",
            "alasan": "Ibu mendapat 1/3 dari sisa harta setelah bagian suami/istri dalam kasus Umariyyatan. Kasus ini terjadi ketika ahli waris hanya terdiri dari: (1) Suami, Ayah, dan Ibu; atau (2) Istri, Ayah, dan Ibu. Ibu mendapat 1/3 dari sisa setelah suami/istri mengambil bagiannya. Ini berdasarkan ijtihad Umar bin Khattab RA.",
            "kasus_khusus": "umariyyatan"
        }
    ],
    
    # =========================================================================
    # AYAH (ABB)
    # =========================================================================
    HeirID.ABB: [
        {
            "fardh": "1/6",
            "kondisi": "Ada anak laki-laki atau cucu laki-laki",
            "alasan": "Ayah mendapat 1/6 (seperenam) sebagai bagian fardh karena pewaris memiliki anak laki-laki atau cucu laki-laki dari anak laki-laki. Dalam kondisi ini, ayah tidak mengambil sisa sebagai ashobah. Dasar hukum: QS. An-Nisa ayat 11.",
            "syarat_ada": [HeirID.IBN, HeirID.IBN_IBN]
        },
        {
            "fardh": "1/6 + Ashobah",
            "kondisi": "Ada anak perempuan atau cucu perempuan (tanpa anak/cucu laki-laki)",
            "alasan": "Ayah mendapat 1/6 (seperenam) sebagai fardh, dan sisa harta sebagai ashobah bil-ghair (bersama dengan anak/cucu perempuan). Kondisi ini terjadi ketika pewaris hanya memiliki anak perempuan atau cucu perempuan tanpa ada anak laki-laki atau cucu laki-laki. Dasar hukum: QS. An-Nisa ayat 11.",
            "syarat_ada": [HeirID.BINT, HeirID.BINT_IBN],
            "syarat_tidak_ada": [HeirID.IBN, HeirID.IBN_IBN]
        },
        {
            "fardh": "Ashobah",
            "kondisi": "Tidak ada anak atau cucu sama sekali",
            "alasan": "Ayah mendapat seluruh sisa harta sebagai ashobah binafsih ketika pewaris tidak memiliki anak atau cucu sama sekali (baik laki-laki maupun perempuan). Ayah menjadi ahli waris utama yang berhak atas semua sisa setelah dzawil furudh lain mengambil bagiannya.",
            "syarat_tidak_ada": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN]
        }
    ],
    
    # =========================================================================
    # KAKEK (JADD)
    # =========================================================================
    HeirID.JADD: [
        {
            "fardh": "Seperti Ayah",
            "kondisi": "Tidak ada ayah",
            "alasan": "Kakek menggantikan posisi ayah dan mendapat bagian yang sama dengan ayah jika ayah tidak ada. Kakek memiliki tiga kemungkinan bagian: (1) 1/6 jika ada anak/cucu laki-laki; (2) 1/6 + Ashobah jika ada anak/cucu perempuan tanpa laki-laki; (3) Ashobah penuh jika tidak ada anak/cucu. Dalam kasus Jadd ma'al-Ikhwah (kakek bersama saudara), kakek memilih opsi terbaik: muqasamah, 1/3, atau 1/6.",
            "syarat_tidak_ada": [HeirID.ABB],
            "catatan": "Lihat aturan Jadd ma'al-Ikhwah untuk kasus kakek bersama saudara"
        }
    ],
    
    # =========================================================================
    # ANAK LAKI-LAKI (IBN)
    # =========================================================================
    HeirID.IBN: [
        {
            "fardh": "Ashobah binafsih",
            "kondisi": "Selalu mendapat sisa sebagai ashobah",
            "alasan": "Anak laki-laki adalah ashobah binafsih (ashobah dengan dirinya sendiri) dan mendapat seluruh sisa harta setelah dzawil furudh mengambil bagiannya. Jika bersama anak perempuan, pembagian dengan rasio 2:1 (anak laki-laki mendapat dua kali lipat anak perempuan). Dasar hukum: QS. An-Nisa ayat 11.",
            "ratio": "2:1 dengan anak perempuan"
        }
    ],
    
    # =========================================================================
    # ANAK PEREMPUAN (BINT)
    # =========================================================================
    HeirID.BINT: [
        {
            "fardh": "1/2",
            "kondisi": "Satu anak perempuan tanpa anak laki-laki",
            "alasan": "Anak perempuan tunggal mendapat 1/2 (setengah) ketika tidak ada anak laki-laki yang dapat menjadikannya ashobah bil-ghair. Dasar hukum: QS. An-Nisa ayat 11.",
            "jumlah": 1,
            "syarat_tidak_ada": [HeirID.IBN]
        },
        {
            "fardh": "2/3",
            "kondisi": "Dua atau lebih anak perempuan tanpa anak laki-laki",
            "alasan": "Dua anak perempuan atau lebih mendapat 2/3 (dua pertiga) untuk dibagi rata di antara mereka ketika tidak ada anak laki-laki. Dasar hukum: QS. An-Nisa ayat 11.",
            "jumlah_min": 2,
            "syarat_tidak_ada": [HeirID.IBN]
        },
        {
            "fardh": "Ashobah bil-ghair",
            "kondisi": "Ada anak laki-laki",
            "alasan": "Anak perempuan menjadi ashobah bil-ghair (ashobah dengan sebab orang lain) ketika bersama dengan anak laki-laki. Pembagian antara anak laki-laki dan perempuan dengan perbandingan 2:1 (anak laki-laki mendapat dua kali lipat anak perempuan). Dasar hukum: QS. An-Nisa ayat 11: 'Lilldzakari mitslu hadzhil untsayain' (bagi anak laki-laki bagian dua anak perempuan).",
            "syarat_ada": [HeirID.IBN],
            "ratio": "2:1"
        }
    ],
    
    # =========================================================================
    # CUCU LAKI-LAKI (IBN IBN)
    # =========================================================================
    HeirID.IBN_IBN: [
        {
            "fardh": "Ashobah binafsih",
            "kondisi": "Tidak ada anak laki-laki",
            "alasan": "Cucu laki-laki dari anak laki-laki adalah ashobah binafsih yang menggantikan posisi anak laki-laki jika anak laki-laki tidak ada. Mendapat seluruh sisa harta setelah dzawil furudh. Jika bersama cucu perempuan sederajat, pembagian 2:1. Dasar hukum: Analogi dengan anak laki-laki (QS. An-Nisa ayat 11).",
            "syarat_tidak_ada": [HeirID.IBN],
            "ratio": "2:1 dengan cucu perempuan"
        },
        {
            "fardh": "Mahjub",
            "kondisi": "Ada anak laki-laki yang lebih tinggi",
            "alasan": "Cucu laki-laki terhalang (mahjub) oleh anak laki-laki. Namun dapat menjadi ashobah jika bersama anak perempuan tunggal untuk melengkapi bagiannya.",
            "syarat_mahjub": [HeirID.IBN]
        }
    ],
    
    # =========================================================================
    # CUCU PEREMPUAN (BINT IBN)
    # =========================================================================
    HeirID.BINT_IBN: [
        {
            "fardh": "1/2",
            "kondisi": "Satu cucu perempuan tanpa anak dan cucu laki-laki",
            "alasan": "Cucu perempuan tunggal dari anak laki-laki mendapat 1/2 (setengah) ketika tidak ada anak (laki-laki atau perempuan) dan tidak ada cucu laki-laki yang sederajat atau lebih tinggi. Posisinya menggantikan anak perempuan. Dasar hukum: QS. An-Nisa ayat 11 (analogi dengan anak perempuan).",
            "jumlah": 1,
            "syarat_tidak_ada": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN]
        },
        {
            "fardh": "2/3",
            "kondisi": "Dua atau lebih cucu perempuan tanpa anak dan cucu laki-laki",
            "alasan": "Dua cucu perempuan atau lebih dari anak laki-laki mendapat 2/3 (dua pertiga) untuk dibagi rata ketika tidak ada anak dan tidak ada cucu laki-laki yang sederajat atau lebih tinggi. Dasar hukum: Analogi dengan anak perempuan (QS. An-Nisa ayat 11).",
            "jumlah_min": 2,
            "syarat_tidak_ada": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN]
        },
        {
            "fardh": "1/6",
            "kondisi": "Ada satu anak perempuan (sebagai ta'shib/pelengkap)",
            "alasan": "Cucu perempuan mendapat 1/6 (seperenam) sebagai pelengkap (ta'shib) ketika bersama dengan satu anak perempuan. Bagian anak perempuan 1/2 ditambah bagian cucu perempuan 1/6 menjadi total 2/3. Ini berdasarkan hadits tentang pembagian untuk anak dan cucu perempuan.",
            "syarat_ada": [HeirID.BINT],
            "jumlah_bint": 1,
            "syarat_tidak_ada": [HeirID.IBN, HeirID.IBN_IBN]
        },
        {
            "fardh": "Ashobah bil-ghair",
            "kondisi": "Ada cucu laki-laki sederajat",
            "alasan": "Cucu perempuan menjadi ashobah bil-ghair (ashobah dengan sebab orang lain) ketika bersama dengan cucu laki-laki yang sederajat atau lebih rendah. Pembagian 2:1 seperti anak laki-laki dan perempuan. Dasar hukum: Analogi dengan anak (QS. An-Nisa ayat 11).",
            "syarat_ada": [HeirID.IBN_IBN],
            "ratio": "2:1"
        },
        {
            "fardh": "Mahjub",
            "kondisi": "Ada anak laki-laki atau dua anak perempuan tanpa pelengkap",
            "alasan": "Cucu perempuan terhalang (mahjub) oleh keberadaan anak laki-laki, atau oleh dua anak perempuan atau lebih ketika tidak ada cucu laki-laki yang dapat menjadikannya ashobah.",
            "syarat_mahjub": [HeirID.IBN, HeirID.BINT]
        }
    ],
    
    # =========================================================================
    # NENEK (JADDAH)
    # =========================================================================
    HeirID.JADDAH_UMM: [
        {
            "fardh": "1/6",
            "kondisi": "Tidak ada ibu dan tidak ada nenek yang lebih dekat",
            "alasan": "Nenek dari pihak ibu mendapat 1/6 (seperenam) ketika tidak ada ibu kandung dan tidak ada nenek lain yang lebih dekat kepada pewaris. Jika ada beberapa nenek yang sama derajatnya, bagian 1/6 dibagi rata. Dasar hukum: Hadits Nabi SAW tentang bagian nenek.",
            "syarat_tidak_ada": [HeirID.UMM]
        }
    ],
    
    HeirID.JADDAH_ABB: [
        {
            "fardh": "1/6",
            "kondisi": "Tidak ada ibu dan tidak ada ayah yang menghalangi",
            "alasan": "Nenek dari pihak ayah mendapat 1/6 (seperenam) ketika tidak ada ibu kandung. Nenek dari ayah terhalang oleh ayah kandung jika ayah masih hidup. Jika ada beberapa nenek yang sama derajatnya, bagian 1/6 dibagi rata. Dasar hukum: Hadits Nabi SAW tentang bagian nenek.",
            "syarat_tidak_ada": [HeirID.UMM],
            "catatan": "Terhalang oleh ayah jika ayah ada"
        }
    ],
    
    # =========================================================================
    # SAUDARI KANDUNG (UKHT ABAWAYN)
    # =========================================================================
    HeirID.UKHT_ABAWAYN: [
        {
            "fardh": "1/2",
            "kondisi": "Satu saudari kandung tanpa ashib",
            "alasan": "Saudari kandung tunggal mendapat 1/2 (setengah) ketika tidak ada anak, cucu, ayah, kakek, saudara laki-laki kandung, dan tidak ada ashib yang menjadikannya ashobah. Dasar hukum: QS. An-Nisa ayat 176.",
            "jumlah": 1,
            "syarat_tidak_ada": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN]
        },
        {
            "fardh": "2/3",
            "kondisi": "Dua atau lebih saudari kandung tanpa ashib",
            "alasan": "Dua saudari kandung atau lebih mendapat 2/3 (dua pertiga) untuk dibagi rata ketika tidak ada anak, cucu, ayah, kakek, dan saudara laki-laki kandung. Dasar hukum: QS. An-Nisa ayat 176.",
            "jumlah_min": 2,
            "syarat_tidak_ada": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN]
        },
        {
            "fardh": "Ashobah bil-ghair",
            "kondisi": "Ada saudara laki-laki kandung",
            "alasan": "Saudari kandung menjadi ashobah bil-ghair (ashobah dengan sebab orang lain) ketika bersama saudara laki-laki kandung. Pembagian 2:1 (saudara laki-laki mendapat dua kali lipat saudari). Dasar hukum: QS. An-Nisa ayat 176.",
            "syarat_ada": [HeirID.AKH_ABAWAYN],
            "ratio": "2:1"
        },
        {
            "fardh": "Ashobah ma'al-ghair",
            "kondisi": "Ada anak/cucu perempuan",
            "alasan": "Saudari kandung menjadi ashobah ma'al-ghair (ashobah bersama orang lain) ketika bersama dengan anak perempuan atau cucu perempuan dari anak laki-laki. Saudari kandung mengambil sisa harta setelah anak/cucu perempuan. Dasar hukum: Ijtihad sahabat berdasarkan kemaslahatan.",
            "syarat_ada": [HeirID.BINT, HeirID.BINT_IBN],
            "syarat_tidak_ada": [HeirID.IBN, HeirID.IBN_IBN, HeirID.AKH_ABAWAYN]
        },
        {
            "fardh": "Mahjub",
            "kondisi": "Ada anak laki-laki, cucu laki-laki, ayah, atau kakek (dalam beberapa kondisi)",
            "alasan": "Saudari kandung terhalang (mahjub) oleh anak laki-laki, cucu laki-laki dari anak laki-laki, atau ayah. Kakek menghalangi dalam kondisi tertentu (lihat aturan Jadd ma'al-Ikhwah dan Akdariyyah).",
            "syarat_mahjub": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB]
        }
    ],
    
    # =========================================================================
    # SAUDARI SEAYAH (UKHT AB)
    # =========================================================================
    HeirID.UKHT_AB: [
        {
            "fardh": "1/2",
            "kondisi": "Satu saudari seayah tanpa saudara kandung dan ashib",
            "alasan": "Saudari seayah tunggal mendapat 1/2 (setengah) ketika tidak ada saudara kandung (laki-laki atau perempuan), tidak ada anak, cucu, ayah, dan ashib lainnya. Posisinya seperti saudari kandung. Dasar hukum: QS. An-Nisa ayat 176 (analogi).",
            "jumlah": 1,
            "syarat_tidak_ada": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN, HeirID.UKHT_ABAWAYN, HeirID.AKH_AB]
        },
        {
            "fardh": "2/3",
            "kondisi": "Dua atau lebih saudari seayah tanpa saudara kandung",
            "alasan": "Dua saudari seayah atau lebih mendapat 2/3 (dua pertiga) untuk dibagi rata ketika tidak ada saudara kandung dan ashib yang menghalangi. Dasar hukum: Analogi dengan saudari kandung.",
            "jumlah_min": 2,
            "syarat_tidak_ada": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN, HeirID.UKHT_ABAWAYN, HeirID.AKH_AB]
        },
        {
            "fardh": "1/6",
            "kondisi": "Ada satu saudari kandung (sebagai pelengkap)",
            "alasan": "Saudari seayah mendapat 1/6 (seperenam) sebagai pelengkap ketika ada satu saudari kandung. Bagian saudari kandung 1/2 ditambah saudari seayah 1/6 menjadi total 2/3. Analogi dengan cucu perempuan yang melengkapi anak perempuan.",
            "syarat_ada": [HeirID.UKHT_ABAWAYN],
            "jumlah_ukht_kandung": 1,
            "syarat_tidak_ada": [HeirID.AKH_ABAWAYN, HeirID.AKH_AB]
        },
        {
            "fardh": "Ashobah bil-ghair",
            "kondisi": "Ada saudara laki-laki seayah",
            "alasan": "Saudari seayah menjadi ashobah bil-ghair ketika bersama saudara laki-laki seayah. Pembagian 2:1. Dasar hukum: Analogi dengan saudara kandung.",
            "syarat_ada": [HeirID.AKH_AB],
            "ratio": "2:1"
        },
        {
            "fardh": "Ashobah ma'al-ghair",
            "kondisi": "Ada anak/cucu perempuan tanpa saudara kandung",
            "alasan": "Saudari seayah menjadi ashobah ma'al-ghair ketika bersama anak/cucu perempuan, dengan syarat tidak ada saudara kandung. Mengambil sisa setelah dzawil furudh.",
            "syarat_ada": [HeirID.BINT, HeirID.BINT_IBN],
            "syarat_tidak_ada": [HeirID.IBN, HeirID.IBN_IBN, HeirID.AKH_ABAWAYN, HeirID.UKHT_ABAWAYN]
        },
        {
            "fardh": "Mahjub",
            "kondisi": "Ada anak laki-laki, cucu laki-laki, ayah, dua saudari kandung, atau saudara kandung",
            "alasan": "Saudari seayah terhalang oleh anak laki-laki, cucu laki-laki, ayah, atau dua saudari kandung atau lebih (tanpa ashib yang menjadikannya ashobah).",
            "syarat_mahjub": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.AKH_ABAWAYN]
        }
    ],
    
    # =========================================================================
    # SAUDARA/I SEIBU (AKH/UKHT UMM)
    # =========================================================================
    HeirID.AKH_UMM: [
        {
            "fardh": "1/6",
            "kondisi": "Satu saudara/i seibu",
            "alasan": "Saudara atau saudari seibu tunggal (laki-laki atau perempuan sama) mendapat 1/6 (seperenam) ketika tidak ada anak, cucu, ayah, atau kakek. Saudara seibu laki-laki dan perempuan mendapat bagian yang sama. Dasar hukum: QS. An-Nisa ayat 12.",
            "jumlah": 1,
            "syarat_tidak_ada": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN, HeirID.ABB, HeirID.JADD]
        },
        {
            "fardh": "1/3",
            "kondisi": "Dua atau lebih saudara/i seibu",
            "alasan": "Dua saudara/i seibu atau lebih mendapat 1/3 (sepertiga) untuk dibagi rata, tanpa membedakan laki-laki dan perempuan. Dasar hukum: QS. An-Nisa ayat 12.",
            "jumlah_min": 2,
            "syarat_tidak_ada": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN, HeirID.ABB, HeirID.JADD]
        },
        {
            "fardh": "Mahjub",
            "kondisi": "Ada anak, cucu, ayah, atau kakek",
            "alasan": "Saudara/i seibu terhalang (mahjub) oleh anak (laki-laki atau perempuan), cucu dari anak laki-laki, ayah, atau kakek. Mereka tidak mendapat bagian sama sekali.",
            "syarat_mahjub": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN, HeirID.ABB, HeirID.JADD]
        }
    ],
    
    HeirID.UKHT_UMM: [
        {
            "fardh": "1/6",
            "kondisi": "Satu saudara/i seibu",
            "alasan": "Saudara atau saudari seibu tunggal (laki-laki atau perempuan sama) mendapat 1/6 (seperenam) ketika tidak ada anak, cucu, ayah, atau kakek. Saudara seibu laki-laki dan perempuan mendapat bagian yang sama. Dasar hukum: QS. An-Nisa ayat 12.",
            "jumlah": 1,
            "syarat_tidak_ada": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN, HeirID.ABB, HeirID.JADD]
        },
        {
            "fardh": "1/3",
            "kondisi": "Dua atau lebih saudara/i seibu",
            "alasan": "Dua saudara/i seibu atau lebih mendapat 1/3 (sepertiga) untuk dibagi rata, tanpa membedakan laki-laki dan perempuan. Dasar hukum: QS. An-Nisa ayat 12.",
            "jumlah_min": 2,
            "syarat_tidak_ada": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN, HeirID.ABB, HeirID.JADD]
        },
        {
            "fardh": "Mahjub",
            "kondisi": "Ada anak, cucu, ayah, atau kakek",
            "alasan": "Saudara/i seibu terhalang (mahjub) oleh anak (laki-laki atau perempuan), cucu dari anak laki-laki, ayah, atau kakek. Mereka tidak mendapat bagian sama sekali.",
            "syarat_mahjub": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN, HeirID.ABB, HeirID.JADD]
        }
    ],
    
    # =========================================================================
    # SAUDARA LAKI-LAKI KANDUNG (AKH ABAWAYN)
    # =========================================================================
    HeirID.AKH_ABAWAYN: [
        {
            "fardh": "Ashobah binafsih",
            "kondisi": "Tidak ada anak, cucu, ayah",
            "alasan": "Saudara laki-laki kandung adalah ashobah binafsih yang mendapat sisa harta ketika tidak ada anak (laki-laki/perempuan), cucu dari anak laki-laki, dan ayah. Jika bersama saudari kandung, pembagian 2:1. Dasar hukum: QS. An-Nisa ayat 176.",
            "syarat_tidak_ada": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN, HeirID.ABB],
            "ratio": "2:1 dengan saudari kandung"
        },
        {
            "fardh": "Mahjub",
            "kondisi": "Ada anak laki-laki, cucu laki-laki, atau ayah",
            "alasan": "Saudara laki-laki kandung terhalang oleh anak laki-laki, cucu laki-laki dari anak laki-laki, atau ayah. Dengan kakek, ada aturan khusus Jadd ma'al-Ikhwah.",
            "syarat_mahjub": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB]
        }
    ],
    
    # =========================================================================
    # SAUDARA LAKI-LAKI SEAYAH (AKH AB)
    # =========================================================================
    HeirID.AKH_AB: [
        {
            "fardh": "Ashobah binafsih",
            "kondisi": "Tidak ada anak, cucu, ayah, dan saudara kandung",
            "alasan": "Saudara laki-laki seayah adalah ashobah binafsih yang mendapat sisa harta ketika tidak ada penghalang. Posisinya di bawah saudara kandung. Jika bersama saudari seayah, pembagian 2:1. Dasar hukum: Analogi dengan saudara kandung.",
            "syarat_tidak_ada": [HeirID.IBN, HeirID.BINT, HeirID.IBN_IBN, HeirID.BINT_IBN, HeirID.ABB, HeirID.AKH_ABAWAYN, HeirID.UKHT_ABAWAYN],
            "ratio": "2:1 dengan saudari seayah"
        },
        {
            "fardh": "Mahjub",
            "kondisi": "Ada anak laki-laki, cucu laki-laki, ayah, atau saudara kandung",
            "alasan": "Saudara laki-laki seayah terhalang oleh anak laki-laki, cucu laki-laki, ayah, atau saudara laki-laki kandung.",
            "syarat_mahjub": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.AKH_ABAWAYN]
        }
    ],
    
    # =========================================================================
    # KEPONAKAN LAKI-LAKI DARI SAUDARA KANDUNG (IBN AKH ABAWAYN)
    # =========================================================================
    HeirID.IBN_AKH_ABAWAYN: [
        {
            "fardh": "Ashobah binafsih",
            "kondisi": "Tidak ada penghalang yang lebih tinggi",
            "alasan": "Keponakan laki-laki dari saudara kandung adalah ashobah binafsih urutan ke-7. Mendapat sisa harta jika tidak ada ahli waris yang lebih tinggi urutannya. Dasar hukum: Kaidah ashobah binafsih berdasarkan kedekatan nasab.",
            "syarat_tidak_ada": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN, HeirID.AKH_AB]
        },
        {
            "fardh": "Mahjub",
            "kondisi": "Ada ahli waris ashobah yang lebih tinggi",
            "alasan": "Terhalang oleh: anak laki-laki, cucu laki-laki, ayah, kakek, saudara kandung, atau saudara seayah.",
            "syarat_mahjub": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN, HeirID.AKH_AB]
        }
    ],
    
    # =========================================================================
    # KEPONAKAN LAKI-LAKI DARI SAUDARA SEAYAH (IBN AKH AB)
    # =========================================================================
    HeirID.IBN_AKH_AB: [
        {
            "fardh": "Ashobah binafsih",
            "kondisi": "Tidak ada penghalang yang lebih tinggi",
            "alasan": "Keponakan laki-laki dari saudara seayah adalah ashobah binafsih urutan ke-8. Mendapat sisa harta jika tidak ada ahli waris yang lebih tinggi urutannya. Dasar hukum: Kaidah ashobah binafsih berdasarkan kedekatan nasab.",
            "syarat_tidak_ada": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN, HeirID.AKH_AB, HeirID.IBN_AKH_ABAWAYN]
        },
        {
            "fardh": "Mahjub",
            "kondisi": "Ada ahli waris ashobah yang lebih tinggi",
            "alasan": "Terhalang oleh semua ashobah yang lebih tinggi termasuk keponakan dari saudara kandung.",
            "syarat_mahjub": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN, HeirID.AKH_AB, HeirID.IBN_AKH_ABAWAYN]
        }
    ],
    
    # =========================================================================
    # PAMAN KANDUNG (AMM ABAWAYN)
    # =========================================================================
    HeirID.AMM_ABAWAYN: [
        {
            "fardh": "Ashobah binafsih",
            "kondisi": "Tidak ada penghalang yang lebih tinggi",
            "alasan": "Paman kandung (saudara kandung ayah) adalah ashobah binafsih urutan ke-9. Mendapat sisa harta jika tidak ada ahli waris yang lebih tinggi urutannya. Dasar hukum: Kaidah ashobah binafsih berdasarkan kedekatan nasab.",
            "syarat_tidak_ada": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN, HeirID.AKH_AB, HeirID.IBN_AKH_ABAWAYN, HeirID.IBN_AKH_AB]
        },
        {
            "fardh": "Mahjub",
            "kondisi": "Ada ahli waris ashobah yang lebih tinggi",
            "alasan": "Terhalang oleh semua ashobah yang lebih tinggi sampai urutan ke-8.",
            "syarat_mahjub": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN, HeirID.AKH_AB, HeirID.IBN_AKH_ABAWAYN, HeirID.IBN_AKH_AB]
        }
    ],
    
    # =========================================================================
    # PAMAN SEAYAH (AMM AB)
    # =========================================================================
    HeirID.AMM_AB: [
        {
            "fardh": "Ashobah binafsih",
            "kondisi": "Tidak ada penghalang yang lebih tinggi",
            "alasan": "Paman seayah (saudara seayah dari ayah) adalah ashobah binafsih urutan ke-10. Mendapat sisa harta jika tidak ada ahli waris yang lebih tinggi urutannya. Dasar hukum: Kaidah ashobah binafsih berdasarkan kedekatan nasab.",
            "syarat_tidak_ada": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN, HeirID.AKH_AB, HeirID.IBN_AKH_ABAWAYN, HeirID.IBN_AKH_AB, HeirID.AMM_ABAWAYN]
        },
        {
            "fardh": "Mahjub",
            "kondisi": "Ada ahli waris ashobah yang lebih tinggi",
            "alasan": "Terhalang oleh semua ashobah yang lebih tinggi termasuk paman kandung.",
            "syarat_mahjub": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN, HeirID.AKH_AB, HeirID.IBN_AKH_ABAWAYN, HeirID.IBN_AKH_AB, HeirID.AMM_ABAWAYN]
        }
    ],
    
    # =========================================================================
    # SEPUPU LAKI-LAKI DARI PAMAN KANDUNG (IBN AMM ABAWAYN)
    # =========================================================================
    HeirID.IBN_AMM_ABAWAYN: [
        {
            "fardh": "Ashobah binafsih",
            "kondisi": "Tidak ada penghalang yang lebih tinggi",
            "alasan": "Sepupu laki-laki dari paman kandung adalah ashobah binafsih urutan ke-11. Mendapat sisa harta jika tidak ada ahli waris yang lebih tinggi urutannya. Dasar hukum: Kaidah ashobah binafsih berdasarkan kedekatan nasab.",
            "syarat_tidak_ada": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN, HeirID.AKH_AB, HeirID.IBN_AKH_ABAWAYN, HeirID.IBN_AKH_AB, HeirID.AMM_ABAWAYN, HeirID.AMM_AB]
        },
        {
            "fardh": "Mahjub",
            "kondisi": "Ada ahli waris ashobah yang lebih tinggi",
            "alasan": "Terhalang oleh semua ashobah yang lebih tinggi sampai urutan ke-10.",
            "syarat_mahjub": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN, HeirID.AKH_AB, HeirID.IBN_AKH_ABAWAYN, HeirID.IBN_AKH_AB, HeirID.AMM_ABAWAYN, HeirID.AMM_AB]
        }
    ],
    
    # =========================================================================
    # SEPUPU LAKI-LAKI DARI PAMAN SEAYAH (IBN AMM AB)
    # =========================================================================
    HeirID.IBN_AMM_AB: [
        {
            "fardh": "Ashobah binafsih",
            "kondisi": "Tidak ada penghalang yang lebih tinggi",
            "alasan": "Sepupu laki-laki dari paman seayah adalah ashobah binafsih urutan ke-12 (terakhir). Mendapat sisa harta jika tidak ada ahli waris yang lebih tinggi urutannya. Dasar hukum: Kaidah ashobah binafsih berdasarkan kedekatan nasab.",
            "syarat_tidak_ada": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN, HeirID.AKH_AB, HeirID.IBN_AKH_ABAWAYN, HeirID.IBN_AKH_AB, HeirID.AMM_ABAWAYN, HeirID.AMM_AB, HeirID.IBN_AMM_ABAWAYN]
        },
        {
            "fardh": "Mahjub",
            "kondisi": "Ada ahli waris ashobah yang lebih tinggi",
            "alasan": "Terhalang oleh semua ashobah yang lebih tinggi sampai urutan ke-11.",
            "syarat_mahjub": [HeirID.IBN, HeirID.IBN_IBN, HeirID.ABB, HeirID.JADD, HeirID.AKH_ABAWAYN, HeirID.AKH_AB, HeirID.IBN_AKH_ABAWAYN, HeirID.IBN_AKH_AB, HeirID.AMM_ABAWAYN, HeirID.AMM_AB, HeirID.IBN_AMM_ABAWAYN]
        }
    ],
    
    # =========================================================================
    # PEMBEBAS BUDAK (MUTIQ & MUTIQAH)
    # =========================================================================
    HeirID.MUTIQ: [
        {
            "fardh": "Ashobah bi sabab",
            "kondisi": "Tidak ada ahli waris lain sama sekali",
            "alasan": "Laki-laki pembebas budak (mu'tiq) mendapat sisa harta sebagai ashobah bi sabab (ashobah karena sebab memerdekakan budak) jika tidak ada ahli waris nasab sama sekali. Dasar hukum: Hadits Nabi SAW tentang wala' (hak waris karena memerdekakan budak).",
            "catatan": "Jarang terjadi di zaman modern, hanya relevan jika pewaris adalah budak yang dimerdekakan"
        }
    ],
    
    HeirID.MUTIQAH: [
        {
            "fardh": "Ashobah bi sabab",
            "kondisi": "Tidak ada ahli waris lain dan tidak ada mu'tiq laki-laki",
            "alasan": "Perempuan pembebas budak (mu'tiqah) mendapat sisa harta sebagai ashobah bi sabab jika tidak ada ahli waris nasab dan tidak ada mu'tiq laki-laki. Dasar hukum: Hadits tentang wala'.",
            "catatan": "Jarang terjadi di zaman modern"
        }
    ],
}


# Daftar ahli waris yang bisa jadi Ashobah
MALE_ASHOBAH = {
    HeirID.IBN, HeirID.ABB, HeirID.IBN_IBN, HeirID.JADD,
    HeirID.AKH_ABAWAYN, HeirID.AKH_AB, HeirID.IBN_AKH_ABAWAYN,
    HeirID.IBN_AKH_AB, HeirID.AMM_ABAWAYN, HeirID.AMM_AB,
    HeirID.IBN_AMM_ABAWAYN, HeirID.IBN_AMM_AB
}

FEMALE_ASHOBAH_BIL_GHAIR = {HeirID.BINT, HeirID.BINT_IBN}
FEMALE_ASHOBAH_MAAL_GHAIR = {HeirID.UKHT_ABAWAYN, HeirID.UKHT_AB}

# Tabel 'Aul yang valid
VALID_AUL = {
    6: [7, 8, 9, 10],
    12: [13, 15, 17],
    24: [27]
}


# =============================================================================
# URUTAN PRIORITAS ASHOBAH BINAFSIH
# Sesuai dokumen: urutan 1-12
# =============================================================================
ASHOBAH_PRIORITY = [
    HeirID.IBN,                # 1. Anak laki-laki
    HeirID.IBN_IBN,            # 2. Cucu laki-laki (وان نزل - turun terus)
    HeirID.ABB,                # 3. Ayah
    HeirID.JADD,               # 4. Kakek (وان عال - naik terus)
    HeirID.AKH_ABAWAYN,        # 5. Saudara laki-laki kandung
    HeirID.AKH_AB,             # 6. Saudara laki-laki seayah
    HeirID.IBN_AKH_ABAWAYN,    # 7. Keponakan dari saudara kandung
    HeirID.IBN_AKH_AB,         # 8. Keponakan dari saudara seayah
    HeirID.AMM_ABAWAYN,        # 9. Paman kandung
    HeirID.AMM_AB,             # 10. Paman seayah
    HeirID.IBN_AMM_ABAWAYN,    # 11. Sepupu dari paman kandung
    HeirID.IBN_AMM_AB,         # 12. Sepupu dari paman seayah
]


# =============================================================================
# KASUS-KASUS KHUSUS
# =============================================================================

# Kasus Umariyyatan (Gharrawain)
UMARIYYATAN_CASES = {
    "gharrawain_1": {
        "ahli_waris": [HeirID.ZAWJ, HeirID.ABB, HeirID.UMM],
        "pembagian": {
            HeirID.ZAWJ: "1/2",
            HeirID.UMM: "1/3 sisa (dari sisa setelah suami)",
            HeirID.ABB: "sisa"
        },
        "penjelasan": "Kasus Umariyyatan pertama: Suami, Ayah, Ibu. Ibu mendapat 1/3 dari sisa setelah suami (bukan 1/3 dari keseluruhan)."
    },
    "gharrawain_2": {
        "ahli_waris": [HeirID.ZAWJAH, HeirID.ABB, HeirID.UMM],
        "pembagian": {
            HeirID.ZAWJAH: "1/4",
            HeirID.UMM: "1/3 sisa (dari sisa setelah istri)",
            HeirID.ABB: "sisa"
        },
        "penjelasan": "Kasus Umariyyatan kedua: Istri, Ayah, Ibu. Ibu mendapat 1/3 dari sisa setelah istri (bukan 1/3 dari keseluruhan)."
    }
}

# Kasus Musytarakah (Himariyyah/Haal)
MUSYTARAKAH_CASE = {
    "ahli_waris_minimum": [HeirID.ZAWJ, HeirID.UMM, HeirID.AKH_UMM],
    "ahli_waris_bisa_ditambah": [HeirID.UKHT_UMM],
    "catatan": "Saudara seibu berbagi dengan ibu dalam kondisi tertentu bersama suami/istri",
    "penjelasan": "Kasus Musytarakah: Suami/Istri bersama Ibu dan dua atau lebih saudara seibu. Saudara seibu berbagi bagian 1/3 dengan ibu."
}

# Kasus Akdariyyah
AKDARIYYAH_CASE = {
    "ahli_waris": [HeirID.ZAWJ, HeirID.UMM, HeirID.JADD, HeirID.UKHT_ABAWAYN],
    "asal_masalah": 27,
    "penjelasan": "Kasus Akdariyyah (masalah 27): Suami, Ibu, Kakek, dan Saudari Kandung. Kasus langka dengan asal masalah 27.",
    "pembagian_awal": {
        HeirID.ZAWJ: "1/2 = 13.5/27",
        HeirID.UMM: "1/6 = 4.5/27",
        HeirID.JADD: "musyarakah dengan saudari",
        HeirID.UKHT_ABAWAYN: "musyarakah dengan kakek"
    }
}


# =============================================================================
# CATATAN PENTING UNTUK IMPLEMENTASI
# =============================================================================
