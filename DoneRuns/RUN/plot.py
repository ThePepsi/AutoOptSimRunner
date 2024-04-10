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

def plot_simple_graph(df, x_axis_name, y_axis_name, y_lim = None):
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
    plt.show()


def plot_speed_braking_graph(df, y_axis_name, error, y_lim = None):
    """
    Plottet einen Graphen basierend auf dem übergebenen DataFrame und den Namen der X- und Y-Achsen.

    Args:
    - df: pandas DataFrame, der die Daten enthält.
    - y_axis_name: Der Name der Spalte im DataFrame, die als Y-Achse dient.
    """
    for startBraking in sorted(df['startBraking'].unique()):
        f_df = df[(df['startBraking'] == startBraking )]
        plt.plot(f_df["leaderSpeed"], f_df[y_axis_name], label= startBraking)

    plt.title(f'{y_axis_name} vs. LeaderSpeed and frameErrorRate == {error}')
    plt.grid(True)  # Gitternetzlinien anzeigen
    plt.legend(loc='upper right')  # Legende anzeigen
    plt.xlabel("LeaderSpeed")
    plt.ylabel(y_axis_name)
    if y_lim:
        plt.ylim(y_lim)
    plt.show()


def plot_speed_error_graph(df, y_axis_name, y_lim = None):
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
    plt.show()



def plot_3d_graph(df, y_value):
    """
    Erstellt einen 3D-Graphen aus einem gegebenen DataFrame.
    
    Args:
    - df: Der DataFrame, der die Daten enthält.
    - y_value: Der Name der Spalte, die als Y-Achse verwendet wird.
    """
    # Initialisiere einen 3D-Plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Eindeutige frameErrorRates extrahieren
    unique_error_rates = np.unique(df['frameErrorRate'])

    # Für jede einzigartige frameErrorRate
    for error_rate in unique_error_rates:
        # Filtere den DataFrame für die aktuelle frameErrorRate
        filtered_df = df[df['frameErrorRate'] == error_rate].sort_values(by=y_value)

        # Werte für Achsen extrahieren
        x = filtered_df['leaderSpeed']
        y = filtered_df[y_value]
        z = filtered_df['frameErrorRate']
        
        # Eine Linie für die aktuelle frameErrorRate zeichnen
        ax.scatter(x, y, z, label=f'Error Rate: {error_rate}')
    
    # Titel und Achsenbeschriftungen hinzufügen
    ax.set_title('3D-Scatter-Plot')
    ax.set_xlabel('Leader Speed')
    ax.set_ylabel(y_value)
    ax.set_zlabel('Frame Error Rate')
    
    # Zeige den Plot an
    plt.show()

def plot_3d_scatter_with_braking_color(df, z_value_key):
    """
    Erstellt einen 3D-Scatter-Plot mit leaderSpeed auf der X-Achse, 
    frameErrorRate auf der Y-Achse und einem dynamischen Z-Wert basierend auf z_value_key.
    Die Farbe der Punkte basiert auf dem Wert von 'startBraking'.
    
    Args:
    - df: pandas DataFrame, das die Daten enthält.
    - z_value_key: Der Schlüssel aus dem DataFrame, der für die Z-Werte verwendet wird.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Daten für X, Y und Z extrahieren
    xs = df['leaderSpeed']
    ys = df['frameErrorRate']
    zs = df[z_value_key]
    
    # Farbgebung basierend auf startBraking
    colors = df['startBraking']

    scatter = ax.scatter(xs, ys, zs, c=colors, cmap='coolwarm', marker='o')

    # Farblegende hinzufügen
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label('Start Braking')
    
    # Achsenbeschriftungen hinzufügen
    ax.set_xlabel('Leader Speed')
    ax.set_ylabel('Frame Error Rate')
    ax.set_zlabel(z_value_key)
    
    # Titel hinzufügen
    ax.set_title('3D Scatter Plot with Braking Color')

    plt.show()

def plot_speed_braking_graph(df, y_axis_name, y_lim = None):
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
    plt.show()

# csv_path = input("CSV File:")
# controller = input("Controller:")





if "CACC" == "CACC":
    df = clean_csv_and_create_dataframe(f"C:\\Users\\timos\\OneDrive\\Desktop\\AutoOptSimRunner\\DoneRuns\\RUN\\CACC\\data.csv", ['Hz'])
    print(df)

    filtered_df = df[(df['startBraking'] == 5) & (df['frameErrorRate'] == 0.0)]
    print(filtered_df)
    # plot_simple_graph(filtered_df,"leaderSpeed","caccC1")
    # plot_simple_graph(filtered_df,"leaderSpeed","caccOmegaN")
    # plot_simple_graph(filtered_df,"leaderSpeed","caccXi")
    # plot_simple_graph(filtered_df,"leaderSpeed","value")

    # plot_speed_error_graph(df[(df['startBraking'] == 5 )],"caccC1")
    # plot_speed_error_graph(df[(df['startBraking'] == 5 )],"caccOmegaN")
    # plot_speed_error_graph(df[(df['startBraking'] == 5 )],"caccXi")
    # plot_speed_error_graph(df[(df['startBraking'] == 5 )],"value")

    # for x in [0.0,0.2,0.4,0.6,0.8,0.9,0.95,0.99]:
    #     plot_speed_braking_graph(df[(df['frameErrorRate'] == x )],"value", x)

    #plot_speed_braking_graph(df[(df['frameErrorRate'] == 0 )],"value")

    # plot_3d_scatter_with_braking_color(df, "caccC1")
    # plot_3d_lines_by_error_rate(df[(df['startBraking'] == 5)], "caccC1")
    
    pass

if "FLATBED" == "FLATBED":
    df = clean_csv_and_create_dataframe(f"C:\\Users\\timos\\OneDrive\\Desktop\\AutoOptSimRunner\\DoneRuns\\RUN\\FLATBED\\data.csv", ['Hz'])
    # plot_speed_error_graph(df[(df['startBraking'] == 5 )],"flatbedKa")
    # plot_speed_error_graph(df[(df['startBraking'] == 5 )],"flatbedKv")
    # plot_speed_error_graph(df[(df['startBraking'] == 5 )],"flatbedKp")
    # plot_speed_error_graph(df[(df['startBraking'] == 5 )],"flatbedH")
    # plot_speed_error_graph(df[(df['startBraking'] == 5 )],"value")

    for x in [0.0,0.2,0.4,0.6,0.8,0.9,0.95,0.99]:
        plot_speed_braking_graph(df[(df['frameErrorRate'] == x )],"value", x)





