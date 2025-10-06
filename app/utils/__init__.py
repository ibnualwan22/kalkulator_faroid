"""
Utility modules untuk Kalkulator Faroid
"""

from .constants import (
    HeirID,
    HEIR_NAMES,
    FURUDH_RULES,
    MALE_ASHOBAH,
    FEMALE_ASHOBAH_BIL_GHAIR,
    FEMALE_ASHOBAH_MAAL_GHAIR,
    VALID_AUL
)

from .math_helpers import (
    lcm,
    lcm_multiple,
    gcd_multiple,
    simplify_fraction,
    fraction_to_string,
    parse_fraction,
    add_fractions,
    compare_fractions,
    distribute_shares,
    check_aul_valid,
    calculate_aul,
    calculate_radd_recipients
)

__all__ = [
    # Constants
    'HeirID',
    'HEIR_NAMES',
    'FURUDH_RULES',
    'MALE_ASHOBAH',
    'FEMALE_ASHOBAH_BIL_GHAIR',
    'FEMALE_ASHOBAH_MAAL_GHAIR',
    'VALID_AUL',
    
    # Math helpers
    'lcm',
    'lcm_multiple',
    'gcd_multiple',
    'simplify_fraction',
    'fraction_to_string',
    'parse_fraction',
    'add_fractions',
    'compare_fractions',
    'distribute_shares',
    'check_aul_valid',
    'calculate_aul',
    'calculate_radd_recipients',
]
