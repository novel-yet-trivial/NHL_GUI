'''
The first thing is that you need to remember that repetitive tasks are the computer's job. If you find yourself copy / pasteing code you need to make a routine to do that for you. That way you get dynamic, easily updated code (which is pretty much the mantra of python).

Note how in this new code you can eaisly remove, add or reorganize teams. Or adjut how many columns to use. That would have taken a huge amount of work in the old code.

Also in the spirit of being dynamic, you need to separate more. Make smaller, more specialized classes and functions. Things that have no GUI interactions don't need to be in a GUI class.
'''

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import os
import sys
import datetime
import json
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
    ("Anaheim", "Ducks", "Anaheim_Ducks.gif"),
    ("Boston", "Bruins", "Boston_Bruins.gif"),
    ("Buffalo", "Sabres", "Buffalo_Sabres.gif"),
    ("Calgary", "Flames", "Calgary_Flames.gif"),
    ("Carolina", "Hurricanes", "Carolina_Hurricanes.gif"),
    ("Chicago", "Blackhawks", "Chicago_Blackhawks.gif"),
    ("Colorado", "Avalanche", "Colorado_Avalanche.gif"),
    ("Columbus", "Blue Jackets", "Columbus_Blue_Jackets.gif"),
    ("Dallas", "Stars", "Dallas_Stars.gif"),
    ("Detroit", "Red Wings", "Detroit_Red_Wings.gif"),
    ("Edmonton", "Oilers", "Edmonton_Oilers.gif"),
    ("Florida", "Panthers", "Florida_Panthers.gif"),
    ("Los Angeles", "Kings", "Los_Angeles_Kings.gif"),
    ("Minnesota", "Wild", "Minnesota_Wild.gif"),
    ("Montreal", "Canadiens", "Montreal_Canadiens.gif"),
    ("Nashville", "Predators", "Nashville_Predators.gif"),
    ("New Jersey", "Devils", "New_Jersey_Devils.gif"),
    ("New York", "Islanders", "New_York_Islanders.gif"),
    ("New York", "Rangers", "New_York_Rangers.gif"),
    ("Ottawa", "Senators", "Ottawa_Senators.gif"),
    ("Philadelphia", "Flyers", "Philadelphia_Flyers.gif"),
    ("Phoenix", "Coyotes", "Phoenix_Coyotes.gif"),
    ("Pittsburgh", "Penguins", "Pittsburgh_Penguins.gif"),
    ("San Jose", "Sharks", "San_Jose_Sharks.gif"),
    ("St. Louis", "Blues", "St_Louis_Blues.gif"),
    ("Tampa Bay", "Lightning", "Tampa_Bay_Lightning.gif"),
    ("Toronto", "Maple Leafs", "Toronto_Maple_Leafs.gif"),
    ("Vancouver", "Canucks", "Vancouver_Canucks.gif"),
    ("Washington", "Capitals", "Washington_Capitals.gif"),
    ("Winnipeg", "Jets", "Winnipeg_Jets.gif"),
]

COLUMNS = 7

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
            btn.img = tk.PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos", image))
            btn.config(image=btn.img)
            row, col = divmod(idx, COLUMNS)
            btn.grid(row=row, column=col)

class StartPage(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.Team_Name = tk.StringVar()
        self.Team_Name.set('Unassigned')

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

class Schedule(ttk.Frame):
    def __init__(self, master=None, highlight='', **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)

        self.error_lbl = tk.Label(self, fg="red")
        self.error_lbl.place(relx=.5, rely=.5)

        self.tree = ttk.Treeview(self)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(self)
        vsb.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        vsb.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.tag_configure('fav', background="blue")

        col_headers = ("Away", "", "Home", "", "Clock", "Status")
        col_widths = (100, 20, 100, 20, 150, 100)

        columns = list(map(str, range(len(col_headers))))
        self.tree.config(columns=columns)
        self.tree.column('#0',width=0, minwidth=0)
        for col, name, width in zip(columns, col_headers, col_widths):
            self.tree.heading(col, text=name)
            self.tree.column(col,width=width, minwidth=20)

    def update(self, highlight=''):
        #clear out previous values
        self.tree.delete(*self.tree.get_children())

        data = get_data()

        if isinstance(data, str):
            # an error occured
            self.error_lbl.config(text=data)
            self.error_lbl.tkraise()
            return

        self.tree.tkraise()

        #Populate data in the treeview
        for game_info in data['games']:
            # Assign more meaningful names - why is there so many unused variables here?
            game_clock = game_info['ts']
            #~ game_stage = game_info['tsc']
            status = game_info['bs']

            #~ away_team_locale = game_info['atn']
            away_team_name = game_info['atv'].title()
            away_team_score = game_info['ats']
            #~ away_team_result = game_info['atc']

            #~ home_team_locale = game_info['htn']
            home_team_name = game_info['htv'].title()
            home_team_score = game_info['hts']
            #~ home_team_result = game_info['htc']

            row = away_team_name, away_team_score, home_team_name, home_team_score, game_clock, status

            tags='none'
            if row[0] == highlight or row[2] == highlight:
                tags = 'fav'
                self.master.master.Game_ID.set(game_info['id'])
            self.tree.insert('', 'end',values = row, tags=tags)

class LiveGame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        lbl_home = tk.Label(self, text="AWAY")
        lbl_home.grid(row=1,column=2)

        lbl_away = tk.Label(self, text="HOME")
        lbl_away.grid(row=1,column=4)

        lbl_game_id = tk.Label(self, textvariable=master.master.Game_ID)
        lbl_game_id.grid(row=1,column=6)

class PageOne(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.Game_ID = tk.StringVar(self)
        self.Game_ID.set('Unassigned')

        button1 = tk.Button(self, text="Back to Home",command=lambda: master.show_frame(StartPage))
        button1.grid(row=2,column=1)

        notebook = ttk.Notebook(self)
        self.tab_schedule = Schedule(notebook)
        tab_live_game = LiveGame(notebook)
        tab_team_stats = ttk.Frame(notebook)
        tab_standings = ttk.Frame(notebook)
        notebook.add(self.tab_schedule, text='Schedule')
        notebook.add(tab_live_game, text='Live Game')
        notebook.add(tab_team_stats, text='Team Stats')
        notebook.add(tab_standings, text='Standings')
        notebook.grid(row=1,column=1)

    def tkraise(self):
        '''called when this frame is opened'''
        tk.Frame.tkraise(self)
        self.after(10, self.tab_schedule.update, self.master.frames[StartPage].Team_Name.get())

def get_data():
    api_url = 'http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp?loadScoreboard=jQuery110105207217424176633_1428694268811&_=1428694268812'
    api_headers = {'Host': 'live.nhle.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', 'Referer': 'http://www.nhl.com/ice/scores.htm'}

    try:
        r = requests.get(api_url, headers=api_headers) #making sure there is a connection with the API
    except (requests.ConnectionError): #Catch these errors
        return "Could not get response from NHL.com trying again..."
    except(requests.HTTPError):
        return "HTTP Error when loading url. Please restart program. "
    except(requests.Timeout):
        return "The request took too long to process and timed out. Trying again... "
    except(socket.error):
        return "Could not get response from NHL.com trying again..."
    except(requests.RequestException):
        return "Unknown error. Please restart the program. "
    # We get back JSON data with some JS around it, gotta remove the JS
    json_data = r.text

    # Remove the leading JS
    json_data = json_data.replace('loadScoreboard(', '')

    # Remove the trailing ')'
    json_data  = json_data[:-1]

    data = json.loads(json_data)

    if 'games' not in data:
        return "ERROR: no games found"

    return data

#~ def get_data():
    #~ '''uncomment this to debug'''
    #~ with open('nhl_data.json') as f:
        #~ return json.load(f)

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

