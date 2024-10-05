import streamlit as st
import time
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

current_year = datetime.now().year
current_directory = os.getcwd()

chart = st.line_chart()

Month_translator = {
    "Januar": 1,
    "Februar": 2,
    "März": 3,
    "April": 4,
    "Mai": 5,
    "Juni": 6,
    "Juli": 7,
    "August": 8,
    "Sepember": 9,
    "Oktober": 10,
    "November": 11,
    "Dezember": 12
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


    if chosenYear == "alle":
        chart.line_chart(data=years_data, x_label="Monat", y_label="Strommenge")
    else:
        chart.line_chart(data=years_data[chosenYear], x_label="Monat", y_label="Strommenge")




def drawYearsRadio():
    years = ["alle"]
    for year in range (35):
            year += 2000 
            filename = f"y{year}.json"
            if filename in os.listdir(current_directory):
                years.append(year)


    chosenYear = st.radio(
        "Which year to show",
        years,
        )
    
    if chosenYear == "alle":
        passYear = "alle"
    else: 
        passYear = chosenYear
    loadChart(passYear)

    
def drawInputs():

    drawYearsRadio()

    year= st.number_input("Jahr:", value=current_year)

    month = st.selectbox("Wähle einen Monat:", ["Bitte Auswählen", "Januar","Februar","März","April","Mai","Juni","Juli","August","Sepember","Oktober","November","Dezember"])

    strom = st.number_input("Menge:", value=0)
    st.write(f"{strom} gemacht")


    if st.button("Daten speichern"):
        try:
            if month != "Bitte Auswählen":
                filename = f"y{year}.json"
                if filename in os.listdir(current_directory):
                    with open(filename) as loadedFile:
                        old = json.load(loadedFile)
                        old[str(Month_translator[month])] = strom

                else:
                    st.write(f"new file for year 20{year} created")
                    old = {str(Month_translator[month]):strom}
                
                
                with open(filename,'w') as file:
                    json.dump(old, file)
                    loadChart()


            else: st.write(f"Bitte noch den Monat auswählen")
        except Exception as e: st.write(f"Error... = {e} ")
    




loadChart("alle")
drawInputs()