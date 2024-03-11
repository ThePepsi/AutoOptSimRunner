import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(f"DoneRuns\\EvaluationDeathAnalysis\\output1.csv", sep=';')

fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(10, 5))

for i, value in enumerate(["caccC1", "caccOmegaN", "caccXi"]):
    axs[i].plot(df['Evaluations'], df[value])
    axs[i].grid(True)
    axs[i].set_title(f'{value}')
    axs[i].set_xlabel('evaluations')
    axs[i].set_ylabel(value)


axs[3].plot(df['Evaluations'], df["Value"])
axs[3].grid(True)
# axs[3].set_title(f'{value}')
axs[3].set_xlabel('evaluations')
axs[3].set_ylabel("optimisation value")  

for i in range(0,4):
    axs[i].axvline(x=48, color='red', linestyle='--',linewidth=0.5)
    axs[i].axvline(x=2788, color='red', linestyle='--',linewidth=0.5)
    axs[i].axvline(x=11652, color='red', linestyle='--',linewidth=0.5)
    axs[i].axvline(x=12824, color='red', linestyle='--',linewidth=0.5)

    axs[i].axvline(x=500, color='green', linestyle='--',linewidth=0.5)
    axs[i].axvline(x=1000, color='green', linestyle='--',linewidth=0.5)
    axs[i].axvline(x=5000, color='green', linestyle='--',linewidth=0.5)
    axs[i].axvline(x=17000, color='green', linestyle='--',linewidth=0.5)
axs[2].set_ylim([0, 100]) 

fig.suptitle(value)
# Anzeigen des Graphen
fig.legend(loc='lower center', ncol=8)
# fig.subplots_adjust(bottom=0.2)
plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.show()