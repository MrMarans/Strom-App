This App is a small app to track ones own electricity intake our outtake. 

Basically you have a timeline and you can add something based on year and month. 


to run locally:
pip install poetry
then
poetry install

to start the app:
streamlit run main.py  

To build:
docker build -t strom-app -f app.dockerfile .

then

docker run -d -p 8501:8501 --name strom-app-container strom-app
