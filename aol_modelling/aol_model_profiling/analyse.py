import pstats
p3 = pstats.Stats('Profile3.prof')
p3.sort_stats('cumulative').print_stats(35)
p3.sort_stats('time').print_stats(25)
p4 = pstats.Stats('Profile4.prof')
p4.sort_stats('cumulative').print_stats(35)
p4.sort_stats('time').print_stats(25)
