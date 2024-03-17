import re
import os

def open_in_notepad(file_path):
    os.system('start notepad.exe ' + file_path)

def extractDiffName(input_text):
    pattern = re.search(r"^.*-.*\s\(.*\)\s\[(.*)\]", input_text)
    return pattern.groups()

def breakFinder(f,start):
    breaks = []
    for l_no,line in enumerate(f,start):
        previous = extractTime(line)
        break
    for l_no, line in enumerate(f,start=start+1):
        next = extractTime(line)
        if gapAnalyser(previous,next):
            breaks.append(l_no)
        previous = next
    return breaks

def extractTime(line):
    noteData = line.split(',')
    return int(noteData[2])

def gapAnalyser(note1,note2):
    return note2-note1 >= 3000

def createFile(start,end,directory,diffName,ogFile):
    with open(f"{directory}{diffName}.osu", "w") as file:
        dataLine = extractGeneralEditorData(ogFile)
        file.write(dataLine[0])
        file.write(f"Version:{diffName}\n")
        dataLine = extractSourceTagsBeatmapID(ogFile,dataLine[1]+1)
        file.write(dataLine[0])
        file.write("BeatmapSetID:-1\n")
        file.write("quoi")
        open_in_notepad(f"{directory}{diffName}.osu")
    
def extractSourceTagsBeatmapID(f,start):
    result = ""
    endLine = 0
    with open(f,"r") as file:
        for l_no,i in enumerate(file):
            if l_no >= start-1:
                if 'BeatmapSetID:' in i:
                    endLine = l_no+1
                    break
                result = result + i
    return result,endLine
    
def extractGeneralEditorData(f):
    result = ""
    endLine = 0
    with open(f,"r") as file:
        for l_no,i in enumerate(file):
            if 'Version:' in i:
                endLine = l_no+1
                break
            result = result + i
    return result,endLine
     
file = "C:\\Users\\labbe\\AppData\\Local\\osu!\\Songs\\1116467 Various Artists - 4K LN Dan Courses v2 - FINAL -\\Various Artists - 4K LN Dan Courses v2 - FINAL - (_underjoy) [15th Dan - Yume (Marathon)].osu"
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
createFile(no,breaks[0],dir,extractDiffName(diffName)[0] + " - 1st Map",file)
f.close()