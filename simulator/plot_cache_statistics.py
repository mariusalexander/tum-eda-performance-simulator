import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import sys

logy  = False;
width = 1.0;

files = sys.argv[1:]
if len(files) == 0: exit()

for file_name in files:
	df = pd.read_csv(file_name)
	print(file_name)
	print(df)

	indicies = df['index']
	nsteps   = 16
	xticks   = np.arange(15, len(indicies), nsteps)
	xlabels  = [str(indicies[i]) for i in xticks]
	
	# plot accesses
	ax = None
	ax = df.plot(kind='bar', x='index', y='hits', color='red', logy=logy, ax=ax, width=width)
	ax.set(xticks=xticks, xticklabels=xlabels)
	#ax.fill_between(x=df.index, y1=df.hits, y2=0, where=df.hits > 0, interpolate=True, color='pink')

	# plot evictions
	ax = df.plot(kind='bar', x='index', y='evictions', color='blue', logy=logy, ax=ax, width=width)
	ax.set(xticks=xticks, xticklabels=xlabels)

	#ax.yaxis.grid(True)#, color='#EEEEEE')
	#ax.xaxis.grid(False)
	
	plt.grid(color='#EEEEEE')
	plt.xlabel("cache block no.")
	plt.ylabel("")
	plt.title(file_name)

plt.show()