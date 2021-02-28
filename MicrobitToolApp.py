"""
License: https://opensource.org/licenses/Apache-2.0
Author: Adak Celina, https://www.github.com/bosdos12
"""

from tkinter import *
from tkinter import messagebox
from webbrowser import open_new as wbOpen
import time
from os import system
from pathlib import Path


class App:
    def __init__(self):
        self.mainWindow = Tk()
        # configuring some window properties
        self.mainWindow.geometry("650x460")
        self.mainWindow.resizable(False, False)
        self.mainWindow.title("Microbit Tool App")
        
        # header frame
        Frame(height=70,width=700,bg="gray").place(x=0,y=0)

        # clock
        Label(text="_________________________", fg="white", bg="gray").place(x=532, y=13)
        self.clockLabel = Label(text="", font=150, bg="gray", fg="white")
        self.clockLabel.place(x=558, y=5)
        self.updateClock()

        # setting some header text
        Label(text="MicrobitToolApp", fg="white", bg="gray", font=("Courier", 30)).place(x=40, y=10)

        # asking for the user to enter the path of the python file they want to run
        Label(text="Enter The path of your python file", font=("Arial", 18)).place(x=16, y=100)
        self.PathEntry = Entry(width=30, bg="lightgray", font=("Arial", 16))
        self.PathEntry.place(x=16, y=130)
        Button(text="Run", bg="gray", fg="white", padx=20, font=("Arial", 14), command=self.runScript).place(x=16, y=161)

        # recent files side frame
        Frame(height=360,width=215,bg="gray",borderwidth = 1, highlightthickness="1", highlightbackground="black").place(x=435,y=70)
        Label(text="____________________", font=("Arial", 13), bg="gray").place(x=453, y=80)
        Label(text="Recently ran scripts", font=("Arial", 13), bg="gray").place(x=468, y=75)
        # file is loading shower
        self.fileIsBeingFlashedLoader = Label(text="", font=("Arial", 16))
        self.fileIsBeingFlashedLoader.place(x=16, y=205)

        # logs textbox
        Label(text="Logs:", font=("Arial", 14)).place(x=16, y=235)
        self.logsBox = Text(width=44, height=10, bg="black", fg="lime", font=("Arial", 12))
        self.logsBox.place(x=16, y=260)
        
        # run recent files bar
        self.reRenderRecents()

        # license
        Frame(height=30,width=700,bg="gray").place(x=0,y=430)
        Button(text="Click for license info", bg="lightgray", padx=6, pady=2, command=self.viewLicense, font=("Arial", 9)).place(x=518, y=431)
        # looping the main window
        self.mainWindow.mainloop()

    # running the script
    def runScript(self):
        runVar = self.PathEntry.get()
        self.PathEntry.delete(0, "end")
        
        # checking if the path directs to a valid python file or even exists
        if self.checkFileExtension(runVar):
            if system("uflash " + runVar) == 0:
                recentFilesF = open("./MBTA_appData/recentFiles.txt", 'r+')
                rfLines = recentFilesF.readlines()
                recentFilesF.close()
                recentFWO = open("./MBTA_appData/recentFiles.txt", "w")
                if len(rfLines) < 5:
                    rfLines.insert(0, f"{runVar}\n")
                    recentFWO.writelines(rfLines)
                else:
                    rfLines.insert(0, f"{runVar}\n")
                    rfLines.pop()
                    recentFilesF.close()
                    recentFWO.writelines(rfLines)
                recentFWO.close()
                # rerendering the screen
                self.fileIsBeingFlashedLoader.config(text="File flashed succesfully!", bg="lime", fg="black")
                self.logsBox.insert('1.0', str(time.strftime("%H:%M:%S")) + " > [Info: File flashed succesfully]\n\n")
                self.reRenderRecents()
            else:
                self.logsBox.insert('1.0', str(time.strftime("%H:%M:%S")) + " > [Error: The file or your microbit not found]\n\n")
                messagebox.showerror("Error", "The file or your microbit not found")
        else:
            self.logsBox.insert('1.0', str(time.strftime("%H:%M:%S")) + " > [Invalid Input: Please enter the path of a valid python file]\n\n")
            messagebox.showerror("Invalid Input", "Please enter the path of a valid python file")

    def reRenderRecents(self):
        recentFilesF = open("./MBTA_appData/recentFiles.txt", 'r')
        rfLines = recentFilesF.readlines()
        recentFilesF.close()
        buttonLoc = 70

        for i in range(len(rfLines)):
            buttonLoc += 40
            # create a new button with the data returned from self.getTitle(rfLines[i])
            print(rfLines[i])
            btitle = self.getTitle(rfLines[i])
            Button(text=btitle + ".py", font=("Arial", 10), width=20, height=1, command=lambda i=i:self.startWithButton(rfLines[i])).place(x=460, y=buttonLoc)
        
    # the function for returning the name of the file from the full path.
    def getTitle(self, pathP):
        return Path(pathP).stem

    # the function for starting the recent opened files
    def startWithButton(self, startPath):
        if system(f"uflash {startPath}") == 0:
            self.fileIsBeingFlashedLoader.config(text="File flashed succesfully!", bg="lime", fg="black")
            self.logsBox.insert('1.0', str(time.strftime("%H:%M:%S")) + " > [Info: File flashed succesfully!]\n\n")
        else:
            self.fileIsBeingFlashedLoader.config(text="There was an error flashing the file", bg="red", fg="white")
            self.logsBox.insert('1.0', str(time.strftime("%H:%M:%S")) + " > [Error: there was an error flashing the file]\n\n")

    # the function for keeping the clock updated.
    def updateClock(self):
        curTime = time.strftime("%H:%M:%S")
        self.clockLabel.config(text=curTime)
        self.mainWindow.after(1000, self.updateClock)

    # checking if the path extension is a valid .py file.
    def checkFileExtension(self, fileExt):
        tl = len(fileExt)
        if tl > 0:
            if fileExt.endswith(".py"):
                return True
            else:
                return False
        else:
            return False


    # viewing the license
    def viewLicense(self):
        wbOpen("https://opensource.org/licenses/Apache-2.0")



run=App()