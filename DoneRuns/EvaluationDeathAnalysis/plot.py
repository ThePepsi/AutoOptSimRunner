# import pandas as pd
# import matplotlib.pyplot as plt

# df = pd.read_csv(f"DoneRuns\\EvaluationDeathAnalysis\\output1.csv", sep=';')

# fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(10, 5))

# for i, value in enumerate(["caccC1", "caccOmegaN", "caccXi"]):
#     axs[i].plot(df['Evaluations'], df[value])
#     axs[i].grid(True)
#     axs[i].set_title(f'{value}')
#     axs[i].set_xlabel('evaluations')
#     axs[i].set_ylabel(value)


# axs[3].plot(df['Evaluations'], df["Value"])
# axs[3].grid(True)
# # axs[3].set_title(f'{value}')
# axs[3].set_xlabel('evaluations')
# axs[3].set_ylabel("optimisation value")  

# for i in range(0,4):
#     axs[i].axvline(x=48, color='red', linestyle='--',linewidth=0.5)
#     axs[i].axvline(x=2788, color='red', linestyle='--',linewidth=0.5)
#     axs[i].axvline(x=11652, color='red', linestyle='--',linewidth=0.5)
#     axs[i].axvline(x=12824, color='red', linestyle='--',linewidth=0.5)

#     axs[i].axvline(x=500, color='green', linestyle='--',linewidth=0.5)
#     axs[i].axvline(x=1000, color='green', linestyle='--',linewidth=0.5)
#     axs[i].axvline(x=5000, color='green', linestyle='--',linewidth=0.5)
#     axs[i].axvline(x=17000, color='green', linestyle='--',linewidth=0.5)
# axs[2].set_ylim([0, 100]) 

# fig.suptitle(value)
# # Anzeigen des Graphen
# fig.legend(loc='lower center', ncol=8)
# # fig.subplots_adjust(bottom=0.2)
# plt.tight_layout(rect=[0, 0.05, 1, 1])
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt

def plot_graph_from_dict(dataframes_dict, y_value_column, y_limits = None):
    """
    Erstellt Graphen für jeden DataFrame in einem Dictionary. Jeder Graph wird in dasselbe Plot gezeichnet.
    
    Parameter:
    dataframes_dict (dict): Ein Dictionary, das DataFrames enthält. Die Schlüssel sind Bezeichner für jeden DataFrame.
    y_value_column (str): Der Name der Spalte, die auf der Y-Achse gezeigt werden soll.
    """
    plt.figure(figsize=(12, 8))  # Größe des Graphen festlegen
    

        
    plt.plot(df['Evaluations'], df[y_value_column], label=f'Value', linewidth=4)
    
    plt.xlabel('Evaluations', fontsize=40)  # Beschriftung der x-Achse
    plt.ylabel(y_value_column, fontsize=40)  # Beschriftung der y-Achse
    plt.subplots_adjust(left=0.17, right=0.99, top=0.97, bottom=0.15)
    plt.tick_params(axis='x', labelsize=40)
    plt.tick_params(axis='y', labelsize=40)
    plt.grid(True, linewidth=2.0)  # Gitternetzlinien anzeigen


    # Dicke der Spines (x- und y-Achsenlinien) anpassen
    ax = plt.gca()  # Gibt das aktuelle Axes-Objekt zurück
    ax.spines['top'].set_linewidth(4)    # Dicke der oberen Linie anpassen
    ax.spines['bottom'].set_linewidth(4) # Dicke der unteren Linie anpassen
    ax.spines['left'].set_linewidth(4)   # Dicke der linken Linie anpassen
    ax.spines['right'].set_linewidth(4)  # Dicke der rechten Linie anpassen

    ax.axvline(x=48, color='red', linestyle='--',linewidth=4 )
    ax.axvline(x=2788, color='red', linestyle='--',linewidth=4)
    ax.axvline(x=11652, color='red', linestyle='--',linewidth=4)
    ax.axvline(x=12824, color='red', linestyle='--',linewidth=4)

    ax.axvline(x=500, color='green', linestyle='--',linewidth=4 )
    ax.axvline(x=1000, color='green', linestyle='--',linewidth=4)
    ax.axvline(x=5000, color='green', linestyle='--',linewidth=4)
    ax.axvline(x=17000, color='green', linestyle='--',linewidth=4)

    if y_limits:
        ax.set_ylim(y_limits)
    
    # Manuelles Hinzufügen der Legende für axvline
    import matplotlib.lines as mlines
    blue_line = mlines.Line2D([], [], color='blue', linestyle='-', label=f'value')
    red_line = mlines.Line2D([], [], color='red', linestyle='--', label=f'value changes')
    green_line = mlines.Line2D([], [], color='green', linestyle='--', label=f'evaluations depth')
    # Legende mit dem manuell hinzugefügten Eintrag erstellen
    plt.legend(handles=[blue_line, red_line, green_line],fontsize=30)

    plt.show()  # Zeigen des Graphen

# Graphen einzeln erstellen und anzeigen  
df = pd.read_csv(f"DoneRuns\\EvaluationDeathAnalysis\\output1.csv", sep=';')
plot_graph_from_dict(df, "caccC1")
plot_graph_from_dict(df, "caccOmegaN")
plot_graph_from_dict(df, "caccXi",y_limits=[0,50])
plot_graph_from_dict(df, "Value", y_limits=[0,0.001])