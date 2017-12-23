# Import stuff to backend
from urllib.request import urlopen
import json

# Here goes all the backend functions
def printTest():
    print("Test successful")

username = "cesuna"
currentregion="na1"

fn = 'apikey.txt'
apkfile = open(fn)
rawapk = apkfile.read().replace('\n','')
apkfile.close()
apkey = rawapk


# # Dealing with getting json from urlResponses
def getJsonFromUrl(url):
    # Get data and decode the bitString object into plain string
    json_data = urlopen(url).read().decode('utf8')
    print(json_data)
    # Now convert the string into jsonObject
    data = json.loads(json_data)
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
 FUNCT <- (selectedRegion, summonerName); example ["na1", "cesuna"]
 WAIT
 FUNC -> dict {id: summonerId, accountId: accountId, etc};
 exampleOut
 {'accountId': 32626469, 'summonerLevel': 55, 'name': 'cesuna',
 'profileIconId': 3159, 'revisionDate': 1513993431000, 'id': 19877155}
'''

# # _SpectatorV3_
# Siin saame infot käimasoleva mängu kohta (overall) [kui mängu pole, siis tuleb 404 error!]
def spec(r, id):
    url = "https://<REGION>.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/<ID>?api_key="+api_key
    url = url.replace('<REGION>', r).replace('<ID>', id)
    json_data = urlopen(url)
    andmed = json.load(json_data)
    return andmed


print(getUserData(currentregion, username, apkey))
