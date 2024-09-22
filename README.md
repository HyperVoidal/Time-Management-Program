# Time Management Program
 Time management program including time spent on programs and integrated checklist. In active development.

# Info for Beginners
This program is designed to allow you to better understand your activities and time spent in different tasks on your computer. 
It functions by tracking the apps open on your device and storing them in a sequentially updating graph that can be accessed at any time by visiting the site "http://127.0.0.1:5000/dashboard". 
This is locally hosted and will not be uploaded to any other location other than your computer.
Other features including a checklist function, and different graphs for total time and daily time are available on the site in tandem.

# Getting Started
To get started with this software, first make sure to download, install, and unzip the file into it's own directory. 
Anywhere is fine, but the base C: drive is the most optimal location.

Next, if you haven't installed the python library, it is best to install that first, along with the python library manager "pip".

After installing python, enter the following commands into your command prompt in order to install the necessary libraries for the operation of this program.
- "pip install pyautogui"
- "pip install time"
- "pip install matplotlib"
- "pip install numpy"
- "pip install os"
- "pip install threading"
- "pip install json"
- "pip install traceback"
- "pip install datetime"
- "pip install flask"
- "pip install flask_wtf"
- "pip install wtforms"
- "pip install subprocess"

These commands are essential to the functionality of the program, as they are libraries that must be installed for the program to function.

After the installation of the libraries, open the python file "Learning Flask.py" and run it. 

If at any point, an error message returns, cancel the active terminal window and rerun the program, it needed to boot from a fresh start and should be immediately operational afterwards.

If the program runs successfully, congratulations, your time data is now being recorded safely. You can cancel data recording at any time by closing the terminal window, but it must be running in order to access this data.

When you wish to access the data, visit "http://127.0.0.1:5000/dashboard" to see all available data as recorded by the system. 

The checklist saves automatically, and the daily time data resets at exactly 11:59pm every day, using local time data.

Thank you for your choice to use AppScan, and I wish you well in your self-improvement journey.
