docker build -t strom-app -f app.dockerfile .

then

docker run -d -p 8501:8501 --name heizungs-app-container heizungs-app