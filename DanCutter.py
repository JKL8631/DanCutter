import re
import os
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import customtkinter
from tkinter.messagebox import showinfo

# Processing functions
 
def processFilePath(file):
    dir = ""
    path = file.split("\\")
    for i in range(0,len(path)-1):
        dir = dir + path[i] + "\\"
    return path[-1][0:-4],dir

def breakFinder(f,start):
    breaksLines = []
    breaksTPoints = []
    for l_no,line in enumerate(f,start):
        previous = extractTime(line)
        break
    for l_no, line in enumerate(f,start=start+1):
        next = extractTime(line)
        if gapAnalyser(previous,next):
            breaksLines.append(l_no)
            breaksTPoints.append(previous)
        previous = next
    return breaksLines,breaksTPoints

def gapAnalyser(note1,note2):
    return note2-note1 >= 3000

def processTimingPoints(tPoints,start,end):
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
            tPoint2[1] = sliderVelocityMultiplierConvertor(float(tPoint1[1])/mapBeatLength)
            tPointsTabFiltered[i+1] = listToString(tPoint2)
    tPointsString = ""
    for i in range(0,len(tPointsTabFiltered)):
        tPointsString = tPointsString + tPointsTabFiltered[i] + "\n"
    return tPointsString

def listToString(list):
    res = ""
    for i in list:
        res = res + str(i) + ','
    return res[0:-1]

def calculateGlobalBpm(bpm,sliderVelocity):
    return bpmToBeatPerSecond(bpm)*sliderVelocityMultiplierConvertor(sliderVelocity)

def bpmToBeatPerSecond(bpm):
    return 1 / bpm * 1000 * 60

def sliderVelocityMultiplierConvertor(number):
    return 1/-number*100
    
def countLinesInFile(file):
    with open(f"{file}", 'r') as fp:
        for count, line in enumerate(fp):
            pass
    return (count+1)

# Variables extraction functions

def getBreaks(file):
    with open(file, "r") as f:
        no = 0
        for l_no, line in enumerate(f):
            if '[HitObjects]' in line:
                no = l_no + 1
                break
        result = []
        temp = breakFinder(f,no)
        result.append(temp[0])
        result.append(temp[1])
        result.append(no)
        return result

def getLastLineOfFileTime(file):
    with open(f'{file}', 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line = f.readline().decode().split(',')
        return int(last_line[2])

def extractDiffName(input_text):
    pattern = re.search(r"^.*-.*\s\(.*\)\s\[(.*)\]", input_text)
    return pattern.groups()[0]

def extractMapTitle(input_text):
    pattern = re.search(r"^(.*)\s\[.*\]$",input_text)
    return pattern.groups()[0]

def extractTime(line):
    noteData = line.split(',')
    return int(noteData[2])

def getMapBpm(tPointsTab):
    return round(bpmToBeatPerSecond(float(tPointsTab[0].split(',')[1])),3)

def getGlobalBpm(tPointsTab):
    return round(calculateGlobalBpm(float(tPointsTab[0].split(',')[1]),float(tPointsTab[1].split(',')[1])),3)

def extractNoteData(f,start,end):
    result = ""
    with open(f,"r") as file:
        for l_no,i in enumerate(file):
            if l_no >= start:
                if l_no > end-1:
                    break
                result = result + i
    return result

def extractData(f,start,stopPoint):
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

# File manipulation functions

def buildMapName(oldMapName,mapNumber):
    return f"{extractMapTitle(oldMapName)} [{extractDiffName(oldMapName)} - Map {mapNumber}"

def createFile(startingLine,endingLine,startingTPoint,endingTPoint,directory,mapName,ogFile,mapNumber):
    with open(f"{directory}{buildMapName(mapName,mapNumber)}].osu", "w") as file:
        dataLine = extractData(ogFile,0,'PreviewTime:')
        file.write(dataLine[0])
        file.write(f"PreviewTime: {round((int(startingTPoint)+int(endingTPoint))/2)}\n")
        dataLine = extractData(ogFile,dataLine[1]+1,'Version:')
        file.write(dataLine[0])
        file.write(f"Version: {extractDiffName(mapName)} - Map {mapNumber}\n")
        dataLine = extractData(ogFile,dataLine[1]+1,'BeatmapSetID:')
        file.write(dataLine[0])
        file.write("BeatmapSetID: -1\n")
        dataLine = extractData(ogFile,dataLine[1]+1,'[TimingPoints]')
        file.write(dataLine[0])
        dataLine = extractData(ogFile,dataLine[1]+1,'[HitObjects]')
        file.write('[TimingPoints]\n')
        file.write(processTimingPoints(dataLine[0],startingTPoint,endingTPoint))
        file.write('\n[HitObjects]\n')
        file.write(extractNoteData(ogFile,startingLine,endingLine))
        # open_in_notepad(f"{directory}{buildMapName(mapName,mapNumber)}].osu")

# Debug functions

def open_in_notepad(file_path):
    os.system('start notepad.exe ' + file_path)

# GUI functions

def select_file():
    filetypes = (
        ('All types(*.*)', '*.*'),
        ('Osu! Maps','*.osu')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='C:\\Users\\labbe\\AppData\\Local\\osu!\\Songs\\1116467 Various Artists - 4K LN Dan Courses v2 - FINAL -\\',
        filetypes=filetypes
    )
    
    set_text(filename)

def set_text(text):
    pathOfMap.delete(0,END)
    pathOfMap.insert(0,text)
    return
    
def testfunc():
    showinfo(
        title='Test',
        message="to be done"
    )
    

root = customtkinter.CTk()
root.geometry("700x500")
root.title("DanCutter")
root.resizable(False,False)
root.iconbitmap("danCutterLogo.ico")
root.grid_columnconfigure(0,weight=1)
file = ""
breakLineFrame = customtkinter.CTkFrame(root)
breakLineFrame.grid(row=1,column=0,padx=20,sticky="NSW")
pathOfMap = customtkinter.CTkEntry(root, placeholder_text="Path to the map")

infoBreakDisplay = customtkinter.CTkLabel(breakLineFrame, text="Length of a break in milliseconds : ", fg_color="transparent")
breakLengthEntry = customtkinter.CTkEntry(breakLineFrame, placeholder_text="Ex : 3000")
browseFileButton = customtkinter.CTkButton(root, text="Browse Files ...", command=select_file)
findBreakButton = customtkinter.CTkButton(root, text="Find Breaks", command=testfunc)

pathOfMap.grid(row=0, column=0, padx=20, pady=20, sticky="ew",columnspan=4)
browseFileButton.grid(row=0, column=4,padx=20, pady=20, sticky="ew")
infoBreakDisplay.grid(row=0,column=0,padx=20, sticky="w",columnspan=2)
breakLengthEntry.grid(row=0,column=3,padx=20,pady=5, sticky="e")
findBreakButton.grid(row=1,column=4,padx=20,pady=5)

root.mainloop()


# Main program
  
file = "C:\\Users\\labbe\\AppData\\Local\\osu!\\Songs\\1116467 Various Artists - 4K LN Dan Courses v2 - FINAL -\\Various Artists - 4K LN Dan Courses v2 - FINAL - (_underjoy) [15th Dan - Yume (Marathon)].osu"
#file = "C:\\Users\\labbe\\AppData\\Local\\osu!\\Songs\\Various_Artists_-_Bacon_Haniwa_dan\\Various Artists - Bacon Haniwa dan (Bacon Haniwa) [~EXTRA-EPSILON~].osu"
mapName,dir = processFilePath(file)
breaksLines,breaksTPoints,no = getBreaks(file)
# with open(file, "r") as f:
#     createFile(no,breaksLines[0],0,breaksTPoints[0],dir,mapName,file,1)
#     for i in range(1,len(breaksLines)):
#         createFile(breaksLines[i-1],breaksLines[i],breaksTPoints[i-1],breaksTPoints[i],dir,mapName,file,i+1)
#     createFile(breaksLines[-1],countLinesInFile(file),breaksTPoints[-1],getLastLineOfFileTime(file),dir,mapName,file,len(breaksLines)+1)
