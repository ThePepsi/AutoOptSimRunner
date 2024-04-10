import matplotlib.pyplot as plt
import pandas as pd
import os, re


# Call to get the csv from vec
# ./opp_vec2csv.pl --merge-by em -A configname -P "*.prio" -F posx -F posy -F speed -F distance -F relativeSpeed -F nodeId -F acceleration -F controllerAcceleration Braking_1_0.1_0.vec > output.csv

path = "DoneRuns\\TestSerie_Speed_CACC\\DataFromRealSimualtion\\"

c = ['#1f77b4',
 '#ff7f0e',
 '#2ca02c',
 '#d62728',
 '#9467bd',
 '#8c564b',
 '#e377c2',
 '#7f7f7f']

def create_files_per_node(df, output_dir):
    """
    Erstellt für jeden einzigartigen Wert in der 'node'-Spalte der DataFrame eine eigene Datei.
    
    Args:
    - df: DataFrame, die die Daten enthält.
    - output_dir: Der Pfad zum Verzeichnis, in dem die Dateien gespeichert werden sollen.
    
    Returns:
    - Eine Liste der erstellten Dateinamen.
    """
    # Sicherstellen, dass das Ausgabeverzeichnis existiert
    os.makedirs(output_dir, exist_ok=True)
    
    # Eindeutige Werte in der 'node'-Spalte
    unique_nodes = df['node'].unique()
    
    created_files = []  # Liste, um die Namen der erstellten Dateien zu speichern
    
    for node in unique_nodes:
        # Filtern der DataFrame für den aktuellen 'node'-Wert
        node_df = df[df['node'] == node]
        
        # Generieren des Dateinamens basierend auf dem 'node'-Wert
        # Ersetzen von unerwünschten Zeichen im 'node'-Namen, die Probleme in Dateinamen verursachen könnten
        safe_node_name = node.replace('.', '_').replace('[', '_').replace(']', '')
        if "prot" in safe_node_name:
            break
        filename = f"{safe_node_name}.csv"
        
        # Vollständiger Pfad zur Ausgabedatei
        file_path = os.path.join(output_dir, filename)
        
        # Speichern der gefilterten DataFrame in eine CSV-Datei
        node_df = node_df.sort_values(by='time')
        node_df.to_csv(file_path, index=False, sep='\t')
        
        # Hinzufügen des Dateinamens zur Liste der erstellten Dateien
        created_files.append(filename)
        
    return created_files


for data in ["500","1000","5000","10000"]:
    # Verzeichnis für die Ausgabedateien
    output_directory = f'{path}{data}\\split'

    # Aufrufen der Methode und Speichern der Namen der erstellten Dateien
    name = f"{path}{data}\\output.csv"
    df = pd.read_csv(name, sep='\t')
    create_files_per_node(df, output_directory)


def plot(value = "controllerAcceleration", value_label = "Zeit (s)", tmin = 0, tmax=60, ymin=0, ymax = 0):

    # Erstellen des Graphen für den gefilterten Datensatz
    #plt.figure(figsize=(10, 6))
    # Erstellen einer Figure und eines 4x1 Grids von Subplots
    fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(10, 5))
    for i, data in enumerate(["500","1000","5000","10000"]):
        for file in os.listdir(f"{path}{data}\\split"):
            df = pd.read_csv(f"{path}{data}\\split\\"+file, sep='\t')
            node_id = int(re.findall(r'\d+', file)[0])
            axs[i].plot(df['time'], df[value], label=f'Node {node_id}', color=c[node_id])
        axs[i].set_xlim([tmin, tmax])
        if ymax != 0 and ymin != 0:
            axs[i].set_ylim([ymin, ymax]) 
        axs[i].grid(True)
        axs[i].set_title(f'{data} evaluations')
        axs[i].set_xlabel('time (s)')
        axs[i].set_ylabel(value_label)
    
    handles, labels = axs[0].get_legend_handles_labels()

    fig.suptitle(value)
    # Anzeigen des Graphen
    fig.legend(handles, labels, loc='lower center', ncol=8)
    # fig.subplots_adjust(bottom=0.2)
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.show()

# plot("controllerAcceleration","braking deceleration (mpsps)",4,10)
# plot("acceleration","braking deceleration (mpsps)",4,10)
# plot("distance", "distance (m)",4,10,  ymin=4.9,ymax=5.1)
# plot("speed", "speed (mps)",4,10)

def plot_individual_graphs(value="controllerAcceleration", value_label="Zeit (s)", tmin=0, tmax=60, ymin=0, ymax=0, path="DoneRuns\\TestSerie_Speed_CACC\\DataFromRealSimualtion\\"):
    # Iterieren durch jeden Datensatz und Erstellen eines Graphen für jeden
    for data in ["500", "1000", "5000", "10000"]:
        # Erstellen einer neuen Figure für jeden Datensatz
        fig, ax = plt.subplots(figsize=(5, 5))
        
        for file in os.listdir(f"{path}{data}/split"):
            df = pd.read_csv(f"{path}{data}/split/{file}", sep='\t')
            node_id = int(re.findall(r'\d+', file)[0])
            ax.plot(df['time'], df[value], label=f'Node {node_id}') # Die Variable `c` wurde entfernt, da sie nicht definiert ist. Optional kann Farbgebung hinzugefügt werden.
        
        ax.set_xlim([tmin, tmax])
        if ymax != 0 and ymin != 0:
            ax.set_ylim([ymin, ymax])
        ax.grid(True)
        if data != "10000":
            ax.set_title(f'{data} evaluations')
        else:
            ax.set_title(f'15000 evaluations')
        ax.set_xlabel('time (s)')
        ax.set_ylabel(value_label)
        
        # Anzeigen des Titels für jeden Graphen
        #fig.suptitle(value)

        # Anzeigen der Legende
        ax.legend(loc='upper right')
        #ax.legend(loc='lower center', ncol=8, bbox_to_anchor=(0.5, -0.05))
        
        # Anpassen des Layouts, um Platz für die Legende zu schaffen
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        
        # Anzeigen des Graphen
        plt.show()

# plot_individual_graphs("controllerAcceleration","braking deceleration (mpsps)",4,10)
# plot_individual_graphs("acceleration","braking deceleration (mpsps)",4,10)
plot_individual_graphs("distance", "distance (m)",4,12,  ymin=4.9,ymax=5.15)
# plot_individual_graphs("speed", "speed (mps)",4,10)