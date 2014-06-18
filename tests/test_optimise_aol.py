from optimise_aol import calculate_efficiency, set_up_aol

def test_efficiency():
    aol = set_up_aol()
    eff = calculate_efficiency(aol)
    
    assert eff < 1e-3 and eff > 0