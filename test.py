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
from colorama import init, Fore, Style

class GameTime(tk.Tk):

    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)


        container = tk.Frame(self)
        container.pack(side="top", fill="both",expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)



        self.frames={}

        for F in (StartPage, PageOne):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0,column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()




class StartPage(tk.Frame):

    

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        global Team_Name
        Team_Name = StringVar()
        Team_Name.set('Unassigned')
        global Game_ID
        Game_ID = StringVar()
        Game_ID.set('Unassigned')

        #Declare the team pictures
        pic_Anaheim_Ducks = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Anaheim_Ducks.gif"))
        pic_Boston_Bruins = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Boston_Bruins.gif"))
        pic_Buffalo_Sabres = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Buffalo_Sabres.gif"))
        pic_Calgary_Flames = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Calgary_Flames.gif"))
        pic_Carolina_Hurricanes = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Carolina_Hurricanes.gif"))
        pic_Chicago_Blackhawks = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Chicago_Blackhawks.gif"))
        pic_Colorado_Avalanche = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Colorado_Avalanche.gif"))
        pic_Columbus_Blue_Jackets = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Columbus_Blue_Jackets.gif"))
        pic_Dallas_Stars = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Dallas_Stars.gif"))
        pic_Detroit_Red_Wings = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Detroit_Red_Wings.gif"))
        pic_Edmonton_Oilers = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Edmonton_Oilers.gif"))
        pic_Florida_Panthers = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Florida_Panthers.gif"))
        pic_Los_Angeles_Kings = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Los_Angeles_Kings.gif"))
        pic_Minnesota_Wild = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Minnesota_Wild.gif"))
        pic_Montreal_Canadiens = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Montreal_Canadiens.gif"))
        pic_Nashville_Predators = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Nashville_Predators.gif"))
        pic_New_Jersey_Devils = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/New_Jersey_Devils.gif"))
        pic_New_York_Islanders = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/New_York_Islanders.gif"))
        pic_New_York_Rangers = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/New_York_Rangers.gif"))
        pic_Ottawa_Senators = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Ottawa_Senators.gif"))
        pic_Philadelphia_Flyers = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Philadelphia_Flyers.gif"))
        pic_Phoenix_Coyotes = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Phoenix_Coyotes.gif"))
        pic_Pittsburgh_Penguins = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Pittsburgh_Penguins.gif"))
        pic_San_Jose_Sharks = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/San_Jose_Sharks.gif"))
        pic_St_Louis_Blues = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/St_Louis_Blues.gif"))
        pic_Tampa_Bay_Lightning = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Tampa_Bay_Lightning.gif"))
        pic_Toronto_Maple_Leafs = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Toronto_Maple_Leafs.gif"))
        pic_Vancouver_Canucks = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Vancouver_Canucks.gif"))
        pic_Washington_Capitals = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Washington_Capitals.gif"))
        pic_Winnipeg_Jets = PhotoImage(file=os.path.join(sys._MEIPASS, "NHL_Logos/Winnipeg_Jets.gif"))

        #Declare the buttons with associated team logo/name
        btn_Anaheim_Ducks = Button(self,image=pic_Anaheim_Ducks,text="Anaheim Ducks",compound="top",command=lambda: set_label_to_team("Ducks"))
        btn_Anaheim_Ducks.image = pic_Anaheim_Ducks #Tkinter does handle references to Image objes properly so we need to hold a reference to the internal object. Otherwise the python garbage collector discards it
        btn_Boston_Bruins = Button(self,image=pic_Boston_Bruins,text="Boston Bruins",compound="top",command=lambda: set_label_to_team("Bruins"))
        btn_Boston_Bruins.image = pic_Boston_Bruins
        btn_Buffalo_Sabres = Button(self,image=pic_Buffalo_Sabres,text="Buffalo Sabres",compound="top",command=lambda: set_label_to_team("Sabres"))
        btn_Buffalo_Sabres.image = pic_Buffalo_Sabres
        btn_Calgary_Flames = Button(self,image=pic_Calgary_Flames,text="Calgary Flames",compound="top",command=lambda: set_label_to_team("Flames"))
        btn_Calgary_Flames.image = pic_Calgary_Flames
        btn_Carolina_Hurricanes = Button(self,image=pic_Carolina_Hurricanes,text="Carolina Hurricanes",compound="top",command=lambda: set_label_to_team("Hurricanes"))
        btn_Carolina_Hurricanes.image = pic_Carolina_Hurricanes
        btn_Chicago_Blackhawks = Button(self,image=pic_Chicago_Blackhawks,text="Chicago Blackhawks",compound="top",command=lambda: set_label_to_team("Blackhawks"))
        btn_Chicago_Blackhawks.image = pic_Chicago_Blackhawks
        btn_Colorado_Avalanche = Button(self,image=pic_Colorado_Avalanche,text="Colorado Avalanche",compound="top",command=lambda: set_label_to_team("Avalanche"))
        btn_Colorado_Avalanche.image = pic_Colorado_Avalanche
        btn_Columbus_Blue_Jackets = Button(self,image=pic_Columbus_Blue_Jackets,text="Columbus Blue Jackets",compound="top",command=lambda: set_label_to_team("Blue Jackets"))
        btn_Columbus_Blue_Jackets.image = pic_Columbus_Blue_Jackets
        btn_Dallas_Stars = Button(self,image=pic_Dallas_Stars,text="Dallas Stars",compound="top",command=lambda: set_label_to_team("Stars"))
        btn_Dallas_Stars.image = pic_Dallas_Stars
        btn_Detroit_Red_Wings = Button(self,image=pic_Detroit_Red_Wings,text="Detroit Red Wings",compound="top",command=lambda: set_label_to_team("Red Wings"))
        btn_Detroit_Red_Wings.image = pic_Detroit_Red_Wings
        btn_Edmonton_Oilers = Button(self,image=pic_Edmonton_Oilers,text="Edmonton Oilers",compound="top",command=lambda: set_label_to_team("Oilers"))
        btn_Edmonton_Oilers.image = pic_Edmonton_Oilers
        btn_Florida_Panthers = Button(self,image=pic_Florida_Panthers,text="Florida Panthers",compound="top",command=lambda: set_label_to_team("Panthers"))
        btn_Florida_Panthers.image = pic_Florida_Panthers
        btn_Los_Angeles_Kings = Button(self,image=pic_Los_Angeles_Kings,text="Los Angeles Kings",compound="top",command=lambda: set_label_to_team("Kings"))
        btn_Los_Angeles_Kings.image = pic_Los_Angeles_Kings
        btn_Minnesota_Wild = Button(self,image=pic_Minnesota_Wild,text="Minnesota Wild",compound="top",command=lambda: set_label_to_team("Wild"))
        btn_Minnesota_Wild.image = pic_Minnesota_Wild
        btn_Montreal_Canadiens = Button(self,image=pic_Montreal_Canadiens,text="Montreal Canadiens",compound="top",command=lambda: set_label_to_team("Canadiens"))
        btn_Montreal_Canadiens.image = pic_Montreal_Canadiens
        btn_Nashville_Predators = Button(self,image=pic_Nashville_Predators,text="Nashville Predators",compound="top",command=lambda: set_label_to_team("Predators"))
        btn_Nashville_Predators.image = pic_Nashville_Predators
        btn_New_Jersey_Devils = Button(self,image=pic_New_Jersey_Devils,text="New Jersey Devils",compound="top",command=lambda: set_label_to_team("Devils"))
        btn_New_Jersey_Devils.image = pic_New_Jersey_Devils
        btn_New_York_Islanders = Button(self,image=pic_New_York_Islanders,text="New York Islanders",compound="top",command=lambda: set_label_to_team("Islanders"))
        btn_New_York_Islanders.image = pic_New_York_Islanders
        btn_New_York_Rangers = Button(self,image=pic_New_York_Rangers,text="New York Rangers",compound="top",command=lambda: set_label_to_team("Rangers"))
        btn_New_York_Rangers.image = pic_New_York_Rangers
        btn_Ottawa_Senators = Button(self,image=pic_Ottawa_Senators,text="Ottawa Senators",compound="top",command=lambda: set_label_to_team("Senators"))
        btn_Ottawa_Senators.image = pic_Ottawa_Senators
        btn_Philadelphia_Flyers = Button(self,image=pic_Philadelphia_Flyers,text="Philadelphia Flyers",compound="top",command=lambda: set_label_to_team("Flyers"))
        btn_Philadelphia_Flyers.image = pic_Philadelphia_Flyers
        btn_Phoenix_Coyotes = Button(self,image=pic_Phoenix_Coyotes,text="Phoenix Coyotes",compound="top",command=lambda: set_label_to_team("Coyotes"))
        btn_Phoenix_Coyotes.image = pic_Phoenix_Coyotes
        btn_Pittsburgh_Penguins = Button(self,image=pic_Pittsburgh_Penguins,text="Pittsburgh Penguins",compound="top",command=lambda: set_label_to_team("Penguins"))
        btn_Pittsburgh_Penguins.image = pic_Pittsburgh_Penguins
        btn_San_Jose_Sharks = Button(self,image=pic_San_Jose_Sharks,text="San Jose Sharks",compound="top",command=lambda: set_label_to_team("Sharks"))
        btn_San_Jose_Sharks.image = pic_San_Jose_Sharks
        btn_St_Louis_Blues = Button(self,image=pic_St_Louis_Blues,text="St. Louis Blues",compound="top",command=lambda: set_label_to_team("Blues"))
        btn_St_Louis_Blues.image = pic_St_Louis_Blues
        btn_Tampa_Bay_Lightning = Button(self,image=pic_Tampa_Bay_Lightning,text="Tampa Bay Lightning",compound="top",command=lambda: set_label_to_team("Lightning"))
        btn_Tampa_Bay_Lightning.image = pic_Tampa_Bay_Lightning
        btn_Toronto_Maple_Leafs = Button(self,image=pic_Toronto_Maple_Leafs,text="Toronto Maple Leafs",compound="top",command=lambda: set_label_to_team("Maple Leafs"))
        btn_Toronto_Maple_Leafs.image = pic_Toronto_Maple_Leafs
        btn_Vancouver_Canucks = Button(self,image=pic_Vancouver_Canucks,text="Vancouver Canucks",compound="top",command=lambda: set_label_to_team("Canucks"))
        btn_Vancouver_Canucks.image = pic_Vancouver_Canucks
        btn_Washington_Capitals = Button(self,image=pic_Washington_Capitals,text="Washington Capitals",compound="top",command=lambda: set_label_to_team("Capitals"))
        btn_Washington_Capitals.image = pic_Washington_Capitals
        btn_Winnipeg_Jets = Button(self,image=pic_Winnipeg_Jets,text="Winnipeg Jets",compound="top",command=lambda: set_label_to_team("Jets"))
        btn_Winnipeg_Jets.image = pic_Winnipeg_Jets


        #Organize the buttons in a 5x6 grid
        btn_Anaheim_Ducks.grid(row=1,column=1)
        btn_Boston_Bruins.grid(row=1,column=2)
        btn_Buffalo_Sabres.grid(row=1,column=3)
        btn_Calgary_Flames.grid(row=1,column=4)
        btn_Carolina_Hurricanes.grid(row=1,column=5)
        btn_Chicago_Blackhawks.grid(row=2,column=1)
        btn_Colorado_Avalanche.grid(row=2,column=2)
        btn_Columbus_Blue_Jackets.grid(row=2,column=3)
        btn_Dallas_Stars.grid(row=2,column=4)
        btn_Detroit_Red_Wings.grid(row=2,column=5)
        btn_Edmonton_Oilers.grid(row=3,column=1)
        btn_Florida_Panthers.grid(row=3,column=2)
        btn_Los_Angeles_Kings.grid(row=3,column=3)
        btn_Minnesota_Wild.grid(row=3,column=4)
        btn_Montreal_Canadiens.grid(row=3,column=5)
        btn_Nashville_Predators.grid(row=4,column=1)
        btn_New_Jersey_Devils.grid(row=4,column=2)
        btn_New_York_Islanders.grid(row=4,column=3)
        btn_New_York_Rangers.grid(row=4,column=4)
        btn_Ottawa_Senators.grid(row=4,column=5)
        btn_Philadelphia_Flyers.grid(row=5,column=1)
        btn_Phoenix_Coyotes.grid(row=5,column=2)
        btn_Pittsburgh_Penguins.grid(row=5,column=3)
        btn_San_Jose_Sharks.grid(row=5,column=4)
        btn_St_Louis_Blues.grid(row=5,column=5)
        btn_Tampa_Bay_Lightning.grid(row=6,column=1)
        btn_Toronto_Maple_Leafs.grid(row=6,column=2)
        btn_Vancouver_Canucks.grid(row=6,column=3)
        btn_Washington_Capitals.grid(row=6,column=4)
        btn_Winnipeg_Jets.grid(row=6,column=5)
        
        label = tk.Label(self,text="Start Page")
        label.grid(row=8,column=4)


        lbl_selected_team = tk.Label(self, text="Selected Team: ", anchor="e")
        lbl_selected_team.grid(row=9,column=1)

        lbl_Team_Def = tk.Label(self, textvariable=Team_Name, anchor="w")
        lbl_Team_Def.grid(row=9,column=2)
        
        button = tk.Button(self, text="Visit Page 1",command=lambda: is_team_set(Team_Name))
        button.grid(row=10,column=5)


        def set_label_to_team(some_team_name):
            global Team_Name
            Team_Name.set(some_team_name)
            lbl_Team_Def.config(text=Team_Name, anchor="w")

        def is_team_set(Team_Name):
            if Team_Name.get() == 'Unassigned':
                messagebox.showwarning("Error!", "You must select your favorite team!")
            else:
                controller.show_frame(PageOne)


class PageOne(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
           
        global Team_Name
        global Game_ID

        label = tk.Label(self,text="Page One")      

        button1 = tk.Button(self, text="Back to Home",command=lambda: controller.show_frame(StartPage))
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

app = GameTime()
app.title('GameTime')
#app.wm_iconbitmap('Icon.ico')
app.resizable(0,0)
app.mainloop()
