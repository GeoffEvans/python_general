from optimise_aol import calculate_efficiency
from set_up_utils import set_up_aol

def test_efficiency():
    aol = set_up_aol()
    eff = calculate_efficiency(aol, 4)
    
    assert eff < 1 and eff > 0
