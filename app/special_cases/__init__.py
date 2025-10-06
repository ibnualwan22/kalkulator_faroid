"""
Special Cases untuk Perhitungan Warisan
Meliputi: Akdariyyah, Jadd Ikhwah, Musytarakah, Gharrawin, Haml, Khuntsa, Gharqa, Munasakhot
"""

from .akdariyyah import is_akdariyyah, calculate_akdariyyah
from .jadd_ikhwah import is_jadd_ikhwah, calculate_jadd_ikhwah
from .musytarakah import is_musytarakah, calculate_musytarakah
from .gharrawin import is_gharrawin, calculate_gharrawin
from .haml import calculate_haml
from .khuntsa import calculate_khuntsa
from .gharqa import calculate_gharqa
from .munasakhot import (
    calculate_munasakhot, 
    calculate_munasakhot_simple,
    MunasakhotCase
)

__all__ = [
    'is_akdariyyah',
    'calculate_akdariyyah',
    'is_jadd_ikhwah',
    'calculate_jadd_ikhwah',
    'is_musytarakah',
    'calculate_musytarakah',
    'is_gharrawin',
    'calculate_gharrawin',
    'calculate_haml',
    'calculate_khuntsa',
    'calculate_gharqa',
    'calculate_munasakhot',
    'calculate_munasakhot_simple',
    'MunasakhotCase',
]
