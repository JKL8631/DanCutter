import re
import os
import math

def open_in_notepad(file_path):
    os.system('start notepad.exe ' + file_path)

def extractDiffName(input_text):
    pattern = re.search(r"^.*-.*\s\(.*\)\s\[(.*)\]", input_text)
    return pattern.groups()

def breakFinder(f,start):
    breaksNo = []
    breaksTPoints = []
    for l_no,line in enumerate(f,start):
        previous = extractTime(line)
        break
    for l_no, line in enumerate(f,start=start+1):
        next = extractTime(line)
        if gapAnalyser(previous,next):
            breaksNo.append(l_no)
            breaksTPoints.append(previous)
        previous = next
    return breaksNo,breaksTPoints

def extractTime(line):
    noteData = line.split(',')
    return int(noteData[2])

def gapAnalyser(note1,note2):
    return note2-note1 >= 3000

def createFile(startingLine,endingLine,startingTPoint,endingTPoint,directory,diffName,ogFile):
    with open(f"{directory}{diffName}.osu", "w") as file:
        dataLine = extractData(ogFile,0,'Version:')
        file.write(dataLine[0])
        file.write(f"Version:{diffName}\n")
        dataLine = extractData(ogFile,dataLine[1]+1,'BeatmapSetID:')
        file.write(dataLine[0])
        file.write("BeatmapSetID:-1\n")
        dataLine = extractData(ogFile,dataLine[1]+1,'[TimingPoints]')
        file.write(dataLine[0])
        dataLine = extractData(ogFile,dataLine[1]+1,'[HitObjects]')
        print(processTimingPoints(dataLine[0],startingTPoint,endingTPoint)) # Process Timing Points
        return
        file.write('[HitObjects]\n')
        file.write(extractNoteData(ogFile,startingLine,endingLine))
        open_in_notepad(f"{directory}{diffName}.osu")

def processTimingPoints(tPoints,start,end):
    tPointsTab = tPoints.split()
    tPointsTabFiltered = []
    for i in range(0,len(tPointsTab)):
        lineValue = tPointsTab[i].split(',')
        if int(lineValue[0]) >= start and int(lineValue[0]) <= end:
            tPointsTabFiltered.append(tPointsTab[i])
    print(findGlobalBpm(tPointsTabFiltered))
    # for i in range(0,len(tPointsTabFiltered)-1):
    #     tPoint1 = tPointsTabFiltered[i].split(',')
    #     tPoint2 = tPointsTabFiltered[i+1].split(',')
    #     if int(tPoint1[6]) == 1 and int(tPoint2[6]) == 0:
    #         tPoint3 = tPointsTabFiltered[i+2].split(',')
    #         res = float(tPoint3[1])/float(tPoint1[1])
    #         print(res)
    return
    for i in range(0,len(tPointsTab)-1):
        pass
    return

def findGlobalBpm(tPointsTab):
    for i in range(0,len(tPointsTab)-1):
        print(tPointsTab[i].split(',')[6] == 1 and tPointsTab[i+1].split(',')[6] == 0)
        if int(tPointsTab[i].split(',')[6]) == 1 and int(tPointsTab[i+1].split(',')[6]) == 0:
            return calculateGlobalBpm(float(tPointsTab[i].split(',')[1]),float(tPointsTab[i+1].split(',')[1]))

def calculateGlobalBpm(bpm,sliderVelocity):
    return bpmToBeatPerSecond(bpm)*negativeSliderVelocityMultiplierToMultiplier(sliderVelocity)

def bpmToBeatPerSecond(bpm):
    return 1 / bpm * 1000 * 60

def negativeSliderVelocityMultiplierToMultiplier(number):
    return 1/-number*100

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
     
file = "C:\\Users\\labbe\\AppData\\Local\\osu!\\Songs\\1116467 Various Artists - 4K LN Dan Courses v2 - FINAL -\\Various Artists - 4K LN Dan Courses v2 - FINAL - (_underjoy) [15th Dan - Yume (Marathon)].osu"
file = "C:\\Users\\labbe\\AppData\\Local\\osu!\\Songs\\1919657 Various Artists - Dan ~ PRE-DELTA ~ Courses v2\\Various Artists - Dan ~ PRE-DELTA ~ Courses v2 (Sakisagee) [Pre-Delta v5].osu"
dir = ""
path = file.split("\\")
for i in range(0,len(path)-1):
    dir = dir + path[i] + "\\"
diffName = path[-1][0:-4]
f = open(file, "r")
no = 0
for l_no, line in enumerate(f):
    if '[HitObjects]' in line:
        no = l_no + 1
        break
breaks = breakFinder(f,no)
breaksLines = breaks[0]
breaksTPoints = breaks[1]
createFile(no,breaksLines[0],0,breaksTPoints[0],dir,extractDiffName(diffName)[0] + " - 1st Map",file)
f.close()