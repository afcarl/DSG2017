import glob
import json
import time
import urllib

'''
We need the songs in order to generate the MEL features.
'''

index = 0
jsons = glob.glob("./dumps/media/*json")

'''
Each song is downloaded from the API.
We use the already existing JSON files.
The songs are saved under their music identifiers.
Sleeps are needed for accomodating the API call number and exceptions are handled with a pass.
'''

for js in jsons:
    index = index + 1
    print(index)
    try:
        with open(js) as data_file:
            dataset = json.load(data_file)
            link = dataset["preview"]
            ID = dataset["id"]
            folder = "./music/" + str(ID) + ".mp3"   
            testfile = urllib.URLopener()
            testfile.retrieve(link, folder)
            time.sleep(0.1)
    except:
        pass
