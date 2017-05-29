import urllib2
import re

class Scraper:
    def scrape(self, player):
        urlend = player.id.replace("#", "-")
        url_base = "https://playoverwatch.com/en-us/career/pc"
        urls = (url_base+"/us/"+urlend, url_base+"/eu/"+urlend)
        
        #<div class="competitive-rank"><img src="https://blzgdapipro-a.akamaihd.net/game/rank-icons/season-2/rank-3.png"/><div class="u-align-center h6">2183</div>
        
        parsed_rating = -1
        
        for url in urls:
            try:
                req = urllib2.urlopen(url)
                if req.getcode() != 404:
                    result = req.read()
                    match = re.search( "\<div class=\"competitive-rank\"\>\<img src=\".+\"/\>\<div class=\"u-align-center h6\"\>([0-9]+)\</div\>", result)
                    sr_maybe = match.group(1)
                    try:
                        parsed_rating = int(sr_maybe)
                    except Exception:
                        print ("Could not parse SR for %s, using" % (player.name, player.rating) )
                break
            except urllib2.HTTPError:
                continue
        if parsed_rating != -1:
            print ("Got SR for %s: %d" % (player.name, parsed_rating))
            player.setSR(parsed_rating)
        else:
            print ("Rating not found for %s, using %d" % (player.name, player.sr))

    def __init__(self):
        pass

class Player:
    #Default role to flex, and sr to 2300
    def __init__(self, id):
        self.id = id
        self.sr = 2300
        self.role = "flex"
        display = id.split('#')
        self.name = display[0]

    def getName(self):
        return self.name

    def setSR(self, sr):
        self.sr = sr

    def getWeightedSR(self):
        return float(self.sr) * getWeight(self.sr)

    def getSR(self):
        return self.sr

    def setRole(self, role):
        self.role = role


def readPlayers(fileName):
    f = open(fileName, 'r')
    for line in f:
        print line[:-1]
        player = Player(line[:-1])
        players.append(player)
    f.close()
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

#Gonna make it look real nice
def printTeam(team):
    for p in team:
        print("| " + p.getName())

if __name__ == "__main__":
    #Grab the list of players
    players = []
    readPlayers('players.txt')

    # Try scraping SRs
    scraper = Scraper()
    for p in players:
        scraper.scrape(p)
    
    #Create the two teams
    redTeam = []
    redTeamAverageSR = 0
    redTeamWeightedSR = 0
    blueTeam = []
    blueTeamAverageSR = 0
    blueTeamWeightedSR = 0

    #Greedy algorithm. Sort by weighted SR and pop off
    players.sort(key=lambda x: x.getSR(), reverse=True)
    print ("Begin Sorting")
    for p in players:
        print ("  Sorting " + p.getName())
        if redTeamWeightedSR < blueTeamWeightedSR:
            redTeam.append(p)
            redTeamWeightedSR += p.getWeightedSR()
            redTeamAverageSR += p.getSR()
            print ("    Sorted "+ p.getName() + " to red team")
            print ("    RedTeam has weighted SR " + str(redTeamWeightedSR))
        else:
            blueTeam.append(p)
            blueTeamWeightedSR += p.getWeightedSR()
            blueTeamAverageSR += p.getSR()
            print ("    Sorted "+ p.getName() + " to blue team")
            print ("    BlueTeam has weighted SR " + str(blueTeamWeightedSR))

    #Print the teams
    print ("Red Team: " + str((redTeamAverageSR)/len(redTeam)))
    printTeam(redTeam)
    print ("------------")
    print ("Blue Team: " + str((blueTeamAverageSR)/len(blueTeam)))
    printTeam(blueTeam)
