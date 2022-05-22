from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import re
import requests

error_message = {'Error Message': 'Invalid API call. Please retry or visit the documentation '
                                  '(https://www.alphavantage.co/documentation/) for TIME_SERIES_INTRADAY.'}


class ButtonGrid(GridLayout):
    def __init__(self, **kwargs):
        super(ButtonGrid, self).__init__(**kwargs)  # calls super constructor with the arguments passed as **kwargs
        self.cols = 2

        # button widget
        self.button = Button(
            text="add",
            size_hint=(0.5, 0.5),
            bold=True,
            background_color='#0FF0A5',
            size_hint_y=None,
            height=self.height * 0.5
        )
        self.button.bind(on_press=self.add_function)
        self.add_widget(self.button)

        # button widget
        self.button = Button(
            text="remove",
            size_hint=(0.5, 0.5),
            bold=True,
            background_color='#E81749',
            size_hint_y=None,
            height=self.height*0.5
        )

        self.button.bind(on_press=self.remove_function)
        self.add_widget(self.button)

    def remove_function(self, instance):
        stock = str(self.parent.children[1].text).upper()

        # checks for empty submits and help requests
        if stock == "":
            self.parent.children[2].text = "Please enter the stock tagg \nor help to return to instructions"
            return
        elif re.search('help', stock):
            self.parent.children[2].text = "Here you can add stocks to your personal window!\n"\
                                   "To add more stocks write the tagg of the stock "\
                                   "and click submit\n"\
                                   "If you want to remove one enter the stock tag and "\
                                   "click remove"
            return

        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='
        second_part = '&interval=5min&apikey=RA66O94G43D93XOV'
        url = url + stock + second_part
        r = requests.get(url)
        data = r.json()
        new_line = ""
        flag_found = False

        # check if the stock tagg exists
        if data == error_message:
            self.parent.children[2].text = "The stock tagg you entered is wrong\n " \
                                           "please check the stock tagg and retry"
        else:
            file_stocks = open("stocks_list.txt", "r+")

            # checks if the item is already in the file
            for line in file_stocks:

                if line.strip("\n") == stock:
                    flag_found = True

                else:
                    new_line += line

            if flag_found:
                # removes last newline character
                new_line = new_line[:-1]
                self.parent.children[2].text = "Successfully removed"

                # saves the new list
                file_stocks.close()
                file_stocks = open("stocks_list.txt", "w+")
                file_stocks.write(new_line)
            else:
                self.parent.children[2].text = "Item doesn't exist!"

    def add_function(self, instance):
        stock = str(self.parent.children[1].text).upper()

        # checks for empty submits and help requests
        if stock == "":
            self.parent.children[2].text = "Please enter the stock tagg \nor help to return to instructions"
            return
        elif re.search('HELP', stock):
            self.parent.children[2].text = "Here you can add stocks to your personal window!\n"\
                                   "To add more stocks write the tagg of the stock "\
                                   "and click submit\n"\
                                   "If you want to remove one enter the stock tag and "\
                                   "click remove"
            return

        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='
        second_part = '&interval=5min&apikey=RA66O94G43D93XOV'
        url = url + stock + second_part
        r = requests.get(url)
        data = r.json()
        line_counter = 0

        # check if the stock tagg exists
        if data == error_message:
            self.parent.children[2].text = "The stock tagg you entered is wrong\n " \
                                           "please check the stock tagg and retry"
        else:
            file_stocks = open("stocks_list.txt", "r+")

            # checks if the item is already in the file
            for line in file_stocks:

                if line_counter == 3:
                    self.parent.children[2].text = "You have enter the maximum" \
                                                   "numer of elements in the list "
                    return

                line_counter += 1
                if line.strip("\n") == stock:

                    self.parent.children[2].text = "You already have this stock in your list"
                    return

            file_stocks.write("\n" + stock)
            self.parent.children[2].text = "Successfully added!"


class MainApp(GridLayout):

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)  # calls super constructor with the arguments passed as **kwargs

        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # label widget
        self.greeting = Label(text="Here you can add stocks to your personal window!\n"
                                   "To add more stocks write the tagg of the stock "
                                   "and click submit\n"
                                   "If you want to remove one enter the stock tag and "
                                   "click remove", font_size=18)
        self.add_widget(self.greeting)

        # text input field
        self.command = TextInput(
            multiline=False,
            padding_y=(20, 20),
            size_hint=(1, 0.5)
        )

        self.add_widget(self.command)
        self.add_widget(ButtonGrid())


class Settings(App):

    def build(self):
        return MainApp()


Settings().run()
