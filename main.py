import streamlit as st
import time
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

current_year = datetime.now().year
current_directory = os.getcwd() + "/data"
# plot = st.pyplot()
#chart = st.line_chart()


Month_translator = {
    1: "Januar",
    2: "Februar",
    3: "Maerz",
    4: "April",
    5: "Mai",
    6: "Juni",
    7: "Juli",
    8: "August",
    9: "September",  
    10: "Oktober",
    11: "November",
    12: "Dezember"
}

def getAllYears():
    years_data = {}
    
    for year in range (35):
        year += 2000 
        filename = f"y{year}.json"
        if filename in os.listdir(current_directory):
            if filename.endswith('.json'):
                with open(f"{current_directory}/{filename}") as loadedFile:
                    try:
                        year_data = json.load(loadedFile)
                        years_data[year] = year_data         
                    except EOFError:
                        st.write("Error loading")
    return years_data

def loadChart(chosenYear):
    years_data = getAllYears()

    # Generate Data for visualisation
    strom = []
    pv_mini = []
    pv = []
    y = []
    fig, ax = plt.subplots(figsize=(10, 6))
    maxDataPoints = 0

    month_order = ["Januar", "Februar", "Maerz", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

    if chosenYear == "Zeitlinie":
        _ = 0
        sorted_years = sorted(years_data.keys())
        for year in sorted_years:
            monthData = years_data[year]
            sorted_months = sorted(monthData.keys(), key=lambda x: month_order.index(x))
            for month in sorted_months:
                data = monthData[month]
                strom.append(data["strom"])
                pv_mini.append(data["PV_Mini"])
                pv.append(data["PV"])
                y.append(f"{year-2000}_{month}")
                _ += 1
    else:
        _ = 0
        monthData = years_data[chosenYear]
        sorted_months = sorted(monthData.keys(), key=lambda x: month_order.index(x))
        for month in sorted_months:
            data = monthData[month]
            strom.append(data["strom"])
            pv_mini.append(data["PV_Mini"])
            pv.append(data["PV"])
            y.append(month)
            _ += 1
    
    maxDataPoints = _

    #create Slider
    try:
        start_point, end_point = st.slider(
            "Menge der visualisierten Datenpunkte",
            min_value=1,
            max_value=maxDataPoints,
            value=(1, maxDataPoints),
            step=1,
            key= "slider"
        )
    except:
        print(st.text("Nicht genug Datenpunkte für den Slider"))
        start_point = 1
        end_point = 2
    #UI to choose which buttons to show
    with st.popover("Auswahl der Stromdaten"):
        strom_bool = st.checkbox(label="Strom", value=True)
        pv_mini_bool = st.checkbox(label="pv_mini", value=True)
        pv_bool = st.checkbox(label="pv", value=True)
    y = y[start_point-1:end_point]
    
    # Calculate differences
    def calculate_diff(data):
        return [data[i] - data[i-1] for i in range(1, len(data))]

    strom_diff = calculate_diff(strom[start_point-1:end_point])
    pv_mini_diff = calculate_diff(pv_mini[start_point-1:end_point])
    pv_diff = calculate_diff(pv[start_point-1:end_point])

    # Remove the first point from y as well
    y = y[1:]

    #Visualize Data in Plot
    if strom_bool:
        ax.plot(y, strom_diff, label='Strom', color='black', linestyle='--', marker='o')
    
    if pv_mini_bool:
        ax.plot(y, pv_mini_diff, label="PV mini", color='blue', linestyle='-', marker='o')

    if pv_bool:    
        ax.plot(y, pv_diff, label="PV", color='yellow', linestyle='-', marker='o')
    
    # Add difference values to each point
    for y_val, strom_val, pv_mini_val, pv_val in zip(y, strom_diff, pv_mini_diff, pv_diff):
        if strom_bool:  ax.annotate(f'{strom_val:.0f}', (y_val, strom_val), xytext=(0, 5), textcoords='offset points', ha='center') 
        if pv_mini_bool: ax.annotate(f'{pv_mini_val:.0f}', (y_val, pv_mini_val), xytext=(0, 5), textcoords='offset points', ha='center')
        if pv_bool: ax.annotate(f'{pv_val:.0f}', (y_val, pv_val), xytext=(0, 5), textcoords='offset points', ha='center')

    # Diagram texts
    ax.set_title(f'Stromverbrauch und Einnahmen Haus Metzger {chosenYear} (Differenzen)')
    ax.set_xlabel('Monat')
    ax.set_ylabel('kWh (Differenz zum Vormonat)')
    ax.legend()
    ax.grid(True)

    # X Text rotation to be readable
    plt.xticks(rotation=90)

    # Show diagram
    plot = st.pyplot(fig)



def drawYearsRadio():
    years = ["Zeitlinie"]
    for year in range (35):
            year += 2000 
            filename = f"y{year}.json"
            if filename in os.listdir(current_directory):
                years.append(year)

    chosenYear = st.radio(
        "Welche Daten sollen angezeigt werden?",
        years,
    )
    
    loadChart(chosenYear)


def drawSavingInputs():
    
    
    
    year= st.number_input("Jahr:", value=current_year)

    month = st.number_input("Monat:", value=1, min_value=1, max_value=12)

    strom = st.number_input("Gesamte Strommenge kWh:", value=0)
    pv_Mini= st.number_input("PV Mini kWh:", value=0)
    pv= st.number_input("PV kWh:", value=0)


    if st.button("Daten speichern"):
        try:
            filename = f"y{year}.json"
            if filename in os.listdir(current_directory):
                with open(f"{current_directory}/{filename}") as loadedFile:
                    old = json.load(loadedFile)
                    old[Month_translator[month]] = {"strom": strom, "PV_Mini": pv_Mini, "PV": pv}

            #? new file creating 
            else:
                st.write(f"new file for year {year} created")
                old = {Month_translator[month] : {"strom": strom, "PV_Mini": pv_Mini, "PV": pv}}
            
            with open(f"{current_directory}/{filename}",'w') as file:
                json.dump(old, file)
            
            # loadChart("Zeitlinie")
        except Exception as e: st.write(f"Error... = {e} ")
    
def drawBackupButtons():
    with st.popover("Backup"):
        uploaded_files = st.file_uploader(
            "Upload the json data", 
            accept_multiple_files=True,
            type=['json']  # Nur JSON-Dateien erlauben
        )
        for uploaded_file in uploaded_files:
            try:
                # Dateiinhalt als JSON lesen
                json_data = json.loads(uploaded_file.getvalue().decode('utf-8'))
                
                # Speichern der JSON-Datei
                save_path = os.path.join(current_directory, uploaded_file.name)
                with open(save_path, 'w') as file:
                    json.dump(json_data, file, indent=4)
                
                st.success(f"Datei {uploaded_file.name} wurde erfolgreich gespeichert.")
            except json.JSONDecodeError:
                st.error(f"Datei {uploaded_file.name} enthält ungültiges JSON und konnte nicht gespeichert werden.")
            except Exception as e:
                st.error(f"Fehler beim Speichern von {uploaded_file.name}: {str(e)}") 



        for file in os.listdir(current_directory):
            with open(f"{current_directory}/{file}", "rb") as downloadFile:
                st.download_button(
                label=f"Download {file}",
                data=downloadFile,
                file_name=file,
                mime="year/json",)

drawYearsRadio()
drawSavingInputs()
drawBackupButtons()