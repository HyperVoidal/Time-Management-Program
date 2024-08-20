import pyautogui
import time
import matplotlib.pyplot as plt
import numpy as np
import os
import threading
import json
import traceback

truepath = os.path.dirname(os.path.abspath(__file__))
path = truepath  + "\\static\\AppReaderData.json"
fig, ax = plt.subplots(figsize=(7,4))
columngraphpath = truepath + "\\static\\Column.png"
piechartpath = truepath + "\\static\\Pie.png"
timedisplay = "Seconds"

class AppReader():
    def __init__(self):
        self.start_time = time.time()
        self.appsrunning = []
        self.apptime = {}
        self.appslist = {}

    def AppNameEdit(self):
        #Add another name editor for app names that are part of the same action but have different names
        #e.g. mozilla firefox - new tab, and mozilla firefox - stackoverflow, should become the same name
        modified_apps = []  # Initialize a new list for modified titles
        for x in self.appsrunning:
            titletest = x
            if titletest in ["", " ", "    ", " - "]:  # Simplified check for empty or specific strings
                titletest = "UNKNOWN APP"
            if " - " in titletest:
                thetitletest = titletest.split(" - ")
                titletest = thetitletest[-1]
            if "\\" in titletest:
                thetitletest = titletest.split("\\")
                titletest = thetitletest[-1]
            if " - " not in titletest:
                titletest = titletest
            modified_apps.append(titletest)  # Append the modified title to the new list
        self.appsrunning.clear()
        self.appsrunning = modified_apps  # Replace the original list with the modified list
    
    def AppRunning(self):
        self.appsrunning.extend([window.title for window in pyautogui.getAllWindows()])
        self.appsrunning = [x for x in self.appsrunning if x.strip() and x != ""]
        seen = set()
        self.appsrunning = [x for x in self.appsrunning if not (x in seen or seen.add(x))]
    
    def UpdateRunningApps(self):
        # Fetch the current list of running apps
        current_running_apps = [window.title for window in pyautogui.getAllWindows()]
        current_running_apps = [x for x in current_running_apps if x.strip() and x != ""]

        # Filter out apps that are no longer running from self.appsrunning
        # Do not modify self.apptime here to ensure time persists
        self.appsrunning = [app for app in self.appsrunning if app in current_running_apps]

    def AppTimer(self):
        current_time = round(time.time())  # Ensure current_time is rounded at the source
        for app in self.appsrunning:
            if app in self.apptime:
                # Validate appchoose is a dictionary and has 'cur_time'
                if isinstance(self.apptime[app], dict) and 'cur_time' in self.apptime[app]:
                    appchoose = self.apptime[app]
                    # Ensure elapsed_time is rounded immediately after calculation
                    elapsed_times = int(round(current_time - appchoose['cur_time']))
                    elapsed_time = round(elapsed_times, 0)
                    self.apptime[app]['elapsed'] = elapsed_time  # Convert to int to ensure compatibility
                else:
                    print(f"Error: appchoose for {app} is not properly formatted. Current value: {self.apptime[app]}")
            else:
                # For new apps, ensure 'cur_time' is rounded before being set
                self.apptime[app] = {'cur_time': round(current_time, 0), 'elapsed': 0}  # current_time is already rounded
                
    def AppRelease(self):
        #Sorting algorith here - descending order
        self.apptime = dict(sorted(self.apptime.items(), key=lambda x: x[1]['elapsed'], reverse=True))

        for app_name, time in self.apptime.items():
            # Update the time for the app in self.appslist
            self.appslist[app_name] = (f"{time['elapsed']} seconds")
        

def update_graph(timedisplay):
    try:
        ax.clear()
        smalllist = {}
        smalllist = AppReader.appslist
        #If there are more than 15 apps, only display the top 15
        if len(smalllist) > 25:
            smalllist = dict(list(smalllist.items())[:25])
        app_names = list(smalllist.keys())
        for i in (smalllist.values()):
            values = i.split(" ")
            value = values[0]
            maximum = max([int(round(float(value.split(" ")[0]), 0)) for value in smalllist.values()])
            if maximum > 60 and maximum < 3600:
                timedisplay = "Minutes"
                break
            elif maximum > 3600:
                timedisplay = "Hours"
                break
            elif maximum > 86400:
                timedisplay = "Days"
                break
            else:
                pass
            
        if timedisplay == "Seconds":
            times = [int(round(float(time.split(" ")[0]), 0)) for time in smalllist.values()]
        elif timedisplay == "Minutes":
            times = [(int(round(float(time.split(' ')[0]), 0)))/60 for time in smalllist.values()]
        elif timedisplay == "Hours":
            times = [(int(round(float(time.split(" ")[0]), 0)))/3600 for time in smalllist.values()]
        elif timedisplay == "Days":
            times = [(int(round(float(time.split(" ")[0]), 0)))/86400 for time in smalllist.values()]
        else:
            print("Error: Invalid time display. Defaulting to hours.")
            times = [(int(round(float(time.split(" ")[0]), 0)))/3600 for time in smalllist.values()]
            timedisplay = "Hours"
                
        color_indices = np.arange(len(app_names))
        cmap = plt.colormaps.get_cmap("viridis")
        colors = [cmap(index*15) for index in color_indices]
        appernames = []
        appernames.extend(app_names)
        for i in range(len(app_names)):
            for i in range(len(app_names)):
                if len(app_names[i]) > 23:
                    theappnames = app_names[i][:20] + "..."
                    appernames[i] = theappnames

        ax.bar(appernames, times, color=colors, edgecolor="black")
        ax.set_xlabel('App Name')
        ax.set_ylabel(f'Time ({timedisplay})')
        ax.set_title('App Usage Time')
        plt.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray", axis="y")
        plt.xticks(rotation = 45, ha="right")
        plt.subplots_adjust(left=0.2,bottom=0.4, top = 0.9, right = 0.9)
        plt.savefig(columngraphpath)
    except Exception as e:
        print("GRAPH ERROR:")
        print(e)
        print(traceback.format_exc())
        time.sleep(2)
        pass

    return timedisplay

def piechart():
    try:
        ax.clear()
        smalllist = {}
        smalllist = AppReader.appslist
        #If there are more than 10 apps, only display the top 10
        if len(smalllist) > 10:
            otherlist = dict(list(smalllist.items())[9:])
            otherlist = [int(round(float(time.split(" ")[0]), 0)) for time in otherlist.values()]
            totalsum = 0
            for i in range(len(otherlist)):
                totalsum += otherlist[i]
            smalllist = dict(list(smalllist.items())[:9])
            smalllist["Other"] = f"{totalsum} seconds"
        #Sort smalllist from largest to smallest value
        smalllist = dict(sorted(smalllist.items(), key=lambda x: int(round(float(x[1].split(" ")[0]), 0)), reverse=True))
        
            
                        
        app_names = list(smalllist.keys())
        total = 0
        for i in (smalllist.values()):
            total += int(round(float(i.split(" ")[0]), 0))
        
        appernames = []
        appernames.extend(app_names)
        for i in range(len(app_names)):
            for i in range(len(app_names)):
                if len(app_names[i]) > 23:
                    theappnames = app_names[i][:20] + "..."
                    appernames[i] = theappnames
                    
        times = [int(round(float(time.split(" ")[0]), 0)) for time in smalllist.values()]
        color_indices = np.arange(len(appernames))
        cmap = plt.colormaps.get_cmap("viridis")
        colors = [cmap(index*15) for index in color_indices]
        ax.pie(times, autopct='%1.1f%%', startangle=0, colors=colors)
        ax.axis('equal')
        ax.set_title('App Usage Time')
        ax.legend(appernames, title="Legend", loc="center left", bbox_to_anchor=(-0.1, 0))
        plt.subplots_adjust(left=0.2,bottom=0.4, top = 0.9, right = 0.9)
        plt.savefig(piechartpath)
        
    except Exception as e:
        print("GRAPH ERROR:")
        print(e)
        print(traceback.format_exc())
        time.sleep(2)
        pass

#Recommended next avenue is to add alternative graph methods such as pie chart and/or time based records e.g. previous day, week, month, year.
    
def scan():
    while True:
        AppReader.AppRunning(AppReader)
        AppReader.UpdateRunningApps(AppReader)
        AppReader.AppNameEdit(AppReader)
        AppReader.AppTimer(AppReader)
        AppReader.AppRelease(AppReader)

#Update json and store json need to be edited to account for apptime library changes
def UpdateJson(apptime, path):
    with open (f"{path}", "w") as f:
        json.dump(apptime, f)
    
        
AppReader.__init__(AppReader)

#Load the previously stored json data
try:
    with open(f"{path}", "r") as f:
        appnamelist = json.load(f)
        AppReader.appsrunning = list(appnamelist.keys())
        AppReader.apptime.update(dict(appnamelist))
        AppReader.apptime = appnamelist
        
except:
    pass
thread = threading.Thread(target=scan)
    
thread.start()

time.sleep(5)
while True:
    update_graph(timedisplay)
    piechart()
    UpdateJson(AppReader.apptime, path)
    time.sleep(0.5)
    