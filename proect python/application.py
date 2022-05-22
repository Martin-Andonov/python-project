from kivy.app import App            # imports app class
from kivy.uix.label import Label    # imports label class that allows us to create text labels
from kivy.uix.widget import Widget  # imports widget class allows us to create widget objects
from kivy.uix.gridlayout import GridLayout  # imports grid layout
from kivy.uix.button import Button  # imports Button class allows us to create Buttons
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from eventregistry import *
import datetime
import webbrowser
from kivy.uix.spinner import Spinner
import os
import tkinter
API_KEY = "430ca50f-b8c4-4f25-bfed-3d1dbb6118e7"

error_message = {"Note": "Thank you for using Alpha Vantage! Our standard API call"
                         " frequency is 5 calls per minute and 500 calls per day. "
                         "Please visit https://www.alphavantage.co/premium/ "
                         "if you would like to target a higher API call frequency."}


class Sidebar(BoxLayout):
    def __init__(self, **kwargs):
        super(Sidebar, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 160
        self.spacing = 10
        self.number_of_buttons = 0
        self.children_height = 0
        self.orientation = 'vertical'

        with self.canvas:

            Color(1, 1, 1, 0.1)
            self.rect = Rectangle(pos=self.center,
                                  size=(self.width,
                                        self.height))

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

        self.add_widget(Button(text="open schedule settings", background_color=(1, 1, 1, 0.25),
                               size_hint_y=None, height=self.height/2, size_hint_x=None, width=self.width))
        self.add_widget(Button(text="open stock settings", background_color=(1, 1, 1, 0.25),
                               size_hint_y=None, height=self.height/2, size_hint_x=None,  width=self.width))
        self.add_widget(Spinner(text="Choose language", size_hint_y=None,
                                size_hint_x=None, width=self.width, height=self.height/2,
                                values=("english", "spanish"), background_color=(1, 1, 1, 0.25)))
        self.add_widget(Label(text="", size_hint_y=None))

        self.children[2].bind(on_press=lambda x: self.settings_window(self))
        self.children[3].bind(on_press=lambda x: self.schedule_list())

    # update function which makes the canvas adjustable.
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

        # adjusting the Label size so buttons are on top of the widget
        self.number_of_buttons = len(self.children) - 1
        self.children_height = self.children[2].height
        self.children[0].height = self.height - self.number_of_buttons * self.children_height
        self.children[0].height -= self.number_of_buttons * 10

    @staticmethod
    def schedule_list():
        os.system('python schedule_list.py')

    @staticmethod
    def settings_window(self):

        os.system('python settings_window.py')


class StocksGrid(GridLayout):

    def __init__(self, **kwargs):
        super(StocksGrid, self).__init__(**kwargs)
        self.label_text = ""
        self.cols = 2

        self.add_widget(NewsGrid())
        self.add_widget(Label(size_hint_x=None, width=0))

        # calls "update_stock_price" once at the start of the program
        # "lambda dt:" is added to call a function without passing parameters
        Clock.schedule_once(lambda dt: self.update_stock_price(), 1)

        # schedules and event calling "update_stock_price" every 5 minutes
        # "lambda dt:" is added to call a function without passing parameters
        Clock.schedule_interval(lambda dt: self.update_stock_price(), 300)

    def on_size(self, *args):

        if self.width >= 1250:
            # changes the font size of the news labels on resizing the screen
            for child in self.children[1].children:
                child.children[1].font_size = 20

            # if the screen is big enough it activates the stocks window
            self.children[0].width = self.width * 0.2
            self.children[0].font_size = 20
            self.children[0].text = self.label_text
        else:
            # changes the font size of the news labels on resizing the screen
            for child in self.children[1].children:
                child.children[1].font_size = 15

            # if the screen is not big enough it deactivates the stocks window
            self.children[0].width = 0
            self.children[0].font_size = 0
            self.children[0].text = ""

    def update_stock_price(self):
        template = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
        symbol = "&symbol="
        interval = "&interval=5min"
        key = "&apikey=RA66O94G43D93XOV"
        stock_file = open("stocks_list.txt", "r")

        label_output = ""

        for line in stock_file:
            if line != "" and line != " " and line != "\n":

                line = line.strip("\n")
                url = template + symbol + line + interval + key

                # getting the data with the request
                r = requests.get(url)
                data = r.json()

                if data == error_message:
                    if self.children[0].width >= 1250:
                        self.children[0].text = "Error updating the stocks list \n" \
                                                "This will automatically\n update after 5 minutes\n" \
                                                "if the problem continues\n restart the application"
                        self.label_text = self.children[0].text
                    else:
                        self.children[0].text = ""
                        self.label_text = "Error updating the stocks list \n" \
                                          "This will automatically\n update after 5 minutes\n" \
                                          "if the problem continues\n restart the application"
                    return

                # data formatting and string manipulation
                label_output += str(data["Meta Data"]["2. Symbol"]) + ":\n"
                stock_data = data["Time Series (5min)"][data["Meta Data"]["3. Last Refreshed"]]
                label_output += "open:" + str(round(float(stock_data["1. open"]), 2)) + " "
                label_output += "close:" + str(round(float(stock_data["4. close"]), 2)) + "\n"
                label_output += "high:" + str(round(float(stock_data["2. high"]), 2)) + " "
                label_output += "low:" + str(round(float(stock_data["3. low"]), 2)) + "\n"
                label_output += "volume:" + stock_data["5. volume"] + " "
                label_output += "\n\n"

        if self.children[0].width >= 1250:
            self.children[0].text = label_output
            self.label_text = label_output
        else:
            self.children[0].text = ""
            self.label_text = label_output


class SidebarGrid(GridLayout):

    def __init__(self, **kwargs):
        super(SidebarGrid, self).__init__(**kwargs)

        self.cols = 2

        self.add_widget(StocksGrid())
        self.add_widget(Sidebar())


class NavbarGrid(GridLayout):

    def __init__(self, **kwargs):
        super(NavbarGrid, self).__init__(**kwargs)  # calls super constructor with the arguments passed as **kwargs

        self.cols = 5
        self.time = str(datetime.datetime.now().strftime("DATE:"+" %d/%m/%y" + "\nTIME: " + "%H:%M:%S"))

        self.add_widget(Label(text=self.time, font_size=20))
        self.add_widget(Label())
        self.add_widget(Label())

        self.add_widget(Button(text="personal assistant", background_color=(1, 1, 1, 0.5),
                               size_hint_y=None, height=self.height / 2,))
        self.add_widget(Button(text="close settings", background_color=(1, 1, 1, 0.5),
                               size_hint_y=None, height=self.height / 2))

        self.children[0].bind(on_press=lambda x: self.side_bar_toggle())
        self.children[1].bind(on_press=lambda x: self.assistant())

    def side_bar_toggle(self):
        if self.parent.parent.children[0].children[0].width == 0:

            # changes button label when you open/close the sidebar
            self.parent.parent.children[1].children[0].children[0].text = "close settings"

            if self.children[0].width <= 160:
                self.parent.parent.children[0].children[0].width = self.children[0].width

                for child in self.parent.parent.children[0].children[0].children:
                    child.width = self.children[0].width
                    child.font_size = 15

            else:
                self.parent.parent.children[0].children[0].width = 160

                for child in self.parent.parent.children[0].children[0].children:
                    child.width = 160
                    child.font_size = 15

        else:

            # changes button label when you open/close the sidebar
            self.parent.parent.children[1].children[0].children[0].text = "open settings"

            self.parent.parent.children[0].children[0].width = 0

            for child in self.parent.parent.children[0].children[0].children:
                child.x = 0
                child.font_size = 0

    @staticmethod
    def assistant():
        os.system('python personal_asistant.py')


class NavbarCanvas(Widget):

    def __init__(self, **kwargs):

        super(NavbarCanvas, self).__init__(**kwargs)  # calls super constructor with the arguments passed as **kwargs

        # Arranging Canvas
        with self.canvas:
            Color(1, 1, 1, 0.1)  # set the colour

            # Setting the size and position of canvas
            self.rect = Rectangle(pos=self.center,
                                  size=(self.width / 2.,
                                        self.height / 2.))

            # self.add_widget(Label(text="test", pos=self.center, size=self.size))
            self.add_widget(NavbarGrid(height=self.height, pos=self.pos))

            # Update the canvas as the screen size change
            self.bind(pos=self.update_rect,
                      size=self.update_rect)

        # schedules and event calling "update_clock" every 0.5 seconds
        # "lambda dt:" is added to call a function without passing parameters
        Clock.schedule_interval(lambda dt: self.update_clock(), 0.5)

        # schedules and event calling "check schedule" every 59 seconds
        # "lambda dt:" is added to call a function without passing parameters
        Clock.schedule_interval(lambda dt: self.check_schedule(), 59)

    # update function which makes the canvas adjustable.
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

        # updating the label to fit the rect box
        self.children[0].pos = self.pos
        self.children[0].size = self.size

    # function to update the internal clock called every 0.5 seconds
    def update_clock(self):

        self.children[0].children[4].text = str(datetime.datetime.now().strftime("DATE:"+" %d/%m/%y" + "\nTIME: " + "%H:%M:%S"))

    @staticmethod
    def check_schedule(self):
        time_get = datetime.datetime.now().strftime("%d/%m/%y" + " " + "%H:%M" + "\n")
        file = open("schedule.txt", "r+")
        new_schedule = ""
        check = False
        event = ""
        print(file)

        for line in file:
            string = line
            line = line.split("|")

            date_time = line[1].split(" ")
            date = date_time[0] + "/" + date_time[1] + "/" + date_time[2]
            time_of_file = date_time[3] + ":" + date_time[4]
            date_time = date + " " + time_of_file

            if re.search(date_time, time_get):
                check = True
                event = line[0]
            else:
                new_schedule += str(string)

        # rewriting the data in schedule
        file.close()
        file = open("schedule.txt", "w+")
        file.write(new_schedule)
        file.close()

        # alert for event
        if check:
            print_string = event + "event now!!!"

            root = tkinter.Tk()
            root.eval('tk::PlaceWindow . center')
            root.title("WINNER")

            window = tkinter.Text(root, height=2, width=30)
            window.insert(tkinter.END, print_string)
            window.configure(state='disabled')
            window.pack()

            tkinter.mainloop()


class LeadingGrid(GridLayout):

    def __init__(self, **kwargs):

        super(LeadingGrid, self).__init__(**kwargs)  # calls super constructor with the arguments passed as **kwargs

        self.rows = 2
        self.a = self.height

        # self.add_widget(Button(text="empty",  size_hint_y=None, height=100, background_color=(1, 1, 1, 1)))
        # button for test purposes
        # look at this https://www.geeksforgeeks.org/python-canvas-in-kivy/
        # self.add_widget(Label(text="test", size_hint_y=None, height=100))

        self.add_widget(NavbarCanvas(size_hint_y=None, height=80))
        self.add_widget(SidebarGrid())


class News(GridLayout):
    def __init__(self, **kwargs):
        super(News, self).__init__(**kwargs)

        self.url = ""
        self.rows = 2

        self.add_widget(Label(text=""))
        self.add_widget(Button(size_hint_y=None, text="Read more!", height=self.height * 0.5,
                               background_color=(1, 1, 1, 0.5)))

        self.children[0].bind(on_press=lambda x: self.open_link())

    def open_link(self):
        webbrowser.open(self.url)


class NewsGrid(GridLayout):

    def __init__(self, **kwargs):
        super(NewsGrid, self).__init__(**kwargs)

        self.lang = "eng"
        self.theme = ""

        self.cols = 2
        self.rows = 2

        self.add_widget(News())
        self.add_widget(News())
        self.add_widget(News())
        self.add_widget(News())

        # calls "update_news" once at the start of the program
        # "lambda dt:" is added to call a function without passing parameters
        Clock.schedule_once(lambda dt: self.update_news(), 1)

        # schedules and event calling "update_news" every 10 minutes
        # "lambda dt:" is added to call a function without passing parameters
        Clock.schedule_interval(lambda dt: self.update_news(), 600)

    def update_news(self):

        event_register = EventRegistry(apiKey=API_KEY)
        query = QueryArticlesIter(conceptUri=event_register.getConceptUri(self.theme))
        news_counter = 0

        if self.parent.parent.children[0].children[1].text == "english":
            self.lang = "eng"
        elif self.parent.parent.children[0].children[1].text == "spanish":
            self.lang = "spa"

        for article in query.execQuery(event_register, sortBy="date"):

            if article["lang"] == self.lang:

                # makes the title multiline
                title = ""
                words = article["title"].split(" ")
                word_count = 0
                for word in words:

                    if word_count == 5:
                        word_count = 0
                        title += "\n"

                    title += word + " "
                    word_count += 1

                self.children[news_counter].children[1].text = title
                self.children[news_counter].url = article["url"]

                news_counter += 1

            if news_counter == 4:
                break


class Scheduler(App):

    def build(self):
        return LeadingGrid()


Scheduler().run()
