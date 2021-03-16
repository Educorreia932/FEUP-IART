# Reads the output of python -m cProfile -o stats .\solution.py

import pstats

p = pstats.Stats('out/stats')
p.sort_stats('tottime').print_stats(20)
