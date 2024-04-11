import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
import numpy as np

error_rate_colors = {
    0.0: "#0000FF",  # Blau
    0.2: "#3232FF",  # Heller Blau
    0.4: "#6666FF",  # Noch heller Blau
    0.6: "#FF9999",  # Rosa
    0.8: "#FF6666",  # Hellrot
    0.9: "#FF3232",  # Rot
    0.95: "#FF0000",  # Dunkelrot
    0.99: "#990000",  # Noch dunkleres Rot
}
    
def clean_csv_and_create_dataframe(csv_path, removal_list):
    """
    Liest den Inhalt einer CSV-Datei als Text, führt eine Bereinigung durch,
    indem spezifische Strings entfernt werden, und lädt den bereinigten Text in einen DataFrame.

    Args:
    - csv_path: Der Pfad zur CSV-Datei.
    - removal_list: Eine Liste von Strings (oder Regex-Patterns), die aus dem Text entfernt werden sollen.

    Returns:
    - Ein pandas DataFrame mit den bereinigten Daten.
    """
    # Den Inhalt der CSV-Datei lesen
    with open(csv_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Durch die removal_list iterieren und jeden String aus dem Inhalt entfernen
    for pattern in removal_list:
        content = re.sub(pattern, '', content)

    # Den bereinigten Inhalt in einen DataFrame umwandeln
    # Hierbei nutzen wir StringIO, um den String als Datei-ähnliches Objekt zu behandeln
    from io import StringIO
    cleaned_data = StringIO(content)
    df = pd.read_csv(cleaned_data, sep=';')

    return df

def plot_simple_graph(df, x_axis_name, y_axis_name, y_lim = None, save_path = None , show=False):
    """
    Plottet einen Graphen basierend auf dem übergebenen DataFrame und den Namen der X- und Y-Achsen.

    Args:
    - df: pandas DataFrame, der die Daten enthält.
    - x_axis_name: Der Name der Spalte im DataFrame, die als X-Achse dient.
    - y_axis_name: Der Name der Spalte im DataFrame, die als Y-Achse dient.
    """
    plt.plot(df[x_axis_name], df[y_axis_name])
    plt.title(f'{y_axis_name} vs. {x_axis_name}')
    plt.grid(True)  # Gitternetzlinien anzeigen
    plt.legend()  # Legende anzeigen
    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)
    if y_lim:
        plt.ylim(y_lim)
    if save_path:
        plt.savefig(save_path)  # Speichert den Graphen als Datei
        print(f"Graph wurde als '{save_path}' gespeichert.")
    if show:
        plt.show()
    plt.close()

def plot_speed_error_graph(df, y_axis_name, y_lim = None, save_path=None, show = False):
    """
    Plottet einen Graphen basierend auf dem übergebenen DataFrame und den Namen der X- und Y-Achsen.

    Args:
    - df: pandas DataFrame, der die Daten enthält.
    - y_axis_name: Der Name der Spalte im DataFrame, die als Y-Achse dient.
    """
    for errorRate in sorted(df['frameErrorRate'].unique()):
        f_df = df[(df['frameErrorRate'] == errorRate )]
        plt.plot(f_df["leaderSpeed"], f_df[y_axis_name], label= errorRate, color = error_rate_colors[errorRate])

    #plt.title(f'{y_axis_name} vs. LeaderSpeed and frameErrorRate')
    plt.grid(True)  # Gitternetzlinien anzeigen
    plt.legend(loc='upper right')  # Legende anzeigen
    plt.xlabel("LeaderSpeed")
    plt.ylabel(y_axis_name)
    if y_lim:
        plt.ylim(y_lim)

    if save_path:
        plt.savefig(save_path)  # Speichert den Graphen als Datei
        print(f"Graph wurde als '{save_path}' gespeichert.")
    if show:
        plt.show()
    plt.close()

def plot_speed_braking_graph(df, y_axis_name, y_lim = None, save_path=None, show=False):
    """
    Plottet einen Graphen basierend auf dem übergebenen DataFrame und den Namen der X- und Y-Achsen.

    Args:
    - df: pandas DataFrame, der die Daten enthält.
    - y_axis_name: Der Name der Spalte im DataFrame, die als Y-Achse dient.
    """

    plt.figure(figsize=(12, 8))
    color = {
        5: "#0000FF",  # Blau
        5.01: "#FF9999",  # Rosa
        5.05: "#990000",  # Noch dunkleres Rot
    }

    for startBraking in sorted(df['startBraking'].unique()):
        f_df = df[(df['startBraking'] == startBraking )]
        plt.plot(f_df["leaderSpeed"], f_df[y_axis_name], label= startBraking, color = color[startBraking], linewidth=4)

    # Dicke der Spines (x- und y-Achsenlinien) anpassen
    ax = plt.gca()  # Gibt das aktuelle Axes-Objekt zurück
    ax.spines['top'].set_linewidth(4)    # Dicke der oberen Linie anpassen
    ax.spines['bottom'].set_linewidth(4) # Dicke der unteren Linie anpassen
    ax.spines['left'].set_linewidth(4)   # Dicke der linken Linie anpassen
    ax.spines['right'].set_linewidth(4)  # Dicke der rechten Linie anpassen
    plt.tick_params(axis='x', labelsize=40)
    plt.tick_params(axis='y', labelsize=40)

    #plt.title(f'{y_axis_name} vs. LeaderSpeed and frameErrorRate')
    plt.grid(True)  # Gitternetzlinien anzeigen
    plt.legend(loc='upper right')  # Legende anzeigen
    # plt.xlabel("LeaderSpeed")
    # plt.ylabel(y_axis_name)
    if y_lim:
        plt.ylim(y_lim)
    plt.ylim(bottom=0)
    
    if save_path:
        plt.savefig(save_path)  # Speichert den Graphen als Datei
        print(f"Graph wurde als '{save_path}' gespeichert.")
    if show:
        plt.show()
    plt.close()

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

def plot_3d_speed_braking_value(df, save_path= None):
    color = {
        5: "#0000FF",  # Blau
        5.01: "#FF9999",  # Rosa
        5.05: "#990000",  # Noch dunkleres Rot
    }

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Für jede einzigartige startBraking , plotte die leaderSpeed vs. value
    for errorRate in sorted(df['frameErrorRate'].unique()):
        for startBraking  in sorted(df['startBraking'].unique()):
            subset = df[df['frameErrorRate'] == errorRate]
            subsubset = subset[subset['startBraking'] == startBraking]
            ax.plot(subsubset['leaderSpeed'], [errorRate]*len(subsubset), zs=subsubset['value'], label=f'{startBraking}', color = color[startBraking])
    
    ax.set_xlabel('LeaderSpeed')
    ax.set_ylabel('FrameErrorRate')
    ax.set_zlabel('Value')  
    ax.legend()
    plt.xlim(left=30)
    if save_path:
        plt.savefig(save_path)  # Speichert den Graphen als Datei
        print(f"Graph wurde als '{save_path}' gespeichert.")
    if show:
        plt.show()
    plt.close()


for controller in ["CACC", "PLOEG", "FLATBED"]:
    show = False

    df = clean_csv_and_create_dataframe(f"C:\\Users\\timos\\OneDrive\\Desktop\\AutoOptSimRunner\\DoneRuns\\RUN\\{controller}\\data.csv", ['Hz', 'ps'])
    path = "DoneRuns\\RUN"
    if controller == "CACC":
        for parameter in ["caccC1","caccOmegaN", "caccXi", "value"]:
            plot_speed_error_graph(df[(df['startBraking'] == 5 )],parameter, save_path=f"{path}\\CACC\\CACC_Speed&ErrorRate_{parameter}.png", show=show)
            
            for x in [0.0,0.2]:
                u = str(x).replace(".","")
                plot_simple_graph(df[(df['startBraking'] == 5) & (df['frameErrorRate'] == x)], "leaderSpeed", parameter, save_path=f"{path}\\{controller}\\{controller}_Speed&ErrorRate(set{u})_{parameter}.png", show=show)

    if controller == "PLOEG":
        for parameter in ["ploegKp","ploegKd"]:
            plot_speed_error_graph(df[(df['startBraking'] == 5 )],parameter, save_path=f"{path}\\PLOEG\\PLOEG_Speed&ErrorRate_{parameter}.png", show=show)

    if controller == "FLATBED":
        for parameter in ["flatbedKa","flatbedKv", "flatbedKp","flatbedH"]:
            plot_speed_error_graph(df[(df['startBraking'] == 5 )],parameter, save_path=f"{path}\\FLATBED\\FLATBED_Speed&ErrorRate_{parameter}.png", show=show)

    plot_speed_error_graph(df[(df['startBraking'] == 5 )],"value", save_path=f"{path}\\{controller}\\{controller}_Speed&ErrorRate_value.png", show=show)

    plot_3d_speed_braking_value(df, save_path=f"{path}\\{controller}\\{controller}_Speed_Braking_value_3D.png")

    for x in [0.0,0.2,0.4,0.6,0.8,0.9,0.95,0.99]:
        u = str(x).replace(".","")
        plot_speed_braking_graph(df[(df['frameErrorRate'] == x )],"value", x, save_path=f"{path}\\{controller}\\{controller}_Speed_Braking_value_(error{u}).png", show=show)



