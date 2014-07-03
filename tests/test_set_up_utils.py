from set_up_utils import get_ray_bundle, set_up_aol

op_wavelength = 800e-9

def test_ray_bundle_and_aol():
    rays = get_ray_bundle(op_wavelength=op_wavelength)
    aol = set_up_aol(1, op_wavelength, 40e6, [1e-3,2e-3,1], [1e3,5e2,0], 0.2, [2,2,2,2])
    aol.propagate_to_distance_past_aol(rays, 0, 10)
    # ok as long as no exception 