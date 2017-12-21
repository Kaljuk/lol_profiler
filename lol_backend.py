# Import stuff to backend
from urllib.request import urlopen
import json

# Here goes all the backend functions
def printTest():
    print("Test successful")

# Get user data from riot api
# getData[r- UIselectedRegion, n- summonerName]
def getData(r, n, api_key):
    region = "eun1" if (r=="EUNE") else "euw1" if (r=="EUW") else "na1"
    url = "https://<REGION>.api.riotgames.com/lol/summoner/v3/summoners/by-name/<NAME>?api_key="+api_key
    url = url.replace('<REGION>', region).replace('<NAME>', n)
    json_data = urlopen(url)
    data = json.load(json_data)
    return data
# FUNCT <- (selectedRegion, summonerName); example ["EUNE", "Kajakaboss"]
# WAIT
# FUNC -> dict {id: summonerId, accountId: accountId, etc};
# example      {id: 123123123, accountId: 121231231, etc}


def spec(id): # Siin saame infot käimasoleva mängu kohta (overall) [kui mängu pole, siis tuleb 404 error!]
    url = "https://na1.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/"+str(id)+"?api_key="+api_key
    json_data = urlopen(url)
    andmed = json.load(json_data)
    return andmed
