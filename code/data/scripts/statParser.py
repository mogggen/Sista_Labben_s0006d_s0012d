statDict = {}

def loadStats():
    f = open("maps/stats.txt", "r")
    # parse map file
    statLines = f.readlines()
    global statDict
    for line in statLines:
        if line[0] not in ("\n", "#"):
            entry = line.split(":")
            statDict[str(entry[0])] = float(entry[1])
    f.close()

def getStat(stat):
    return statDict[stat]