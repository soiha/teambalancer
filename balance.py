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
  
#Grab the list of players
players = {}
readPlayers('players.txt')

#Create the two teams
redTeam = {}
redTeamSR = 0
blueTeam = {}
blueTeamSR = 0

#Greedy algorithm. Sort by SR and pop off
for x in sorted(players, key=players.get):
    if redTeamSR < blueTeamSR:
        redTeam[x] = players[x]
        redTeamSR += int(redTeam[x])
    else:
        blueTeam[x] = players[x]
        blueTeamSR += int(blueTeam[x])

#Print the teams
print ("Red Team Average SR: " + str((redTeamSR)/len(redTeam)))
for i in redTeam:
    print (i, redTeam[i])
print ("------------")
print ("Blue Team Average SR: " + str((blueTeamSR)/len(blueTeam)))
for i in blueTeam:
    print (i, blueTeam[i])
