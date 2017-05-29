import scraper
import player


def readPlayers(fileName):
    file_players = []
    f = open(fileName, 'r')
    s = scraper.Scraper()
    for line in f:
        playerID = line[:-1]
        print(playerID)
        p = player.Player(playerID)
        s.scrape(p)
        file_players.append(p)
    f.close()
    return file_players


#Takes in a list of players and partitions them into two 
#teams using least difference heuristic
def partition(player_list):
    red_team = []
    red_team_average_sr = 0
    red_team_weighted_sr = 0
    blue_team = []
    blue_team_average_sr = 0
    blue_team_weighted_sr = 0
    for p in player_list:
        print("  Sorting " + p.getName())
        if red_team_weighted_sr < blue_team_weighted_sr:
            red_team.append(p)
            red_team_weighted_sr += p.getWeightedSR()
            red_team_average_sr += p.getSR()
            print("    Sorted " + p.getName() + " to red team")
        else:
            blue_team.append(p)
            blue_team_weighted_sr += p.getWeightedSR()
            blue_team_average_sr += p.getSR()
            print("    Sorted " + p.getName() + " to blue team")
    return red_team, blue_team


# Gonna make it look real nice
def printTeam(team):
    for p in team:
        string = '{:14}'.format(p.getName()) + '{:4}'.format(p.getSR()) + '{:>18}'.format(p.getRole())
        print('| %s |' % string)


if __name__ == "__main__":
    # Initialize the players
    players = readPlayers('players.txt')
    players.sort(key=lambda x: x.getSR(), reverse=True)

    # Greedy algorithm. Sort by weighted SR and pop off
    print("Begin Sorting")
    red_team, blue_team = partition(players)
    print("Sorting complete")
    print("----------------------------------------")

    # Print the teams
    printTeam(red_team)
    print("----------------------------------------")
    printTeam(blue_team)
