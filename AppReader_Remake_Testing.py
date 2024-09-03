import pyautogui
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
import threading
import json
import traceback
from datetime import datetime

truepath = os.path.dirname(os.path.abspath(__file__))
path = truepath  + "\\static\\AppReaderData.json"
columngraphpath = truepath + "\\static\\Column.png"
piechartpath = truepath + "\\static\\Pie.png"
timedisplay = "Seconds"
day = (str(datetime.today()).split("-"))[1]
with open (f"{truepath}//day.json", "w") as f:
    json.dump(day, f)

def checkday(day):
    with open (f"{truepath}//day.json", "r") as f:
        day = json.load(f)
        
    daycheck = (str(datetime.today()).split("-"))[1]
    if daycheck != day:
        day = (str(datetime.today()).split('-'))[1]
        with open (f"{truepath}//day.json", "w") as f:
            json.dump(day, f)
        return False
    else:
        return True

class AppReader():
    def __init__(self):
        self.start_time = time.time()
        self.appsrunning = []
        self.apptime = {}
        self.appslist = {}
        self.endingtime = 0
        self.dailytime = {}

    def AppNameEdit(self):
        modified_apps = []
        for x in self.appsrunning:
            titletest = x
            if titletest in ["", " ", "    ", " - "]:
                titletest = "UNKNOWN APP"
            if " - " in titletest:
                thetitletest = titletest.split(" - ")
                titletest = thetitletest[-1]
            if "\\" in titletest:
                thetitletest = titletest.split("\\")
                titletest = thetitletest[-1]
            if " - " not in titletest:
                titletest = titletest
            if "\u2014" in titletest:
                thetitletest = titletest.split("\u2014")
                titletest = thetitletest[-1]
            if titletest[0] == " ":
                titletest = titletest[1:]
            modified_apps.append(titletest)
        self.appsrunning.clear()
        self.appsrunning = modified_apps
    
    def AppRunning(self):
        self.appsrunning.extend([window.title for window in pyautogui.getAllWindows()])
        self.appsrunning = [x for x in self.appsrunning if x.strip() and x != ""]
        seen = set()
        self.appsrunning = [x for x in self.appsrunning if not (x in seen or seen.add(x))]
    
    def UpdateRunningApps(self):
        current_running_apps = [window.title for window in pyautogui.getAllWindows()]
        current_running_apps = [x for x in current_running_apps if x.strip() and x != ""]
        self.appsrunning = [app for app in self.appsrunning if app in current_running_apps]

    def AppTimer(self):
        #Main timers
        current_time = round(time.time())
        for app in self.appsrunning:
            if app in self.apptime:
                if isinstance(self.apptime[app], dict) and 'cur_time' in self.apptime[app]:
                    appchoose = self.apptime[app]
                    elapsed_times = int(round(current_time - appchoose['cur_time']))
                    elapsed_time = round(elapsed_times, 0)
                    self.apptime[app]['elapsed'] += elapsed_time
                    self.apptime[app]['cur_time'] = current_time
                else:
                    print(f"Error: appchoose for {app} is not properly formatted. Current value: {self.apptime[app]}")
            else:
                self.apptime[app] = {'cur_time': current_time, 'elapsed': 0}
        
        #Daily Time
        if checkday(day):
            for app in self.appsrunning:
                if app in self.dailytime:
                    if isinstance(self.dailytime[app], dict) and 'cur_time' in self.apptime[app]:
                        appchoose = self.dailytime[app]
                        elapsed_times = int(round(current_time - appchoose['cur_time']))
                        elapsed_time = round(elapsed_times, 0)
                        self.dailytime[app]['elapsed'] += elapsed_time
                        self.dailytime[app]['cur_time'] = current_time
                    else:
                        print(f"Error: appchoose for {app} is not properly formatted. Current value: {self.apptime[app]}")
                else:
                    self.dailytime[app] = {'cur_time': current_time, 'elapsed': 0}
            with open (f"{truepath}\\static\\DailyTimeData.json", "w") as f:
                json.dump(self.dailytime, f)
        else:
            with open (f"{truepath}\\static\\DailyTimeData.json", "w") as f:
                json.dump({}, f)
                
        
        
    def reset_timer(self):
        with open(f"{truepath}\\SequentialEndingTime.json", "r") as f:
            endingtime = f.read()
            endingtime = json.loads(endingtime)
        
        ending_time = endingtime["end_time"]
        self.endingtime = ending_time

    def start_session(self):
        self.reset_timer(AppReader)
        current_time = round(time.time())
        time_diff = current_time - self.endingtime
        for app in self.apptime:
            if 'elapsed' in self.apptime[app]:
                self.apptime[app]['elapsed'] += time_diff
            else:
                self.apptime[app]['elapsed'] = time_diff
            self.apptime[app]['cur_time'] = current_time

    def AppRelease(self):
        self.apptime = dict(sorted(self.apptime.items(), key=lambda x: x[1]['elapsed'], reverse=True))
        for app_name, time in self.apptime.items():
            self.appslist[app_name] = (f"{time['elapsed']} seconds")
                       
def update_graph(timedisplay):
    fig1, ax1 = plt.subplots(figsize=(7,4))
    try:
        ax1.clear()
        smalllist = AppReader.appslist
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
        cmap = plt.colormaps.get_cmap("twilight")
        colors = [cmap(index*15) for index in color_indices]
        appernames = []
        appernames.extend(app_names)
        for i in range(len(app_names)):
            for i in range(len(app_names)):
                if len(app_names[i]) > 23:
                    theappnames = app_names[i][:20] + "..."
                    appernames[i] = theappnames

        ax1.bar(appernames, times, color=colors, edgecolor="black")
        ax1.set_xlabel('App Name')
        ax1.set_ylabel(f'Time ({timedisplay})')
        ax1.set_title('App Usage Time')
        plt.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray", axis="y")
        plt.xticks(rotation = 45, ha="right")
        plt.subplots_adjust(left=0.2,bottom=0.4, top = 0.9, right = 0.9)
        plt.savefig(columngraphpath)
        plt.close(fig1)
    except Exception as e:
        print("GRAPH ERROR:")
        print(e)
        print(traceback.format_exc())
        time.sleep(2)
        pass

    return timedisplay

def piechart():
    fig2, ax2 = plt.subplots(figsize=(7,4))
    try:
        ax2.clear()
        smalllist = AppReader.appslist
        if len(smalllist) > 10:
            otherlist = dict(list(smalllist.items())[9:])
            otherlist = [int(round(float(time.split(" ")[0]), 0)) for time in otherlist.values()]
            totalsum = 0
            for i in range(len(otherlist)):
                totalsum += otherlist[i]
            smalllist = dict(list(smalllist.items())[:9])
            smalllist["Other"] = f"{totalsum} seconds"
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
        cmap = plt.colormaps.get_cmap("twilight")
        colors = [cmap(index*15) for index in color_indices]
        ax2.pie(times, autopct='%1.1f%%', startangle=0, colors=colors)
        ax2.axis('equal')
        ax2.set_title('App Usage Time')
        ax2.legend(appernames, title="Legend", loc="center left", bbox_to_anchor=(-0.1, 0))
        plt.subplots_adjust(left=0.2,bottom=0.4, top = 0.9, right = 0.9)
        plt.savefig(piechartpath)
        plt.close(fig2)
    except Exception as e:
        print("GRAPH ERROR:")
        print(e)
        print(traceback.format_exc())
        time.sleep(2)
        pass

def scan():
    while True:
        AppReader.AppRunning(AppReader)
        AppReader.UpdateRunningApps(AppReader)
        AppReader.AppNameEdit(AppReader)
        AppReader.AppTimer(AppReader)
        AppReader.AppRelease(AppReader)

def UpdateJson(apptime, path):
    with open(f"{path}", "w") as f:
        json.dump(apptime, f)

AppReader.__init__(AppReader)
try:
    #Fix for shut-down updates to the dailytimedata dictionary
    with open(f"{truepath}//static//DailyTimeData.json", "r") as f:
        dailytimelist = json.load(f)
    timelist = list(dailytimelist.values())
    valuelist = []
    for value in timelist:
        values = value["elapsed"]
        values = int(values)
        valuelist.append(values)
    x=0
    for app in dailytimelist:
        dailytimelist[app].update({"cur_time": (round(time.time())), "elapsed": valuelist[x]})
        x += 1
    AppReader.dailytime = dailytimelist
except:
    pass

AppReader.AppRunning(AppReader)
AppReader.UpdateRunningApps(AppReader)
AppReader.AppNameEdit(AppReader)
AppReader.start_session(AppReader)
AppReader.AppTimer(AppReader)
AppReader.AppRelease(AppReader)


try:
    #Fix for shut-down updates to the appreaderdata dictionary
    with open (f"{path}", "r") as f:
        appnamelist = json.load(f)
    timelist = list(appnamelist.values())
    valuelist = []
    for value in timelist:
        values = value["elapsed"]
        values = int(values)
        valuelist.append(values)
    x=0
    for app in appnamelist:
        appnamelist[app].update({"cur_time": (round(time.time())), "elapsed": valuelist[x]})
        x+=1
        

    

    AppReader.appsrunning = list(appnamelist.keys())
    AppReader.apptime.update(dict(appnamelist))
    AppReader.apptime = appnamelist
        
except Exception as e:
    print(f"Data Error:\n")
    print(f'{e}')
    pass

thread = threading.Thread(target=scan)
thread.start()

time.sleep(5)
while True:
    update_graph(timedisplay)
    piechart()
    UpdateJson(AppReader.apptime, path)
    time.sleep(0.5)
    ending_time = int(round(time.time(), 0))
    with open(f"{truepath}/SequentialEndingTime.json", "w") as f:
        json.dump({"end_time": ending_time}, f)