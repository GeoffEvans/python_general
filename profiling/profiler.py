import pstats, cProfile

import aol_model.pointing_efficiency as p

cProfile.runctx("p.plot_fov_surf(1e9, 0)", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()
