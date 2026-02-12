#First
#pip install PyQt5
#for future use °

import sys
import requests
from requests import Response as resp
from PyQt5.QtWidgets import (QWidget,QApplication,QVBoxLayout,QLabel,QLineEdit,QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("Enter Your City: ",self)
        self.user_input=QLineEdit("Type Here",self)
        self.find_weather_button=QPushButton("Find", self)
        self.temp=QLabel(self)
        self.weather_emoji=QLabel()
        self.description=QLabel(self)
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Winny's Weather App")

        qvbox = QVBoxLayout()

        qvbox.addWidget(self.city_label)
        qvbox.addWidget(self.user_input)
        qvbox.addWidget(self.find_weather_button)
        qvbox.addWidget(self.temp)
        qvbox.addWidget(self.weather_emoji)
        qvbox.addWidget(self.description)

        self.setLayout(qvbox)

        self.user_input.setAlignment(Qt.AlignCenter)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.temp.setAlignment(Qt.AlignCenter)
        self.weather_emoji.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)

        self.user_input.setObjectName("user_input")
        self.city_label.setObjectName("city_label")
        self.temp.setObjectName("temp")
        self.weather_emoji.setObjectName("weather_emoji")
        self.description.setObjectName("description")
        self.find_weather_button.setObjectName("find_weather_button")

        self.setStyleSheet("""
            QLabel,QPushButton{
                font-family:calibri;            
            }
            QLabel#city_label{
                font-size:40px;
            }
            QPushButton#find_weather_button{
                font-size:50px;
                font-weight:bold;
            }
            QLineEdit#user_input{
                font-size:40px;
                font-style:italic;
            }
            QLabel#weather_emoji{
                font-family:segou UI;
                font-size:70px;
            }
            QLabel#temp{
                font-size:70px;
                font-weight:bold
            }
            QLabel#description{
                font-size:30px;
            }
        """)

        self.find_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key="##############################" #provide a valid OpenWeatherMap API Key
        city=self.user_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response=requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"]==200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")


    def display_error(self,message):
        self.temp.setStyleSheet("font-size:30px")
        self.temp.setText(message)

    def display_weather(self, data):
        self.temp.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temp.setText(f"{temperature_c:.0f}°C")
        self.weather_emoji.setText(self.find_weather_emoji(weather_id))
        self.description.setText(weather_description)

    @staticmethod
    def find_weather_emoji(weather_id):

        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return ""

if __name__ =="__main__":
    app = QApplication(sys.argv)
    my_weather_app = WeatherApp()
    my_weather_app.show()
    sys.exit(app.exec_())