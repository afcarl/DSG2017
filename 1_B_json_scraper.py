import json
import deezer
import time

'''
We need to collect the extra metadata.
'''

with open('keys.json') as data_file:    
    keys = json.load(data_file)

client = deezer.Client()

def json_scraper(key, output_folder_name):
    
    """
    key: Name of the ID.
    output_folder_name: Path to the output files.
    """

    for value in keys[key]:
        try:
            if output_folder_name == "user":
                 call_down = client.get_user(value).asdict()   
                    
            elif output_folder_name == "album":
                call_down = client.get_album(value).asdict()  
                
            elif output_folder_name == "genre": 
                call_down = client.get_genre(value).asdict()  
                
            elif output_folder_name == "media":
                call_down = client.get_track(value).asdict()  
                
            elif output_folder_name == "artist":      
                call_down = client.get_artist(value).asdict()
                
            with open("./dumps/" + output_folder_name + "/" + str(call_down["id"]) + ".json", 'w') as fp:    
                json.dump(call_down, fp)
            time.sleep(0.1)
            print(call_down)
        except:
            time.sleep(0.1)
            pass

        
'''
We collected metadata for 5 ID features.
'''

json_scraper("artist_id", "artist")
json_scraper("album_id", "album")
json_scraper("user_id", "user")
json_scraper("media_id", "media")
json_scraper("genre_id", "genre") 
