import scraper
import player


def readPlayers(fileName):
    filePlayers = []
    f = open(fileName, 'r')
    scraper = scraper.Scraper()
    for line in f:
        playerID = line[:-1]
        print playerID
        player = player.Player(playerID)
        filePlayers.append(player)
        scraper.scrape(player)
    f.close()
    return filePlayers


#Takes in a list of players and partitions them into two 
#teams using least difference heuristic
def partition(playerList):
    redTeam = []
    redTeamAverageSR = 0
    redTeamWeightedSR = 0
    blueTeam = []
    blueTeamAverageSR = 0
    blueTeamWeightedSR = 0
    for p in playerList:
        print ("  Sorting " + p.getName())
        if redTeamWeightedSR < blueTeamWeightedSR:
            redTeam.append(p)
            redTeamWeightedSR += p.getWeightedSR()
            redTeamAverageSR += p.getSR()
            print ("    Sorted " + p.getName() + " to red team")
        else:
            blueTeam.append(p)
            blueTeamWeightedSR += p.getWeightedSR()
            blueTeamAverageSR += p.getSR()
            print ("    Sorted " + p.getName() + " to blue team")
    return redTeam, blueTeam
    
# Gonna make it look real nice
def printTeam(team):
    for p in team:
        string = '{:14}'.format(p.getName()) + '{:4}'.format(p.getSR()) + '{:>18}'.format(p.getRole())
        print ('| ' + string + ' |')
     

if __name__ == "__main__":
    # Initialize the players
    players = readPlayers('players.txt')
    players.sort(key=lambda x: x.getSR(), reverse=True)

    # Greedy algorithm. Sort by weighted SR and pop off
    print ("Begin Sorting")
    redTeam, blueTeam = partition(players)
    print("Sorting complete")
    print("----------------------------------------")

    # Print the teams
    printTeam(redTeam)
    print("----------------------------------------")
    printTeam(blueTeam)
