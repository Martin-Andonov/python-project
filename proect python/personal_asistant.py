import re
import datetime
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import os
import requests


error_message = {"Note": "Thank you for using Alpha Vantage! Our standard API call"
                         " frequency is 5 calls per minute and 500 calls per day. "
                         "Please visit https://www.alphavantage.co/premium/ "
                         "if you would like to target a higher API call frequency."}


class MainApp(GridLayout):

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)  # calls super constructor with the arguments passed as **kwargs

        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.flag = False

        # label widget
        self.greeting = Label(text="Hello, im your personal assistant!\n", font_size=18)
        self.add_widget(self.greeting)

        # text input field
        self.command = TextInput(
            multiline=False,
            padding_y=(20, 20),
            size_hint=(1, 0.5)
        )

        self.add_widget(self.command)

        # button widget
        self.button = Button(
            text="SEND",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#00FFCE',
        )

        self.button.bind(on_press=self.submit_function)
        self.add_widget(self.button)

    def callback(self, instance):
        # change label text to "Hello + user name!"
        self.greeting.text = "Hello " + self.command.text + "!"

    def submit_function(self, instance):

        command = str(self.command.text)

        if command == "":
            self.flag = False
            self.greeting.text = str("please enter a commands!" +
                                     "\nWrite \'help\' to get some examples of how you can use me")

        if re.search("help", command):
            self.flag = False
            self.greeting.text = str("This is the \'help\' page, you can "
                                     "always accuses this page by writing \"help\"!\n"
                                     "You can ask for the current time by writing \'what is the time\'.\n"
                                     "You can also play a game first you have to write \'lets play a game\'\n"
                                     "also you can ask for a Joke by writing \'tell me a joke\'\n"
                                     "Or for a price check of a stock by typing \'price-check stock_tag\'\n"
                                     "or dump price-history of a stock by writing\'price-dump stock_tag\'\nfor"
                                     "more information read the readme document!")

        if re.search("time", command) and re.search("what", command):
            self.flag = False
            self.greeting.text = str(datetime.datetime.now().strftime("DATE:" + " %d/%m/%y" + "\nTIME: " + "%H:%M:%S"))

        if re.search("game", command) and re.search("play", command) and not re.search("how", command):
            self.flag = True
            self.greeting.text = str("what game?\n Press 1 for tic tac toe \n Press 2 for connect 4")

        if re.search("joke", command):
            self.flag = False
            while True:
                header = {"Accept": "application/json"}
                r = requests.get("https://icanhazdadjoke.com/", headers=header)
                data = r.json()["joke"]

                if len(str(data)) < 80:
                    self.greeting.text = str(data)
                    break

        if re.search("price-check", command):
            self.flag = False
            label_output = ""
            command = command.strip("price-check")
            command = command.strip("\n")
            command = command.strip(" ")
            command = command.upper()

            template = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
            symbol = "&symbol="
            interval = "&interval=5min"
            key = "&apikey=RA66O94G43D93XOV"
            url = template + symbol + command + interval + key

            # getting the data with the request
            r = requests.get(url)
            data = r.json()

            if data == error_message:
                label_output = "Error updating the stocks list\n please try again in a minute"
            else:
                # data formatting and string manipulation
                label_output += str(data["Meta Data"]["2. Symbol"]) + ":\n"
                stock_data = data["Time Series (5min)"][data["Meta Data"]["3. Last Refreshed"]]
                label_output += "open:" + str(round(float(stock_data["1. open"]), 2)) + " "
                label_output += "close:" + str(round(float(stock_data["4. close"]), 2)) + "\n"
                label_output += "high:" + str(round(float(stock_data["2. high"]), 2)) + " "
                label_output += "low:" + str(round(float(stock_data["3. low"]), 2)) + "\n"
                label_output += "volume:" + stock_data["5. volume"] + " "
                label_output += "\n\n"

            self.greeting.text = label_output

        if re.search("price-dump", command):
            self.flag = False
            command = command.strip("price-dump")
            command = command.strip("\n")
            command = command.strip(" ")
            command = command.upper()

            template = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
            symbol = "&symbol="
            interval = "&interval=5min"
            key = "&apikey=RA66O94G43D93XOV"
            url = template + symbol + command + interval + key

            # getting the data with the request
            r = requests.get(url)
            data = r.json()

            if data == error_message:
                label_output = "Error dumping the stocks prices\n please try again in a minute"
            else:
                file_name = str(command)
                file = open("%s.json" % file_name, "w+")
                file.write(str(data))
                file.close()
                label_output = "Successfully dumped the stock information in file: " + file_name + ".txt"

            self.greeting.text = label_output

        if self.flag and re.search("1", command):
            self.flag = False
            os.system("python tic_tac_toe.py")
        elif self.flag and re.search("2", command):
            self.flag = False
            os.system("python connect_4.py")


class PersonalAssistant(App):

    def build(self):
        return MainApp()


PersonalAssistant().run()
