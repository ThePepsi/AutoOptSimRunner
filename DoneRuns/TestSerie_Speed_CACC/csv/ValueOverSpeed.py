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

def load_csv_to_dataframe(filepath):
    """
    Lädt eine CSV-Datei und gibt sie als DataFrame zurück.

    Parameter:
    filepath (str): Der Pfad zur CSV-Datei.

    Rückgabe:
    DataFrame: Ein DataFrame, der die Daten aus der CSV-Datei enthält.
    """
    # Laden der CSV-Datei
    # delimiter=';' bedeutet, dass ';' als Trennzeichen zwischen den Werten in der Datei verwendet wird
    df = pd.read_csv(filepath, delimiter=';')

    return df

import csv

def remove_spaces_from_csv(file_path):
    # Temporäre Liste zum Speichern der bearbeiteten Zeilen
    modified_rows = []

    # Öffnen der CSV-Datei und Einlesen der Daten
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # Entfernen aller Leerzeichen aus jedem Feld der Zeile
            modified_row = [field.replace(' ', '') for field in row]
            modified_rows.append(modified_row)

    # Schreiben der bearbeiteten Daten zurück in die Datei
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(modified_rows)
    
    return file_path


print(os.getcwd())
dates = {}

dates['500']= load_csv_to_dataframe(remove_spaces_from_csv("C:\\Users\\timos\\OneDrive\\Desktop\\AutoOptSimRunner\\DoneRuns\\TestSerie_Speed_CACC\\csv\\500n.csv"))
dates['1000']= load_csv_to_dataframe(remove_spaces_from_csv("C:\\Users\\timos\\OneDrive\\Desktop\\AutoOptSimRunner\\DoneRuns\\TestSerie_Speed_CACC\\csv\\1000n.csv"))
dates['5000']= load_csv_to_dataframe(remove_spaces_from_csv("C:\\Users\\timos\\OneDrive\\Desktop\\AutoOptSimRunner\\DoneRuns\\TestSerie_Speed_CACC\\csv\\5000n.csv"))
dates['15000']= load_csv_to_dataframe(remove_spaces_from_csv("C:\\Users\\timos\\OneDrive\\Desktop\\AutoOptSimRunner\\DoneRuns\\TestSerie_Speed_CACC\\csv\\1000min.csv"))


def plot_graphs_in_two_rows_with_individual_limits(dataframes_dict, y_value_columns, y_limits_list):
    """
    Erstellt Graphen für jeden DataFrame in einem Dictionary und verteilt sie auf zwei Zeilen,
    mit individuell definierten Y-Achsen-Bereichen für jedes Diagramm. Ein Subplot bleibt leer, wenn weniger als 4 Diagramme gezeichnet werden.
    
    Parameter:
    dataframes_dict (dict): Ein Dictionary, das DataFrames enthält. Die Schlüssel sind Bezeichner für jeden DataFrame.
    y_value_columns (list): Eine Liste mit Namen der Spalten, die auf der Y-Achse der Graphen gezeigt werden sollen.
    y_limits_list (list): Eine Liste von Tupeln, wobei jedes Tupel den minimalen und maximalen Wert der Y-Achse für jedes Diagramm angibt.
    """
    
    # Berechnen, wie viele Spalten benötigt werden (maximal 2 Spalten für bis zu 3 Diagramme)
    n_cols = 2
    n_rows = 2  # Fix auf zwei Zeilen gesetzt
    
    # Erstellen einer Figure und Subplots
    fig, axs = plt.subplots(n_rows, n_cols, figsize=(18, 12))  # 2 Zeilen, 2 Spalten
    
    # Ein flaches Array aus den Subplot-Achsen erstellen, um einfacher darauf zugreifen zu können
    axs_flat = axs.flatten()
    
    for i, (y_value_column, y_limits) in enumerate(zip(y_value_columns, y_limits_list)):
        ax = axs_flat[i]  # Den aktuellen Subplot-Achsen auswählen
        for key, df in dataframes_dict.items():
            # Überprüfen, ob der Spaltenname im DataFrame existiert
            if y_value_column not in df.columns:
                print(f"Die Spalte '{y_value_column}' existiert nicht im DataFrame für Schlüssel '{key}'.")
                continue  # Zum nächsten DataFrame im Dictionary übergehen
            
            # Sicherstellen, dass die Daten nach 'leaderSpeed' sortiert sind
            sorted_df = df.sort_values(by='leaderSpeed')
            
            ax.plot(sorted_df['leaderSpeed'], sorted_df[y_value_column], marker='o', label=f'Schlüssel {key}')
            ax.set_title(f"Geschwindigkeit vs. {y_value_column}")  # Titel des Subplots
            ax.set_xlabel('Geschwindigkeit (leaderSpeed)')  # Beschriftung der x-Achse
            ax.set_ylabel(y_value_column)  # Beschriftung der y-Achse
            ax.grid(True)  # Gitternetzlinien anzeigen
            ax.legend()  # Legende anzeigen
        
        # Setzen des individuellen Y-Achsen-Bereichs für den aktuellen Subplot
        ax.set_ylim(y_limits)
    
    # Den letzten Subplot ausblenden, wenn weniger als 4 Diagramme vorhanden sind
    for j in range(i + 1, 4):
        fig.delaxes(axs_flat[j])

    plt.tight_layout()  # Stellt sicher, dass die Subplots nicht überlappen
    plt.show()  # Zeigen der Figure mit allen Subplots



# ALL IN ONE
# Beispielaufruf der Funktion mit individuellen Y-Achsen-Bereichen für drei Graphen
y_value_columns = ["caccC1", "caccOmegaN", "caccXi"]
y_limits_list = [(0.3, 1), (0, 2), (0, 160)]  # Beispielwerte für Y-Achsen-Bereiche
plot_graphs_in_two_rows_with_individual_limits(dataframes_dict=dates, y_value_columns=y_value_columns, y_limits_list=y_limits_list)
    
def plot_graph_from_dict(dataframes_dict, y_value_column):
    """
    Erstellt Graphen für jeden DataFrame in einem Dictionary. Jeder Graph wird in dasselbe Plot gezeichnet.
    
    Parameter:
    dataframes_dict (dict): Ein Dictionary, das DataFrames enthält. Die Schlüssel sind Bezeichner für jeden DataFrame.
    y_value_column (str): Der Name der Spalte, die auf der Y-Achse gezeigt werden soll.
    """
    plt.figure(figsize=(12, 8))  # Größe des Graphen festlegen
    
    for key, df in dataframes_dict.items():
        # Überprüfen, ob der Spaltenname in DataFrame existiert
        if y_value_column not in df.columns:
            print(f"Die Spalte '{y_value_column}' existiert nicht im DataFrame für Schlüssel '{key}'.")
            continue  # Zum nächsten DataFrame im Dictionary übergehen
        
        plt.plot(df['leaderSpeed'], df[y_value_column], marker='o', label=f'Schlüssel {key}')
    
    plt.title(f"Geschwindigkeit vs. {y_value_column}")  # Titel des Graphen
    plt.xlabel('Geschwindigkeit (leaderSpeed)')  # Beschriftung der x-Achse
    plt.ylabel(y_value_column)  # Beschriftung der y-Achse
    plt.grid(True)  # Gitternetzlinien anzeigen
    plt.legend()  # Legende anzeigen
    plt.show()  # Zeigen des Graphen

plot_graph_from_dict(dates, "caccC1")
plot_graph_from_dict(dates, "caccOmegaN")
plot_graph_from_dict(dates, "caccXi")