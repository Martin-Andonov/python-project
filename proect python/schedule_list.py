import re

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

error_message = {'Error Message': 'Invalid API call. Please retry or visit the documentation '
                                  '(https://www.alphavantage.co/documentation/) for TIME_SERIES_INTRADAY.'}


class TextInputGrid(GridLayout):

    def __init__(self, **kwargs):
        super(TextInputGrid, self).__init__(**kwargs)  # calls super constructor with the arguments passed as **kwargs
        self.rows = 3

        # text input field
        self.event = TextInput(
            multiline=False,
            padding_y=(1, 1),
            size_hint=(1, 0.5),
            text="event:"
        )
        # text input field
        self.date = TextInput(
            multiline=False,
            padding_y=(1, 1),
            size_hint=(1, 0.5),
            text="date:"
        )
        # text input field
        self.time = TextInput(
            multiline=False,
            padding_y=(1, 1),
            size_hint=(1, 0.5),
            text="time:"
        )

        self.add_widget(self.event)
        self.add_widget(self.date)
        self.add_widget(self.time)


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
        event = str(self.parent.children[1].children[2].text).strip("event: ")
        date = str(self.parent.children[1].children[1].text).strip("date: ")
        file = open("schedule.txt", "r+")
        new_text = ""

        # removing the line that matches
        for line in file:

            if re.search(event, line):
                pass
            else:
                new_text += line
        file.close()
        file = open("schedule.txt", "w+")
        file.write(new_text)
        self.parent.children[1].children[2].text = "event: "
        self.parent.children[1].children[1].text = "date: "
        self.parent.children[1].children[0].text = "time: "
        self.parent.children[2].text = "Successfully removed"

    def add_function(self, instance):
        event = str(self.parent.children[1].children[2].text).strip("event: ")
        date = str(self.parent.children[1].children[1].text).strip("date: ")
        time = str(self.parent.children[1].children[0].text).strip("time: ")

        # showing the existing schedule
        if re.search("show", event):

            file = open("schedule.txt", "r+")
            string = ""
            for line in file:
                line = line.split("|")

                date_time = line[1].split(" ")
                date = date_time[0] + "/" + date_time[1] + "/" + date_time[2]
                time = date_time[3] + ":" + date_time[4]
                string += line[0] + " " + date + " " + time + "\n"

            self.parent.children[2].text = string
            return

        # adding the new ting to the schedule
        if event == " " or date == "" or time == "":

            self.parent.children[2].text = "Enter event, date and hour!"
        else:
            file = open("schedule.txt", "a+")
            date = date.split("/")
            date = date[0] + " " + date[1] + " " + date[2] + " "
            time = time.split(":")
            time = time[0] + " " + time[1]
            string = event + "|" + date + time + "|" + "\n"
            file.write(string)
            self.parent.children[1].children[2].text = "event: "
            self.parent.children[1].children[1].text = "date: "
            self.parent.children[1].children[0].text = "time: "
            self.parent.children[2].text = "Successfully added"


class MainApp(GridLayout):

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)  # calls super constructor with the arguments passed as **kwargs

        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # label widget
        self.greeting = Label(text="Here you can add or remove things to your schedule list.\n"
                                   "if you want to remove a scheduled event write the name of\n the event  "
                                   "click delete, if you want to see all the events \n write \'show\' in the"
                                   " event tab and click add dates should\n follow (dd/mm/yy) and "
                                   "time should follow (hh:mm) formats", font_size=18)
        self.add_widget(self.greeting)

        self.add_widget(TextInputGrid())
        self.add_widget(ButtonGrid())


class Settings(App):

    def build(self):
        return MainApp()


Settings().run()
