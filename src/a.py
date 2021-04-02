import matplotlib.pyplot as plt

plt.ylabel('Score (s)')
plt.xlabel('Algorithms')
data = [21370074, 21547105, 21662045, 21785077]
plt.ylim(bottom=20000000, top=22000000)
labels = ['Simulated Annealing', 'Hillclimbing', 'Genetic(crossover 1)', 'Genetic(crossover 2)']

plt.bar(labels, data)
plt.show()