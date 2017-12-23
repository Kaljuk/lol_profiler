# Import stuff to backend
from urllib.request import urlopen
import json

# Here goes all the backend functions
def printTest():
    print("Test successful")

# Test input for testing the functions
username = "cesuna"
currentregion="na1"

# Get API Key from secret txt file
fn = 'apikey.txt'
apkfile = open(fn)
rawapk = apkfile.read().replace('\n','')
apkfile.close()
apkey = rawapk


# # Dealing with getting json from urlResponses
def getJsonFromUrl(url):
    try:
        # Get data and proceed when no error | otherwise
        urlresponse = urlopen(url)
        # Decode the bitString object into plain string
        rawdata = urlresponse.read().decode('utf8')
        # Now convert the string into jsonObject
        data = json.loads(rawdata)
        # Add success variable to the object (was the request successful)
        data["success"] = True
        return data
    except:
        # Request wasn't successful
        data = {"success":False}
        return data

# # _SummonerV3_
# Get user data from inserting summonerName and Region into riotAPI
# getData[r- UIselectedRegion, n- summonerName] _SummonerV3_
def getUserData(r, n, api_key):
    region = "eun1" if (r=="EUNE") else "euw1" if (r=="EUW") else "na1"
    url = "https://<REGION>.api.riotgames.com/lol/summoner/v3/summoners/by-name/<NAME>?api_key="+api_key
    url = url.replace('<REGION>', region).replace('<NAME>', n)
    # Now convert the string into jsonObject
    data = getJsonFromUrl(url)
    return data
'''
 FUNCT <- (selectedRegion, summonerName, apikey); example ["na1", "cesuna"]
 WAIT
 FUNCT -> dict {id: summonerId, accountId: accountId, etc};
 exampleOut
 {'accountId': 32626469, 'summonerLevel': 55, 'name': 'cesuna',
  'profileIconId': 3159, 'revisionDate': 1513993431000, 'id': 19877155}
'''

# # _SpectatorV3_
# Siin saame infot käimasoleva mängu kohta (overall) [kui mängu pole, siis tuleb 404 error!]
def getMatchData(r, summonerid, api_key):
    url = "https://<REGION>.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/<ID>?api_key="+api_key
    url = url.replace('<REGION>', r).replace('<ID>', summonerid)
    andmed = getJsonFromUrl(url)
    return andmed
'''
FUNCT <- (selectedRegion, summonerid (not accountId, just id instead), apikey)
WAIT
FUNCT -> {
    'success': True,
    'gameStartTime': 1513995854039, 'gameId': 2677436825, 'gameQueueConfigId': 420,
    'participants': [{'summonerName': 'Flashcannon0', 'spell1Id': 14, 'teamId': 100, 'gameCustomizationObjects': [], 'championId': 12, 'spell2Id': 4, 'perks': {'perkStyle': 8400, 'perkIds': [8439, 8242, 8429, 8444, 8306, 8321], 'perkSubStyle': 8300}, 'summonerId': 43560759, 'bot': False, 'profileIconId': 624},
    'gameLength': 283, 'platformId': 'NA1', 'gameType': 'MATCHED_GAME', 'bannedChampions': [{'championId': 142, 'teamId': 100, 'pickTurn': 1}, {'championId': 516, 'teamId': 100, 'pickTurn': 2}, {'championId': 238, 'teamId': 100, 'pickTurn': 3}, {'championId': 5, 'teamId': 100, 'pickTurn': 4}, {'championId': 121, 'teamId': 100, 'pickTurn': 5}, {'championId': 53, 'teamId': 200, 'pickTurn': 6}, {'championId': -1, 'teamId': 200, 'pickTurn': 7}, {'championId': 268, 'teamId': 200, 'pickTurn': 8}, {'championId': 121, 'teamId': 200, 'pickTurn': 9}, {'championId': 59, 'teamId': 200, 'pickTurn': 10}], 'gameMode': 'CLASSIC', 'mapId': 11, 'observers': {'encryptionKey': 'AqyEqq887qUDTNdpH8cahw+x8UgBw2YT'}
    }
    a.k.a.
    {
    # my output (was the request successful) # True or false  ,
    # gameStartTime (timeWhenGameStarted in utc), # gameId, # gameQueueConfigId,
    # participants: ( all match participants ) [{summonerName: 123, etc}]
    }
    returns all players in match with their data
'''

userdata = getUserData(currentregion, username, apkey)
print(userdata)
print("spec", getMatchData(currentregion, str(userdata["id"]), apkey))
