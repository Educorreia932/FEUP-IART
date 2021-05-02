# Reads the output profiling stats binary file and presents it in a human readable manner

import pstats

p = pstats.Stats('out/stats')
p.sort_stats('tottime').print_stats(20)
