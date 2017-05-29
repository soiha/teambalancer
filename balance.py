import urllib2
import re

class Scraper:
	def scrape(self, player):
		urlend = player.name.replace("#", "-")
		url_base = "https://playoverwatch.com/en-us/career/pc"
		urls = (url_base+"/na/"+urlend, url_base+"/eu/"+urlend)
		
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
			player.rating = parsed_rating
		else:
			print ("Rating not found for %s, using %d" % (player.name, player.rating))

	def __init__(self):
		pass

class Player:
	def __init__(self, name, rating):
		self.name = name
		self.rating = int(rating)
		self.primaryCharacter = ""

def readPlayers(fileName):
	f = open(fileName, 'r')
	for line in f:
		tokens = line.split(':')
		if len(tokens) == 2: 
			addPlayer(tokens[0], tokens[1][:-1])
		else:
			addPlayer(tokens[0][:-1], 2500)
	f.close()
	return

def addPlayer(playerName, SR ):
    players[playerName] = Player(playerName, SR)
    return

def getWeight(SR):
    weight = 0.2
    if SR > 1000:
        weight = 0.4
    if SR > 1500:
        weight = 0.6
    if SR > 2000:
        weight = 0.8
    if SR > 2500:
        weight = 1
    if SR > 3000:
        weight = 1.2
    if SR > 3500:
        weight = 1.4
    if SR > 4000:
        weight = 1.6
    return weight
 


if __name__ == "__main__":
	#Grab the list of players
	players = {}
	readPlayers('players.txt')
	
	# Try scraping SRs
	scraper = Scraper()
	[scraper.scrape(p) for p in players.values()]

	#Create the two teams
	redTeam = {}
	redTeamAverageSR = 0
	redTeamWeightedSR = 0
	blueTeam = {}
	blueTeamAverageSR = 0
	blueTeamWeightedSR = 0

	#Greedy algorithm. Sort by weighted SR and pop off
	for x in sorted(players, key=players.get):
		SR = int(players[x].rating)
		WSR = float(players[x].rating) * getWeight(players[x].rating)
		if redTeamWeightedSR < blueTeamWeightedSR:
			redTeam[x] = players[x]
			redTeamWeightedSR += WSR
			redTeamAverageSR += SR
		else:
			blueTeam[x] = players[x]
			blueTeamWeightedSR += WSR
			blueTeamAverageSR += SR

	#Print the teams
	print ("Red Team Average SR: " + str((redTeamAverageSR)/len(redTeam)))
	for i in redTeam:
		print (i, redTeam[i].rating)
	print ("------------")
	print ("Blue Team Average SR: " + str((blueTeamAverageSR)/len(blueTeam)))
	for i in blueTeam:
		print (i, blueTeam[i].rating)
