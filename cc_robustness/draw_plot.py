import matplotlib.pyplot as plt
import sys

inputfile = sys.argv[1]
step_size = int(sys.argv[2])
outputfile = sys.argv[3]

y = []
with open(inputfile, 'r') as f:
    for line in f:
        y.append(list(map(lambda x: float(x), line.split())))

x = [i * step_size for i in range(0, len(y[0]))]
print(len(y[0]))
print(x)
plt.plot(x, y[0], 'b')
plt.plot(x, y[1], 'r')
plt.plot(x, y[2], 'g')
plt.plot(x, y[3], 'm')
plt.legend(('6 genomes', '5 genomes', '4 genomes', '3 genomes'), loc=1)
plt.xlabel("Number of breakage steps")
plt.ylabel("Number of connected components")
plt.savefig(outputfile + ".png")
