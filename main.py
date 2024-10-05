import streamlit as st
import time
import pandas as pd
import numpy as np
import pickle
import os
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)

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





year= st.number_input("Jahr:", value=23)

month = st.selectbox("Wähle einen Monat:", ["Bitte Auswählen", "Januar","Februar","März","April","Mai","Juni","Juli","August","Sepember","Oktober","November","Dezember"])

strom = st.number_input("Menge:", value=0)
st.write(f"{strom} gemacht")


if st.button("Daten speichern"):
    try:
        if month != "Bitte Auswählen":
            with open(f'y{year}.pkl','ab') as csv_file:
                pickle.dump({Month_translator[month]:strom}, csv_file)
                st.write("gespeichert")
        else: st.write(f"Bitte noch den Monat auswählen")
    except Exception as e: st.write(f"Error... = {e} ")



def loadChart():
    all_years = []
    data = {}
    current_directory = os.getcwd()
    for year in range (35):
        filename = f"y{year}.pkl"
        if filename in os.listdir(current_directory):
            print(f"{year} exists")
            with open(filename, 'r') as file:
                try:
                    years_data = pickle.load(file) 
                    print(years_data)
                    all_years.append(years_data)
        
                except EOFError:
                    st.write("Error loading")
            for dic in all_years:
                data[year] = dic

    df = pd.DataFrame(list(data.items()))
    print(data)
    chart = st.line_chart(data=data, x_label="Monat", y_label="Strommenge")


if st.button("Reload Statistuc"):
    loadChart()


progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
# st.button("Re-run")