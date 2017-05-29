import math
import re
import urllib.request
import urllib.error


class Scraper:
    def __init__(self):
        self.regex_search = "\<div class=\"competitive-rank\"\>\<img src=\".+\"/\>\<div class=\"u-align-center h6\"\>([0-9]+)\</div\>"
        self.url_base = "https://playoverwatch.com/en-us/career/pc"
        self.regions = ("/us/", "/eu/")

    def scrape(self, player):
        player_id = player.id.replace("#", "-")
        parsed_rating = float('nan')

        for region in self.regions:
            try:
                req = urllib.request.urlopen(self.url_base + region + player_id)
                if req.getcode() != 404:
                    result = req.read()
                    resultStr = result.decode('utf-8')
                    match = re.search(self.regex_search, resultStr)
                    sr_maybe = match.group(1)
                    try:
                        parsed_rating = int(sr_maybe)
                    except Exception:
                        print("-->Could not parse SR for %s, using %s" % (player.name, player.sr))
                break
            except urllib.error.HTTPError:
                continue

        if math.isnan(parsed_rating):
            print("-->Rating not found for %s, using %d" % (player.name, player.sr))
        else:
            print("-->Got SR for %s: %d" % (player.name, parsed_rating))
            player.setSR(parsed_rating)

        # Generating overbuff profile link and grabbing data
        profile_link = "https://www.overbuff.com/players/pc/" + player_id
        response = urllib.request.urlopen(profile_link + "?mode=competitive")
        page_source = response.read()

        # Grab number of lines
        nlines = len(page_source.splitlines())
        # If competitive data is not found, collect quick play data
        if (nlines < 4):
            response = urllib.request.urlopen(profile_link)
            page_source = response.read()
            # Grab number of lines
            nlines = len(page_source.splitlines())

        # Main hero classes are on the last line
        mains = page_source.splitlines()[nlines - 1]
        # Parse and print sorted hero classes
        parsed_role = 'Flex'
        support = re.findall(r'Support</a><small><span data-time="(.*?)" data-time-format', mains)
        tank = re.findall(r'Tank</a><small><span data-time="(.*?)" data-time-format', mains)
        defense = re.findall(r'Defense</a><small><span data-time="(.*?)" data-time-format', mains)
        offense = re.findall(r'Offense</a><small><span data-time="(.*?)" data-time-format', mains)

        # Collect hero roles based on amount of time played
        heroMains = {}
        try:
            heroMains["Support"] = int(support[0])
            heroMains["Tank"] = int(tank[0])
            heroMains["Defense"] = int(defense[0])
            heroMains["Offense"] = int(offense[0])
            parsed_role = sorted(heroMains.items(), key=lambda k_v: k_v[1], reverse=True)[0][0]
            parsed_backup_role = sorted(heroMains.items(), key=lambda k_v: k_v[1], reverse=True)[1][0]
            print("-->Got role for %s: %s/%s" % (player.name, parsed_role, parsed_backup_role))
            player.setRole(parsed_role + '/' + parsed_backup_role)
        except IndexError:
            print("-->Could not parse role for %s, using %s" % (player.name, player.role))
