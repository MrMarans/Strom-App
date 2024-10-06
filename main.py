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
    "Januar": "01",
    "Februar": "02",
    "März": "03",
    "April": "04",
    "Mai": "05",
    "Juni": "06",
    "Juli": "07",
    "August": "08",
    "Sepember": "09",
    "Oktober": "10",
    "November": "11",
    "Dezember": "12"
}



def loadChart(chosenYear):
    years_data = {}
    data = {}
    
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


    # Daten generieren
    strom = []
    pv_mini = []
    pv = []
    y = []
    fig, ax = plt.subplots(figsize=(10, 6))
    if chosenYear == "Alle":
        years = []
        for year, monthData in years_data.items():
            for month, data in monthData.items():
                pass



    elif chosenYear == "Zeitlinie":
        for year, monthData in years_data.items():
            for month, data in monthData.items():
                # print(f"{year} was year,  {month} was month, {data} was data")
                strom.append(data["strom"])
                pv_mini.append(data["PV_Mini"])
                pv.append(data["PV"])
                y.append(f"{year-2000}_{month}")

    else:
        for month, data in years_data[chosenYear].items():
            strom.append(data["strom"])
            pv_mini.append(data["PV_Mini"])
            pv.append(data["PV"])
            y.append(month)

    ax.plot(y, strom, label='Monat')
    ax.plot(y ,pv_mini, label = "PV mini")
    ax.plot(y ,pv, label= "PV")

    for i in enumerate(y):
        ax.text(strom,y,i, ha="center", va="center")

    # Diagramm beschriften
    ax.set_title('Stromdaten')
    ax.set_xlabel('Monat')
    ax.set_ylabel('Strommenge')
    ax.legend()
    ax.grid(True)

    # Diagramm in Streamlit anzeigen
    plot = st.pyplot(fig)
    
    return plot #?



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
    
    # if chosenYear == "Alle":
        # passYear = "Alle"
    # else: 
    passYear = chosenYear
    loadChart(passYear)

    
def drawInputs():

    drawYearsRadio()

    year= st.number_input("Jahr:", value=current_year)

    month = st.selectbox("Wähle einen Monat:", ["Bitte Auswählen", "Januar","Februar","März","April","Mai","Juni","Juli","August","Sepember","Oktober","November","Dezember"])

    strom = st.number_input("Menge:", value=0)
    pv_Mini= st.number_input("PV Mini:", value=0)
    pv= st.number_input("PV:", value=0)


    if st.button("Daten speichern"):
        try:
            if month != "Bitte Auswählen":
                filename = f"y{year}.json"
                if filename in os.listdir(current_directory):
                    with open(filename) as loadedFile:
                        old = json.load(loadedFile)
                        old[month] = {"strom": strom, "PV_Mini": pv_Mini, "PV": pv}

                #? new file creating
                else:
                    st.write(f"new file for year 20{year} created")
                    old = {month : {"strom": strom, "PV_Mini": pv_Mini, "PV": pv}}
                
                with open(filename,'w') as file:
                    json.dump(old, file)
                
                # loadChart("Zeitlinie")


            else: st.write(f"Bitte noch den Monat auswählen")
        except Exception as e: st.write(f"Error... = {e} ")
    




# plot = loadChart("Zeitlinie")
drawInputs()