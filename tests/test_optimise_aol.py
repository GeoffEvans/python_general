from optimise_aol import calculate_efficiency, set_up_aol

def test_efficiency():
    aol = set_up_aol()
    eff = calculate_efficiency(aol, 4)
    
    assert eff < 1 and eff > 0
