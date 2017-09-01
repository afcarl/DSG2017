import urllib, json
import time

dataset = {}

for i in range(0,20000):
    try:
        print(i)
        url = "https://api.deezer.com/user/" + str(i) + "/flow"
        time.sleep(0.2)

        response = urllib.urlopen(url)
        data = json.loads(response.read())
        if "data" in data.keys():
            data = data["data"]
            data = map(lambda s: s["id"], data)
            dataset[i] = data
    except:
        pass

with open('/home/benedek/Documents/dsg/dumps/user_flow.json', 'w') as fp:
    json.dump(dataset, fp)
