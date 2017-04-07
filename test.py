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
    ("Columbus", "Bluejackets", "Columbus_Blue_Jackets.gif"),
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

        self.tree.tag_configure('fav', background="light grey")

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

        self.lbl_home = tk.Label(self, text="AWAY")
        self.lbl_home.grid(row=1,column=2)

        self.lbl_away = tk.Label(self, text="HOME")
        self.lbl_away.grid(row=1,column=4)

        self.lbl_game_id = tk.Label(self, textvariable=master.master.Game_ID)
        self.lbl_game_id.grid(row=1,column=6)

        self.lbl_game = tk.Label(self)
        self.lbl_game.grid(row=25,column=4)

        self.lbl_away_name = tk.Label(self, text="", font="-weight bold")
        self.lbl_away_name.grid(row=3,column=2)

        self.lbl_away_score = tk.Label(self, text="")
        self.lbl_away_score.grid(row=3,column=3)

        self.lbl_home_name = tk.Label(self, text="", font="-weight bold")
        self.lbl_home_name.grid(row=3,column=4)

        self.lbl_home_score = tk.Label(self, text="")
        self.lbl_home_score.grid(row=3,column=5)

        self.lbl_current_play = tk.Label(self, text="",font=(None, 12), anchor='w')
        self.lbl_current_play.grid(row=20,column=3)

    def autoupdate_url(self):
        self.update_url()
        self.after(30000 , self.autoupdate_url)

    def update_url(self):
        game_id = self.master.master.Game_ID.get()
        if game_id == "Unassigned":
            self.lbl_game.config(text="There is no live game!", font=(None, 30, 'bold'))
        else:
            url = 'http://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(game_id)
            j = requests.get(url).json()
            self.lbl_game.config(text=url)

            #Away team name heading
            self.lbl_away_name.config(text=j['gameData']['teams']['away']['name'])
            #Away team score heading
            self.lbl_away_score.config(text=j['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['goals'])
            #Home team name heading
            self.lbl_home_name.config(text=j['gameData']['teams']['home']['name'])
            #Home team score heading
            self.lbl_home_score.config(text=j['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['goals'])
            x = 4
            #Displays away team stats about current game
            for awayteam,value in j['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats'].items():
                self.lbl_away_data_col = tk.Label(self, text=awayteam)
                self.lbl_away_data_col.grid(row=x,column=2)
                self.lbl_away_data_col.config(text=awayteam)
                self.lbl_away_data_val = tk.Label(self, text=value)
                self.lbl_away_data_val.grid(row=x,column=3)
                self.lbl_away_data_val.config(text=value)
                x = x + 1

            x = 4
            #Displays home team stats about the current game
            for hometeam,value in j['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats'].items():
                self.lbl_home_data_col = tk.Label(self, text=hometeam)
                self.lbl_home_data_col.grid(row=x,column=4)
                self.lbl_home_data_col.config(text=hometeam)
                self.lbl_home_data_value = tk.Label(self, text=value)
                self.lbl_home_data_value.grid(row=x,column=5)
                self.lbl_home_data_value.config(text=value)
                x = x + 1

            #Just adds two blank rows between the game stats and the current play
            spacer = tk.Label(self, text="            ")
            spacer.grid(row=18,column=2)
            spacer = tk.Label(self, text="            ")
            spacer.grid(row=19,column=2)

            #Static label
            lbl_play_description = tk.Label(self, text="Current Play: ",font=(None, 12))
            lbl_play_description.grid(row=20,column=2)
            #Text description of the current play
            try:
                self.lbl_current_play.config(text=j['liveData']['plays']['currentPlay']['result']['description'])
            except:
                self.lbl_current_play.config(text="No current play.")


class Player_Stats(ttk.Frame):
    def __init__(self, master=None, highlight='', **kwargs):
        ttk.Frame.__init__(self, master, width=500, height=500, **kwargs)
        self.grid_propagate(False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.error_lbl = tk.Label(self, fg="red")
        self.error_lbl.place(relx=.5, rely=.5)

        self.tree = ttk.Treeview(self)
        self.tree.grid(row=0, column=0, sticky='nsew')

        #Vertical Scroll
        vsb = ttk.Scrollbar(self)
        vsb.grid(row=0, column=1, sticky='ns')
        vsb.configure(command=self.tree.yview)

        #Horizontal Scroll
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        hsb.grid(row=1, column=0, sticky='ew')
        hsb.configure(command=self.tree.xview)

        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.configure(xscrollcommand=hsb.set)

        #Column header titles
        col_headers = ("Player", "Time on Ice",  "Assists",  "Goals", "Shots",  "Hits",  "Power Play Goals", "Power Play Assits",  "Penalty Minutes", "Faceoff Wins",  "Faceoffs Taken",  "Takeaways",  "Giveaways",  "Short Handed Goals",  "Short Handed Assists",  "Shots Blocked",  "+/-",  "Even Time on Ice",  "Powerplay Time on Ice",  "Short Handed Time on Ice")

        columns = list(map(str, range(len(col_headers))))
        self.tree.config(columns=columns)
        self.tree.column('#0',width=0, minwidth=0)

        '''this method adjusts all the columns to the same width'''
        #~ for col, name in zip(columns, col_headers):
            #~ self.tree.heading(col, text=name)
            #~ self.tree.column(col, width=150, minwidth=20)

        '''this method uses a list of widths to make each column a unique width'''
        col_widths = [120, 90, 60, 50, 50, 40, 140, 150, 135, 110, 120, 90, 90, 140, 160, 110, 30, 140, 180, 200]
        for col, name, width in zip(self.tree['columns'], col_headers, col_widths):
            self.tree.heading(col, text=name)
            self.tree.column(col, width=width, minwidth=20)

    def update_player_stats(self,game_id, highlight=''):

        #Clear out the stats from the old tree
        self.tree.delete(*self.tree.get_children())
        self.tree.tkraise()

        url = 'http://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(game_id)
        j = requests.get(url).json()
        away_team = j['gameData']['teams']['away']['name']
        #Show away team name in first row
        self.tree.insert('', 'end',values = (away_team , " ",  " ",  " ", " ",  " ",  " ", " ",  " ", " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " "))
        #Get and display player stats
        for awayplayer in j['liveData']['boxscore']['teams']['away']['players']:
            try:
                away_player_name = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['person']['fullName']
                away_timeOnIce = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['timeOnIce']
                away_assists = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['assists']
                away_goals = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['goals']
                away_shots = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['shots']
                away_hits = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['hits']
                away_powerPlayGoals = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['powerPlayGoals']
                away_powerPlayAssists = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['powerPlayAssists']
                away_penaltyMinutes = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['penaltyMinutes']
                away_faceOffWins = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['faceOffWins']
                away_faceoffTaken = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['faceoffTaken']
                away_takeaways = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['takeaways']
                away_giveaways = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['giveaways']
                away_shortHandedGoals = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['shortHandedGoals']
                away_shortHandedAssists = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['shortHandedAssists']
                away_blocked = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['blocked']
                away_plusMinus = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['plusMinus']
                away_evenTimeOnIce = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['evenTimeOnIce']
                away_powerPlayTimeOnIce = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['powerPlayTimeOnIce']
                away_shortHandedTimeOnIce = j['liveData']['boxscore']['teams']['away']['players'][awayplayer]['stats']['skaterStats']['shortHandedTimeOnIce']
            #If player didn't play OR play is a goalie... Need to work on a goalie stat page
            except:
                away_timeOnIce = "DNP"
                away_assists ="DNP"
                away_goals = "DNP"
                away_shots = "DNP"
                away_hits = "DNP"
                away_powerPlayGoals ="DNP"
                away_powerPlayAssists ="DNP"
                away_penaltyMinutes = "DNP"
                away_faceOffWins ="DNP"
                away_faceoffTaken = "DNP"
                away_takeaways = "DNP"
                away_giveaways = "DNP"
                away_shortHandedGoals = "DNP"
                away_shortHandedAssists ="DNP"
                away_blocked = "DNP"
                away_plusMinus = "DNP"
                away_evenTimeOnIce = "DNP"
                away_powerPlayTimeOnIce = "DNP"
                away_shortHandedTimeOnIce = "DNP"
            #Put all the stats in a variable
            row = away_player_name, away_timeOnIce, away_assists, away_goals, away_shots, away_hits, away_powerPlayGoals, away_powerPlayAssists, away_penaltyMinutes, away_faceOffWins, away_faceoffTaken, away_takeaways, away_giveaways, away_shortHandedGoals, away_shortHandedAssists, away_blocked, away_plusMinus, away_evenTimeOnIce, away_powerPlayTimeOnIce, away_shortHandedTimeOnIce
            #Insert the values into the tree
            self.tree.insert('', 'end',values = row)

        #Create some spacing to distinguish a new teams stats
        self.tree.insert('', 'end',values = (" " , " ",  " ",  " ", " ",  " ",  " ", " ",  " ", " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " "))
        self.tree.insert('', 'end',values = ("*******************", "**************",  "**************",  "**************", "**************",  "**************",  "**************", "**************",  "**************", "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************"))
        self.tree.insert('', 'end',values = ("*******************", "**************",  "**************",  "**************", "**************",  "**************",  "**************", "**************",  "**************", "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************"))
        self.tree.insert('', 'end',values = ("*******************", "**************",  "**************",  "**************", "**************",  "**************",  "**************", "**************",  "**************", "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************",  "**************"))
        self.tree.insert('', 'end',values = (" " , " ",  " ",  " ", " ",  " ",  " ", " ",  " ", " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " "))
        home_team = j['gameData']['teams']['home']['name']
        #Show home team name
        self.tree.insert('', 'end',values = (home_team , " ",  " ",  " ", " ",  " ",  " ", " ",  " ", " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " "))
        #Display home player stats
        for homeplayer in j['liveData']['boxscore']['teams']['home']['players']:
            try:
                home_player_name = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['person']['fullName']
                home_timeOnIce = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['timeOnIce']
                home_assists = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['assists']
                home_goals = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['goals']
                home_shots = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['shots']
                home_hits = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['hits']
                home_powerPlayGoals = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['powerPlayGoals']
                home_powerPlayAssists = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['powerPlayAssists']
                home_penaltyMinutes = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['penaltyMinutes']
                home_faceOffWins = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['faceOffWins']
                home_faceoffTaken = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['faceoffTaken']
                home_takeaways = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['takeaways']
                home_giveaways = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['giveaways']
                home_shortHandedGoals = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['shortHandedGoals']
                home_shortHandedAssists = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['shortHandedAssists']
                home_blocked = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['blocked']
                home_plusMinus = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['plusMinus']
                home_evenTimeOnIce = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['evenTimeOnIce']
                home_powerPlayTimeOnIce = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['powerPlayTimeOnIce']
                home_shortHandedTimeOnIce = j['liveData']['boxscore']['teams']['home']['players'][homeplayer]['stats']['skaterStats']['shortHandedTimeOnIce']
            #If player didn't play OR play is a goalie... Need to work on a goalie stat page
            except:
                home_timeOnIce = "DNP"
                home_assists ="DNP"
                home_goals = "DNP"
                home_shots = "DNP"
                home_hits = "DNP"
                home_powerPlayGoals ="DNP"
                home_powerPlayAssists ="DNP"
                home_penaltyMinutes = "DNP"
                home_faceOffWins ="DNP"
                home_faceoffTaken = "DNP"
                home_takeaways = "DNP"
                home_giveaways = "DNP"
                home_shortHandedGoals = "DNP"
                home_shortHandedAssists ="DNP"
                home_blocked = "DNP"
                home_plusMinus = "DNP"
                home_evenTimeOnIce = "DNP"
                home_powerPlayTimeOnIce = "DNP"
                home_shortHandedTimeOnIce = "DNP"
            #Put all the stats in a variable
            row = home_player_name, home_timeOnIce, home_assists , home_goals, home_shots, home_hits, home_powerPlayGoals, home_powerPlayAssists, home_penaltyMinutes, home_faceOffWins, home_faceoffTaken, home_takeaways, home_giveaways, home_shortHandedGoals, home_shortHandedAssists, home_blocked, home_plusMinus, home_evenTimeOnIce, home_powerPlayTimeOnIce, home_shortHandedTimeOnIce
            self.tree.insert('', 'end',values = row)


class Standings(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        lbl_home = tk.Label(self, text="Metropolitan",font="-weight bold")
        lbl_home.grid(row=1,column=2)

        #Just adds empty space horizontally between Metropolitan and Atlantic
        lbl_spacer = tk.Label(self, text="                      ")
        lbl_spacer.grid(row=1,column=3)

        lbl_away = tk.Label(self, text="Atlantic",font="-weight bold")
        lbl_away.grid(row=1,column=5)

        lbl_home = tk.Label(self, text="Central",font="-weight bold")
        lbl_home.grid(row=10,column=2)

        lbl_away = tk.Label(self, text="Pacific",font="-weight bold")
        lbl_away.grid(row=10,column=5)

    def make_standings(self):
        #Full standings JSON URL
        url = "https://statsapi.web.nhl.com/api/v1/standings?expand=standings.record,standings.team,standings.division,standings.conference,team.schedule.next,team.schedule.previous&season=20162017"
        j = requests.get(url).json()
        #X is the index number of the position with in the division
        x = 0
        #Row number where to place the data on the page
        row = 2
        #The position seed in the division
        place = 1
        #Metropolitan division
        for record in j['records'][0]['teamRecords']:
            #Seeding number in division
            lbl_position = tk.Label(self,text=str(place) + ': ')
            lbl_position.grid(row=row,column=1)
            #Team name
            team_lbl = tk.Label(self, text=j['records'][0]['teamRecords'][x]['team']['name'])
            team_lbl.grid(row=row,column=2)
            team_lbl.config(text=j['records'][0]['teamRecords'][x]['team']['name'])
            #Increase the index to the next team
            x = x + 1
            #Increase the seed number
            place = place + 1
            #Increase the row
            row = row + 1
        #Initilize
        x = 0
        row = 2
        place = 1
        #Atlantic division
        for record in j['records'][1]['teamRecords']:
            lbl_position = tk.Label(self,text=str(place) + ': ')
            lbl_position.grid(row=row,column=4)
            team_lbl = tk.Label(self, text=j['records'][1]['teamRecords'][x]['team']['name'])
            team_lbl.grid(row=row,column=5)
            team_lbl.config(text=j['records'][1]['teamRecords'][x]['team']['name'])
            x = x + 1
            place = place + 1
            row = row + 1
        x = 0
        row = 11
        place = 1
        #Central division
        for record in j['records'][2]['teamRecords']:
            lbl_position = tk.Label(self,text=str(place) + ': ')
            lbl_position.grid(row=row,column=1)
            team_lbl = tk.Label(self, text=j['records'][2]['teamRecords'][x]['team']['name'])
            team_lbl.grid(row=row,column=2)
            team_lbl.config(text=j['records'][2]['teamRecords'][x]['team']['name'])
            x = x + 1
            place = place + 1
            row = row + 1
        x = 0
        row = 11
        place = 1
        #Pacific division
        for record in j['records'][3]['teamRecords']:
            lbl_position = tk.Label(self,text=str(place) + ': ')
            lbl_position.grid(row=row,column=4)
            team_lbl = tk.Label(self, text=j['records'][3]['teamRecords'][x]['team']['name'])
            team_lbl.grid(row=row,column=5)
            team_lbl.config(text=j['records'][3]['teamRecords'][x]['team']['name'])
            x = x + 1
            place = place + 1
            row = row + 1


class PageOne(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.Game_ID = tk.StringVar(self)
        self.Game_ID.set('Unassigned')

        button1 = tk.Button(self, text="Back to Home",command=lambda: master.show_frame(StartPage))
        button1.grid(row=2,column=1)

        notebook = ttk.Notebook(self)
        notebook.bind("<<NotebookTabChanged>>", self.tab_change)
        self.tab_schedule = Schedule(notebook)
        self.tab_live_game = LiveGame(notebook)
        self.tab_team_stats = Player_Stats(notebook)
        self.tab_standings = Standings(notebook)
        notebook.add(self.tab_schedule, text='Schedule')
        notebook.add(self.tab_live_game, text='Live Game')
        notebook.add(self.tab_team_stats, text='Player Stats')
        notebook.add(self.tab_standings, text='Standings')
        notebook.grid(row=1,column=1)

    def tab_change(self, event=None):
        tab = event.widget.tab(event.widget.index("current"))['text']
        if tab == 'Live Game':
            self.tab_live_game.update_url()
        if tab == 'Standings':
            self.tab_standings.make_standings()
        if tab == 'Player Stats':
            self.tab_team_stats.update_player_stats(self.Game_ID.get())

    def tkraise(self):
        '''called when this frame is opened'''
        tk.Frame.tkraise(self)
        self.update()
        self.tab_schedule.update(self.master.frames[StartPage].Team_Name.get())

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
    app.frames[PageOne].tab_live_game.autoupdate_url()
    root.mainloop()

#~ def main():
    #~ root = tk.Tk()
    #~ app = Player_Stats(root)
    #~ app.pack(fill=tk.BOTH, expand=True)
    #~ root.mainloop()

if __name__ == "__main__":
    main()
