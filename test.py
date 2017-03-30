'''
The first thing is that you need to remember that repetitive tasks are the computer's job. If you find yourself copy / pasteing code you need to make a routine to do that for you. That way you get dynamic, easily updated code (which is pretty much the mantra of python).

Also in the spirit of being dynamic, you need to separate more. Make smaller, more specialized classes and functions. Things that have no GUI interactions don't need to be in a GUI class.
'''

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import os
import sys

import datetime
import json
import platform
import time
import requests
import socket
from functools import partial

#allows this to run in pure python, without freezeing.
try:
    sys._MEIPASS
except AttributeError:
    sys._MEIPASS = ''

# teams in the order that they should be listed as 3-tuples: (city, name, image)
TEAMS = [
    #~ ("Anaheim", "Ducks", "Anaheim_Ducks.gif"),
    #~ ("Boston", " Bruins", "Boston_Bruins.gif"),
    #~ ("Buffalo", " Sabres", "Buffalo_Sabres.gif"),
    #~ ("Calgary", " Flames", "Calgary_Flames.gif"),
    #~ ("Carolina", " Hurricanes", "Carolina_Hurricanes.gif"),
    #~ ("Chicago", " Blackhawks", "Chicago_Blackhawks.gif"),
    #~ ("Colorado", " Avalanche", "Colorado_Avalanche.gif"),
    #~ ("Columbus", " Blue Jackets", "Columbus_Blue_Jackets.gif"),
    #~ ("Dallas", " Stars", "Dallas_Stars.gif"),
    #~ ("Detroit", " Red Wings", "Detroit_Red_Wings.gif"),
    ("Edmonton", " Oilers", "Edmonton_Oilers.gif"),
    ("Florida", " Panthers", "Florida_Panthers.gif"),
    ("Los Angeles", " Kings", "Los_Angeles_Kings.gif"),
    ("Minnesota", " Wild", "Minnesota_Wild.gif"),
    ("Montreal", " Canadiens", "Montreal_Canadiens.gif"),
    ("Nashville", " Predators", "Nashville_Predators.gif"),
    ("New Jersey", " Devils", "New_Jersey_Devils.gif"),
    ("New York", " Islanders", "New_York_Islanders.gif"),
    ("New York", " Rangers", "New_York_Rangers.gif"),
    ("Ottawa", " Senators", "Ottawa_Senators.gif"),
    ("Philadelphia", " Flyers", "Philadelphia_Flyers.gif"),
    ("Phoenix", " Coyotes", "Phoenix_Coyotes.gif"),
    ("Pittsburgh", " Penguins", "Pittsburgh_Penguins.gif"),
    ("San Jose", " Sharks", "San_Jose_Sharks.gif"),
    ("St. Louis", " Blues", "St_Louis_Blues.gif"),
    ("Tampa Bay", " Lightning", "Tampa_Bay_Lightning.gif"),
    ("Toronto", " Maple Leafs", "Toronto_Maple_Leafs.gif"),
    ("Vancouver", " Canucks", "Vancouver_Canucks.gif"),
    ("Washington ", "Capitals", "Washington_Capitals.gif"),
    ("Winnipeg ", "Jets", "Winnipeg_Jets.gif"),
]

COLUMNS = 5

class GameTime(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        master.title('GameTime')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frames={}

        for F in (StartPage, PageOne):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0,column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class TeamGrid(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        for idx, (city, name, image) in enumerate(TEAMS):
            btn = tk.Button(self,
                text="{} {}".format(city, name),
                compound="top",
                command=partial(master.Team_Name.set, name))
            btn.img = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos", image))
            btn.config(image=btn.img)
            row, col = divmod(idx, COLUMNS)
            btn.grid(row=row, column=col)

class StartPage(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.Team_Name = StringVar()
        self.Team_Name.set('Unassigned')

        self.Game_ID = StringVar()
        self.Game_ID.set('Unassigned')

        teams = TeamGrid(self)
        teams.pack()

        lbl_frame = tk.Frame(self) # put these 2 labels in their own frame that can be packed
        lbl_frame.pack()
        lbl_selected_team = tk.Label(lbl_frame, text="Selected Team: ")
        lbl_selected_team.pack(side=tk.LEFT)
        lbl_Team_Def = tk.Label(lbl_frame, textvariable=self.Team_Name)
        lbl_Team_Def.pack()

        button = tk.Button(self, text="Visit Page 1",command=self.is_team_set)
        button.pack()

    def is_team_set(self):
        if self.Team_Name.get() == 'Unassigned':
            messagebox.showwarning("Error!", "You must select your favorite team!")
        else:
            self.master.show_frame(PageOne)

class PageOne(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        Team_Name = master.frames[StartPage].Team_Name
        Game_ID = master.frames[StartPage].Game_ID

        label = tk.Label(self,text="Page One")

        button1 = tk.Button(self, text="Back to Home",command=lambda: master.show_frame(StartPage))
        button1.grid(row=2,column=1)

        notebook = ttk.Notebook(self)
        tab_schedule = ttk.Frame(notebook)
        tab_live_game = ttk.Frame(notebook)
        tab_team_stats = ttk.Frame(notebook)
        tab_standings = ttk.Frame(notebook)
        notebook.add(tab_schedule, text='Schedule')
        notebook.add(tab_live_game, text='Live Game')
        notebook.add(tab_team_stats, text='Team Stats')
        notebook.add(tab_standings, text='Standings')
        notebook.grid(row=1,column=1)

        #********Schedule*********


        vertscroll = tk.Scrollbar(tab_schedule, orient='vertical')
        canvas_schedule = tk.Canvas(tab_schedule,yscrollcommand=vertscroll.set)
        canvas_schedule.pack(side=LEFT,fill="both",expand=True)
        vertscroll.pack(side=LEFT, fill=Y)
        vertscroll.config(command = canvas_schedule.yview)

        label_home_team = tk.Label(canvas_schedule, text="HOME")
        label_home_team.grid(row=1,column=3)

        label_away_team = tk.Label(canvas_schedule, text="AWAY")
        label_away_team.grid(row=1,column=0)


        #********Live Game*********
        lbl_home = tk.Label(tab_live_game, text="AWAY")
        lbl_home.grid(row=1,column=2)

        lbl_away = tk.Label(tab_live_game, text="HOME")
        lbl_away.grid(row=1,column=4)

        lbl_game_id = tk.Label(tab_live_game, text=Game_ID.get())
        lbl_game_id.grid(row=1,column=6)

        #********Team Stats*********

        #********Standings*********


        i = datetime.datetime.now()  # date and time formatting http://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/
        api_url = 'http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp?loadScoreboard=jQuery110105207217424176633_1428694268811&_=1428694268812'
        api_headers = {'Host': 'live.nhle.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', 'Referer': 'http://www.nhl.com/ice/scores.htm'}
        # Format dates to match NHL API style:

        # Todays date
        t = datetime.datetime.now()
        todays_date = "" + t.strftime("%A") + " " + "%s/%s" % (t.month, t.day)
        # Yesterdays date
        y =y = t - datetime.timedelta(days=1)
        yesterdays_date = "" + y.strftime("%A") + " " + "%s/%s" % (y.month, y.day)
        while True:
            try:
                r = requests.get(api_url, headers=api_headers) #making sure there is a connection with the API
            except (requests.ConnectionError): #Catch these errors
                print ("Could not get response from NHL.com trying again...")
                continue
            except(requests.HTTPError):
                print ("HTTP Error when loading url. Please restart program. ")
                sys.exit(0)
            except(requests.Timeout):
                print ("The request took too long to process and timed out. Trying again... ")
            except(socket.error):
                print ("Could not get response from NHL.com trying again...")
            except(requests.RequestException):
                print ("Unknown error. Please restart the program. ")
                sys.exit(0)

            # We get back JSON data with some JS around it, gotta remove the JS
            json_data = r.text

            # Remove the leading JS
            json_data = json_data.replace('loadScoreboard(', '')

            # Remove the trailing ')'
            json_data  = json_data[:-1]

            data = json.loads(json_data)

            #Used to keep track of the number of games played (number of rows on schedule)
            num_games = 2 #start at 2 because row 1 is already used

            for key in data:
                if key == 'games':
                    for game_info in data[key]:
                        # Assign more meaningful names
                        game_clock = game_info['ts']
                        game_stage = game_info['tsc']
                        status = game_info['bs']

                        away_team_locale = game_info['atn']
                        away_team_name = game_info['atv'].title()
                        away_team_score = game_info['ats']
                        away_team_result = game_info['atc']
                        print(away_team_name)


                        home_team_locale = game_info['htn']
                        home_team_name = game_info['htv'].title()
                        home_team_score = game_info['hts']
                        home_team_result = game_info['htc']

                        # Fix strange names / locales returned by NHL
                        #away_team_locale = fix_locale(away_team_locale)
                        #home_team_locale = fix_locale(home_team_locale)
                        #away_team_name = fix_name(away_team_name)
                        #home_team_name = fix_name(home_team_name)


                        label_away = tk.Label(canvas_schedule, text=away_team_name,anchor='w')
                        label_away.grid(row=num_games,column=0,pady=5,sticky=W)

                        label_away_score = tk.Label(canvas_schedule, text=away_team_score)
                        label_away_score.grid(row=num_games,column=1,pady=5)

                        label_vs = tk.Label(canvas_schedule, text="vs")
                        label_vs.grid(row=num_games,column=2,padx=5,pady=5)

                        label_home = tk.Label(canvas_schedule, text=home_team_name,anchor='w')
                        label_home.grid(row=num_games,column=3,pady=5,sticky=W)

                        label_home_score = tk.Label(canvas_schedule, text=home_team_score)
                        label_home_score.grid(row=num_games,column=4,pady=5)

                        label_game_date = tk.Label(canvas_schedule, text=game_clock)
                        label_game_date.grid(row=num_games,column=5,pady=5)

                        label_game_status = tk.Label(canvas_schedule, text=status)
                        label_game_status.grid(row=num_games,column=6,pady=5)

                        num_games = num_games + 1 #increase the number of rows

                        print (Team_Name.get())
                        if str(Team_Name.get()) == str(away_team_name) or str(Team_Name.get()) == str(home_team_name):
                            Game_ID.set(game_info['id'])

            break
            #End while true

def main():
    root = tk.Tk()
    app = GameTime(root)
    app.pack()
    try:
        root.wm_iconbitmap('Icon.ico')
    except tk.TclError:
        print("icon load failed") # fails in some conditions
    root.resizable(0,0)
    root.mainloop()

if __name__ == "__main__":
    main()

