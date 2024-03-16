def breakFinder(f,start):
    for l_no,line in enumerate(f,start):
        previous = extractTime(line)
        break
    for l_no, line in enumerate(f,start=start+1):
        next = extractTime(line)
        if gapAnalyser(previous,next):
            test = int(input("test"))
            print("break")
        previous = next

def extractTime(line):
    noteData = line.split(',')
    return int(noteData[2])

def gapAnalyser(note1,note2):
    return note2-note1 >= 3000
    
f = open("C:\\Users\\labbe\\AppData\\Local\\osu!\\Songs\\1116467 Various Artists - 4K LN Dan Courses v2 - FINAL -\\Various Artists - 4K LN Dan Courses v2 - FINAL - (_underjoy) [15th Dan - Yume (Marathon)].osu", "r")
no = 0
for l_no, line in enumerate(f):
    if '[HitObjects]' in line:
        no = l_no + 1
        break
breakFinder(f,no)
f.close()