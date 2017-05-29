def readPlayers(fileName):
    f = open(fileName, 'r')
    for line in f:
        tokens = line.split(':')
        addPlayer(tokens[0], tokens[1][:-1])
    f.close()
    return

def addPlayer(playerName, SR ):
    players[playerName] = SR
    return

def getWeight(SR):
    weight = 0.2
    if SR > 1000:
        weight = 0.4
    if SR > 1500:
        weight = 0.6
    if SR > 2000:
        weight = 1
    if SR > 3000:
        weight = 1.2
    if SR > 3500:
        weight = 1.4
    if SR > 4000:
        weight = 1.6
    return weight
  
#Grab the list of players
players = {}
readPlayers('players.txt')

#Create the two teams
redTeam = {}
redTeamAverageSR = 0
redTeamWeightedSR = 0
blueTeam = {}
blueTeamAverageSR = 0
blueTeamWeightedSR = 0

#Greedy algorithm. Sort by weighted SR and pop off
for x in sorted(players, key=players.get):
    SR = int(players[x])
    WSR = float(players[x]) * getWeight(players[x])
    if redTeamWeightedSR < blueTeamWeightedSR:
        redTeam[x] = SR
        redTeamWeightedSR += WSR
        redTeamAverageSR += SR
    else:
        blueTeam[x] = SR
        blueTeamWeightedSR += WSR
        blueTeamAverageSR += SR

#Print the teams
print ("Red Team Average SR: " + str((redTeamAverageSR)/len(redTeam)))
for i in redTeam:
    print (i, redTeam[i])
print ("------------")
print ("Blue Team Average SR: " + str((blueTeamAverageSR)/len(blueTeam)))
for i in blueTeam:
    print (i, blueTeam[i])
