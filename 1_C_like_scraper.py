import urllib, json
import time
import math

'''
Scraping the albums liked by the users.
'''

def scrape_down_likes(folder, output_path):
    
    large_dict = {}

    for i in range(0, 20000):
        print(i)
        try:
            time.sleep(0.2)
            likes = []
            control = 0
            url = "https://api.deezer.com/user/" + str(i) + folder
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            if "total" in data:
                control = data["total"]
                if control > 0:
                    interesting = data["data"]
                    counts = int(math.ceil(float(data["total"]) / 25))
                    if counts > 0:
                        for j in range(0, counts - 1):
                            time.sleep(0.2)
                            response = urllib.urlopen(data["next"])
                            data = json.loads(response.read())
                            interesting = interesting + data["data"]
                    likes = likes + map(lambda s: s["id"], interesting)
                    large_dict[i] = likes
        except:
            pass
    
    with open(output_path, 'w') as fp:
        json.dump(large_dict, fp)

scrape_down_likes("/albums", "/home/benedek/Documents/dsg/dumps/user_albums.json")
scrape_down_likes("/artists", "/home/benedek/Documents/dsg/dumps/user_artists.json")
scrape_down_likes("/charts", "/home/benedek/Documents/dsg/dumps/user_charts.json")
scrape_down_likes("/tracks", "/home/benedek/Documents/dsg/dumps/user_song.json")
