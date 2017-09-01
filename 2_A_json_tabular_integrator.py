import json
import glob
import pandas as pd

'''
We need to integrate the obtained json files.
'''

def json_integrator(columns, input_path, new_columns):
    
    """
    columns: Name of colums to be processed.
    input_path: Path to the csv dumps
    new_columns:  Name of the new columns.
    """
    
    jsons = glob.glob("./dumps/" + input_path + "/*json")
    overall_dataset =[]
    index = 0
    
    for js in jsons:
        index = index + 1
        with open(js) as data_file:
            dataset = json.load(data_file)
            new_dataset = []
            
            if "id" in dataset.keys():
                new_dataset = new_dataset +[dataset["id"]]
            else:
                 new_dataset = new_dataset + [int(js.split("/")[-1].replace(".json",""))]       
            for col in columns:
                if col in dataset.keys():
                    if not isinstance(dataset[col],list):
                        try:
                            dataset[col] = str(dataset[col])
                            new_dataset = new_dataset +[dataset[col]]
                        except:
                            new_dataset = new_dataset + [""]
                    else:
                        new_dataset = new_dataset +[len(list(dataset[col]))]
                else:
                    new_dataset = new_dataset + [0]
    
        overall_dataset = overall_dataset + [new_dataset]
    
    
    overall_dataset = pd.DataFrame(overall_dataset, index = None)
    
    overall_dataset.columns = new_columns
    overall_dataset.to_csv("./raw_dataset/"+ input_path + "_augmented_data.csv", sep = ",", index = None)

#################################################################################
#-------------------------------------------------------------------------------#
#-----------------------ARTIST DATA INTEGRATION---------------------------------#
#-------------------------------------------------------------------------------#
#################################################################################

columns = ["radio", "nb_album", "nb_fan"]
input_path = "artist"
new_columns = ["artist_id", "artist_radio", "artist_albums_num", "artist_fans"]

json_integrator(columns, input_path, new_columns)

#################################################################################
#-------------------------------------------------------------------------------#
#-------------------------ALBUM DATA INTEGRATION--------------------------------#
#-------------------------------------------------------------------------------#
#################################################################################

columns = ["available", "duration", "explicit_lyrics", "fans", "nb_tracks", "record_type", "label"]
input_path = "album"
new_columns = ["album_id",
               "album_available",
               "album_duration",
               "album_explicit",
               "album_fans",
               "album_nb_tracks",
               "album_record_type",
               "album_label"]   

json_integrator(columns, input_path, new_columns)

#################################################################################
#-------------------------------------------------------------------------------#
#--------------------------MEDIA DATA INTEGRATION-------------------------------#
#-------------------------------------------------------------------------------#
#################################################################################

columns = ["available_countries", "disk_number", "explicit_lyrics", "gain", "rank", "contributors", "track_position", "type", "bpm"]
input_path = "media"
new_columns = ["media_id",
               "track_available_countries",
               "track_disk_number", "track_explicit",
               "track_gain","track_rank",
               "track_contri",
               "track_posi",
               "track_type",
               "track_bpm"]

json_integrator(columns, input_path, new_columns)

#################################################################################
#-------------------------------------------------------------------------------#
#---------------------------USER DATA INTEGRATION-------------------------------#
#-------------------------------------------------------------------------------#
#################################################################################

columns = ["country"]
input_path = "user"
new_columns = ["user_id", "nationality"]

json_integrator(columns, input_path, new_columns)
