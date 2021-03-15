# Reads the output of python -m cProfile -o stats .\solution.py

import pstats
p = pstats.Stats('stats')
p.sort_stats('tottime').print_stats(20)