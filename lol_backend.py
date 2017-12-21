# Import stuff to backend
from urllib.request import urlopen
import json

# Here goes all the backend functions
def printTest():
    print("Test successful")

# Siin saame info kasutaja kohta
# [r- UIselectedRegion, summonerName]
def getData(r, n, api_key):
    region = "eun1" if (r=="EUNE") else "euw1" if (r=="EUW") else "na1"
    url = "https://<REGION>.api.riotgames.com/lol/summoner/v3/summoners/by-name/<NAME>?api_key="+api_key
    url.replace('<REGION>', region)
    url.replace('<NAME>', n)
    json_data = urlopen(url)
    data = json.load(json_data)
    return data
