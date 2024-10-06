import streamlit as st
import time
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

current_year = datetime.now().year
current_directory = os.getcwd()
# plot = st.pyplot()
#chart = st.line_chart()


Month_translator = {
    1: "Januar",
    2: "Februar",
    3: "März",
    4: "April",
    5: "Mai",
    6: "Juni",
    7: "Juli",
    8: "August",
    9: "September",  # Korrektur der Schreibweise von "September"
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
            with open(filename) as loadedFile:
                try:
                    year_data = json.load(loadedFile)
                    years_data[year] = year_data         
                except EOFError:
                    st.write("Error loading")
    return years_data

def loadChart(chosenYear):
    years_data = getAllYears()

    # Daten generieren
    strom = []
    pv_mini = []
    pv = []
    y = []
    fig, ax = plt.subplots(figsize=(10, 6))
    maxDataPoints = 0
    if chosenYear == "Zeitlinie":
        _ = 0
        for year, monthData in years_data.items():
            for month, data in monthData.items():
                strom.append(data["strom"])
                pv_mini.append(data["PV_Mini"])
                pv.append(data["PV"])
                y.append(f"{year-2000}_{month}")

                _ +=1
    else:
        _=0
        for month, data in years_data[chosenYear].items():
            strom.append(data["strom"])
            pv_mini.append(data["PV_Mini"])
            pv.append(data["PV"])
            y.append(month)
            _ +=1
    
    maxDataPoints = _


    start_point, end_point = st.slider(
        "Select range of points to display",
        min_value=1,
        max_value=maxDataPoints,
        value=(1, maxDataPoints),  # Default to showing first 12 points
        step=1,
        key= "slider"
    )

    ##PUT in here the radio bool Buttons
    strom_bool = st.checkbox(label="Strom", value=True)
    pv_mini_bool = st.checkbox(label="pv_mini", value=True)
    pv_bool = st.checkbox(label="pv", value=True)
    y = y[start_point-1:end_point]
    # Adjust the data range based on start_point and end_point
    # Note: We subtract 1 from start_point because Python uses 0-based indexing
    if strom_bool:
        strom = strom[start_point-1:end_point]
        ax.plot(y, strom, label='Strom', color='black', linestyle='--', marker='o')
    
    if pv_mini_bool:
        pv_mini = pv_mini[start_point-1:end_point]
        ax.plot(y, pv_mini, label="PV mini", color='blue', linestyle='-', marker='o')

    if pv_bool:    
        pv = pv[start_point-1:end_point]
        ax.plot(y, pv, label="PV", color='yellow', linestyle='-', marker='o')
    
   


    # Add numbers to each point
    for i, (y_val, strom_val, pv_mini_val, pv_val) in enumerate(zip(y, strom, pv_mini, pv), start=start_point):
        if strom_bool:  ax.annotate(f'{i}', (y_val, strom_val), xytext=(0, 5), textcoords='offset points', ha='center') 
        if pv_mini_bool: ax.annotate(f'{i}', (y_val, pv_mini_val), xytext=(0, 5), textcoords='offset points', ha='center')
        if pv_bool: ax.annotate(f'{i}', (y_val, pv_val), xytext=(0, 5), textcoords='offset points', ha='center')

    # Diagramm beschriften
    ax.set_title('Stromdaten')
    ax.set_xlabel('Monat')
    ax.set_ylabel('Strommenge')
    ax.legend()
    ax.grid(True)

    # X-Achsen-Beschriftungen um 90 Grad drehen
    plt.xticks(rotation=90)

    # Diagramm in Streamlit anzeigen
    plot = st.pyplot(fig)
    


    return maxDataPoints

def drawYearsRadio():
    years = ["Zeitlinie"]
    for year in range (35):
            year += 2000 
            filename = f"y{year}.json"
            if filename in os.listdir(current_directory):
                years.append(year)

    chosenYear = st.radio(
        "Which year to show",
        years,
    )
    
    loadChart(chosenYear)


def drawBottomInputs():
    drawYearsRadio()
    

    year= st.number_input("Jahr:", value=current_year)

    month = st.number_input("Monat:", value=1, min_value=1, max_value=12)

    strom = st.number_input("Gesamte Strommenge:", value=0)
    pv_Mini= st.number_input("PV Mini:", value=0)
    pv= st.number_input("PV:", value=0)


    if st.button("Daten speichern"):
        try:
            filename = f"y{year}.json"
            if filename in os.listdir(current_directory):
                with open(filename) as loadedFile:
                    old = json.load(loadedFile)
                    old[Month_translator[month]] = {"strom": strom, "PV_Mini": pv_Mini, "PV": pv}

            #? new file creating
            else:
                st.write(f"new file for year 20{year} created")
                old = {Month_translator[month] : {"strom": strom, "PV_Mini": pv_Mini, "PV": pv}}
            
            with open(filename,'w') as file:
                json.dump(old, file)
            
            # loadChart("Zeitlinie")
        except Exception as e: st.write(f"Error... = {e} ")
    




# plot = loadChart("Zeitlinie")
drawBottomInputs()