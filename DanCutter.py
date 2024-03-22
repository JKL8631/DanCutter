import os
import tkinter as tk
from tkinter import filedialog
import customtkinter as cTk
from tkinter.messagebox import showinfo
import re

class App(cTk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.title("DanCutter")
        self.geometry("700x200")
        self.title("DanCutter")
        self.resizable(False,False)
        self.grid_columnconfigure(0,weight=1)

        basedir = os.path.dirname(__file__)
        self.iconbitmap(os.path.join(basedir, "danCutterLogo.ico"))

        self.pathFrame = pathFrame(self)
        self.breakFrame = breakFrame(self)
        self.resultFrame = resultFrame(self)
        
        self.pathFrame.grid_columnconfigure(0,weight=1)
        self.pathFrame.grid(row=0,column=0,sticky="NWE",columnspan=5)
        self.pathFrame.configure(fg_color="transparent")
        
        self.breakFrame.grid_columnconfigure(0,weight=1)
        self.breakFrame.grid(row=1,column=0,padx=20,sticky="NWE")
        self.breakFrame.configure(fg_color="transparent")
        
        self.resultFrame.grid_columnconfigure(0,weight=1)
        self.resultFrame.grid(row=2,column=0,padx=(20,150),pady=20,sticky="ew")
        
        
        
class pathFrame(cTk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.pathOfMapEntry = cTk.CTkEntry(self, placeholder_text="Path to the map")
        browseFileButton = cTk.CTkButton(self, text="Browse Files ...", command=self.selectFile)
        
        self.pathOfMapEntry.grid(row=0, column=0, padx=20, pady=20, sticky="ew",columnspan=4)
        browseFileButton.grid(row=0, column=4,padx=20, pady=20, sticky="ew")
           
        
    def selectFile(self):
        filetypes = (
            ('Osu! Maps','*.osu'),
            ('All types(*.*)', '*.*')
        )
        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='C:\\Users\\labbe\\AppData\\Local\\osu!\\Songs\\1116467 Various Artists - 4K LN Dan Courses v2 - FINAL -\\', # Change to '\'
            filetypes=filetypes,
        )
        
        self.setPathName(filename)
    
    def setPathName(self,text):
        self.pathOfMapEntry.delete(0,tk.END)
        self.pathOfMapEntry.insert(0,text)
        return
       
class breakFrame(cTk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        
        self.mapData = None
        
        frame = cTk.CTkFrame(self)
        frame.grid(row=0,column=0,padx=(0,40),sticky="we")
        
        infoBreakLabel = cTk.CTkLabel(frame, text="Length of a break in milliseconds : ", fg_color="transparent")
        self.breakLengthEntry = cTk.CTkEntry(frame, placeholder_text="Ex : 3000")
        findBreakButton = cTk.CTkButton(self, text="Find Maps", command=lambda:self.checkInput(parent.pathFrame.pathOfMapEntry.get(),self.breakLengthEntry.get(),parent))
        
        infoBreakLabel.grid(row=0,column=0,padx=20, sticky="w")
        self.breakLengthEntry.grid(row=0,column=1,padx=(90,0),pady=5, sticky="w")
        findBreakButton.grid(row=0,column=2,pady=5,sticky="e")
        
    def checkInput(self,path,breakLength,parent):
        if path == "" and breakLength == "":
            showinfo(
                title='Error !',
                message="You must specify the map path and the break length !"
            )
            return
        elif breakLength == "" and path != "":
            showinfo(
                title='Error !',
                message="You must specify the break length !"
            )
            return
        elif breakLength != "" and path == "":
            showinfo(
                title='Error !',
                message="You must specify the map path !"
            )
            return
        else :
            try:
                breakLength = int(breakLength)
            except ValueError:
                showinfo(
                    title='Error !',
                    message="The break length must be a number !"
                )
                return
            if not os.path.isfile(path):
                showinfo(
                    title='Error !',
                    message="This is not a valid path !"
                )
                return
            
            self.mapData = mapInfos(path,breakLength)
            
            if breakLength <= 0 or breakLength >= self.mapData.totalMapLength:
                showinfo(
                    title='Error !',
                    message="The break length is not valid !"
                )
                return

            parent.resultFrame.numberOfMapsLabel.configure(text=f"{len(self.mapData.breakLines)+1} maps have been found !")
            parent.resultFrame.splitMapsButton.configure(state="normal")
            parent.resultFrame.cancelOperationButton.configure(state="normal")
            self.breakLengthEntry.configure(state="disabled")
            parent.pathFrame.pathOfMapEntry.configure(state="disabled")
    


class resultFrame(cTk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        
        self.numberOfMapsLabel = cTk.CTkLabel(self,text="You Must Find Maps First !")
        self.splitMapsButton = cTk.CTkButton(self,text="Split Maps !",command=lambda:self.splitMaps(parent.breakFrame.mapData,parent.pathFrame.pathOfMapEntry.get()),state="disabled")
        self.cancelOperationButton = cTk.CTkButton(self,text="Cancel Splitting",command=lambda:self.cancelOperation(parent.pathFrame.pathOfMapEntry,parent.breakFrame.breakLengthEntry),state="disabled")
        
        self.numberOfMapsLabel.grid(row=0,column=0,pady=10,padx=20,sticky="w")
        self.splitMapsButton.grid(row=0,column=1,padx=10,sticky="e")
        self.cancelOperationButton.grid(row=0,column=2,padx=10,sticky="e")
        
    def cancelOperation(self,input1,input2):
        input1.configure(state="normal")
        input2.configure(state="normal")
        input2.delete(0,tk.END)
        self.splitMapsButton.configure(state="disabled")
        self.cancelOperationButton.configure(state="disabled")
        self.numberOfMapsLabel.configure(text="You Must Find Maps First !")
        
    def splitMaps(self,mapData,path):
        mapName,directory = self.processFilePath(path)
        
        self.createFile(int(mapData.startingNoteLine),mapData.breakLines[0],0,mapData.breakTimingPoints[0],directory,mapName,path,1)
        for i in range(1,len(mapData.breakLines)):
            self.createFile(mapData.breakLines[i-1],mapData.breakLines[i],mapData.breakTimingPoints[i-1],mapData.breakTimingPoints[i],directory,mapName,path,i+1)
        self.createFile(mapData.breakLines[-1],self.countLinesInFile(path),mapData.breakTimingPoints[-1],self.getLastLineOfFileTime(path),directory,mapName,path,len(mapData.breakLines)+1)
        
        showinfo(
            title='Done !',
            message="Don't forget to hit F5 to see the new maps !"
        )
        
    def getLastLineOfFileTime(self,file):
        with open(f'{file}', 'rb') as f:
            try:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            last_line = f.readline().decode().split(',')
            return int(last_line[2])
    
    def countLinesInFile(self,file):
        with open(f"{file}", 'r') as fp:
            for count, line in enumerate(fp):
                pass
        return (count+1)
    
    def processFilePath(self,file):
        dir = ""
        path = file.split("\\")
        for i in range(0,len(path)-1):
            dir = dir + path[i] + "\\"
        return path[-1][0:-4],dir
    
    def createFile(self,startingLine,endingLine,startingTPoint,endingTPoint,directory,mapName,ogFile,mapNumber):
        with open(f"{directory}{self.buildMapName(mapName,mapNumber)}].osu", "w") as file:
            dataLine = self.extractData(ogFile,0,'PreviewTime:')
            file.write(dataLine[0])
            file.write(f"PreviewTime: {round((int(startingTPoint)+int(endingTPoint))/2)}\n")
            dataLine = self.extractData(ogFile,dataLine[1]+1,'Version:')
            file.write(dataLine[0])
            file.write(f"Version: {self.extractDiffName(mapName)} - Map {mapNumber}\n")
            dataLine = self.extractData(ogFile,dataLine[1]+1,'BeatmapSetID:')
            file.write(dataLine[0])
            file.write("BeatmapSetID: -1\n")
            dataLine = self.extractData(ogFile,dataLine[1]+1,'[TimingPoints]')
            file.write(dataLine[0])
            dataLine = self.extractData(ogFile,dataLine[1]+1,'[HitObjects]')
            file.write('[TimingPoints]\n')
            file.write(self.processTimingPoints(dataLine[0],startingTPoint,endingTPoint))
            file.write('\n[HitObjects]\n')
            file.write(self.extractNoteData(ogFile,startingLine,endingLine))
    
    def buildMapName(self,oldMapName,mapNumber):
        return f"{self.extractMapTitle(oldMapName)} [{self.extractDiffName(oldMapName)} - Map {mapNumber}"
    
    def extractData(self,f,start,stopPoint):
        result = ""
        endLine = 0
        with open(f,"r") as file:
            for l_no,i in enumerate(file):
                if l_no >= start-1:
                    if stopPoint in i:
                        endLine = l_no+1
                        break
                    result = result + i
        return result,endLine
    
    def extractNoteData(self,f,start,end):
        result = ""
        with open(f,"r") as file:
            for l_no,i in enumerate(file):
                if l_no >= start:
                    if l_no > end-1:
                        break
                    result = result + i
        return result
    
    def extractDiffName(self,input_text):
        pattern = re.search(r"^.*-.*\s\(.*\)\s\[(.*)\]", input_text)
        return pattern.groups()[0]
    
    def extractMapTitle(self,input_text):
        pattern = re.search(r"^(.*)\s\[.*\]$",input_text)
        return pattern.groups()[0]
    
    def processTimingPoints(self,tPoints,start,end):
        tPointsTab = tPoints.split()
        tPointsTabFiltered = []
        for i in range(0,len(tPointsTab)):
            lineValue = tPointsTab[i].split(',')
            if int(lineValue[0]) >= start and int(lineValue[0]) <= end:
                tPointsTabFiltered.append(tPointsTab[i])
        mapBeatLength = float(tPointsTabFiltered[0].split(',')[1])
        for i in range(0,len(tPointsTabFiltered)-1):
            tPoint1 = tPointsTabFiltered[i].split(',')
            tPoint2 = tPointsTabFiltered[i+1].split(',')
            if int(tPoint1[6]) == 1 and int(tPoint2[6]) == 0:
                tPoint2[1] = self.sliderVelocityMultiplierConvertor(float(tPoint1[1])/mapBeatLength)
                tPointsTabFiltered[i+1] = self.listToString(tPoint2)
        tPointsString = ""
        for i in range(0,len(tPointsTabFiltered)):
            tPointsString = tPointsString + tPointsTabFiltered[i] + "\n"
        return tPointsString
    
    def listToString(self,list):
        res = ""
        for i in list:
            res = res + str(i) + ','
        return res[0:-1]
    
    def sliderVelocityMultiplierConvertor(self,number):
        return 1/-number*100

class mapInfos():
    
    def __init__(self,path,breakLength):
        self.breakLength = breakLength
        mapData = self.getBreaks(path)
        self.breakLines = mapData[0]
        self.breakTimingPoints = mapData[1]
        self.startingNoteLine = mapData[2]
        self.endingNoteLine = self.getLastLineOfFileTime(path)
        self.totalMapLength = self.countLinesInFile(path)
        
    def getBreaks(self,file):
        with open(file, "r") as f:
            no = 0
            for l_no, line in enumerate(f):
                if '[HitObjects]' in line:
                    no = l_no + 1
                    break
            result = []
            temp = self.breakFinder(f,no)
            result.append(temp[0])
            result.append(temp[1])
            result.append(no)
            return result
    
    def breakFinder(self,f,start):
        breaksLines = []
        breaksTPoints = []
        for l_no,line in enumerate(f,start):
            previous = self.extractTime(line)
            break
        for l_no, line in enumerate(f,start=start+1):
            next = self.extractTime(line)
            if self.gapAnalyser(previous,next):
                breaksLines.append(l_no)
                breaksTPoints.append(previous)
            previous = next
        return breaksLines,breaksTPoints
    
    def gapAnalyser(self,note1,note2):
        return note2-note1 >= self.breakLength

    def extractTime(self,line):
        noteData = line.split(',')
        return int(noteData[2])
    
    def countLinesInFile(self,file):
        with open(f"{file}", 'r') as fp:
            for count, line in enumerate(fp):
                pass
        return (count+1)
    
    def getLastLineOfFileTime(self,file):
        with open(f'{file}', 'rb') as f:
            try:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            last_line = f.readline().decode().split(',')
            return int(last_line[2])
        
    def toString(self):
        return 'Break Length = '+str(self.breakLength)+'\nBreak Lines = '+str(self.breakLines)+'\nBreak Timing Points = '+str(self.breakTimingPoints)+'\nStarting Note Line = '+str(self.startingNoteLine)+'\nEnding Note Line = '+str(self.endingNoteLine)+'\nTotal Map Length = '+str(self.totalMapLength)
    
    
if __name__ == "__main__":
    app = App()
    app.mainloop()