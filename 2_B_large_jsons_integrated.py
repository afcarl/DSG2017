import pandas as pd
import json
from collections import Counter

def json_readup(path):
    with open(path) as data_file:    
        data = json.load(data_file)
    return data
    
def change_the_dict(dict_in):
    
    for key in dict_in.keys():
        dict_in[key] = set(dict_in[key])
    return dict_in

def dataset_integrator(input_data, artist_dict, flow_dict, chart_dict, track_dict, album_dict):
    
    user_ids = map(lambda s: str(s), input_data["user_id"].tolist())
    artists = input_data["artist_id"].tolist()
    tracks = input_data["media_id"].tolist()
    albums = input_data["album_id"].tolist()
    
    artists_unique = artist_dict.keys()
    tracks_unique = track_dict.keys()
    albums_unique = album_dict.keys()
    flows_unique = flow_dict.keys()
    charts_unique = chart_dict.keys()
    

    new_artist, artist_aggregates = [],[]
    new_flow, flow_aggregates = [],[]
    new_track, track_aggregates = [],[]
    new_chart, chart_aggregates = [], [] 
    new_album, album_aggregates = [],[] 
    
    index = 0
    
    for i in range(0, len(user_ids)):
        index = index + 1
        print(index)
        if index % 20000 == 0:

            output = pd.DataFrame()
            output["artist_liked"] = new_artist
            output["artist_like_count"] = artist_aggregates

            output["in_flow"] = new_flow
            output["number_of_items_in_flow"] = flow_aggregates

            output["track_liked"] = new_track
            output["number_of_tracks_liked"] = track_aggregates

            output["chart_liked"] = new_chart
            output["number_of_charts_liked"] = chart_aggregates

            output["album_liked"] = new_album
            output["number_of_albums_liked"] = album_aggregates
            
            output.to_csv("./raw_dataset/train_pieces/train_" + str(index) + ".csv",sep = ",", index = None)
            
            new_artist, artist_aggregates = [],[]
            new_flow, flow_aggregates = [],[]
            new_track, track_aggregates = [],[]
            new_chart, chart_aggregates = [], [] 
            new_album, album_aggregates = [],[] 

        if user_ids[i] in artists_unique:
            if artists[i] in artist_dict[user_ids[i]]:
                new_artist = new_artist + [1]
  
            else:
                new_artist = new_artist + [0]
            artist_aggregates = artist_aggregates  + [len(artist_dict[user_ids[i]])]       
        else:
            new_artist = new_artist + [-1]
            artist_aggregates = artist_aggregates  + [0]  
    
        if user_ids[i] in flows_unique:
            if tracks[i] in flow_dict[user_ids[i]]:
                new_flow = new_flow + [1]  
            else:
                new_flow = new_flow+ [0]   
            flow_aggregates = flow_aggregates  + [len(flow_dict[user_ids[i]])]   
        else:
            new_flow = new_flow + [-1]
            flow_aggregates = flow_aggregates  + [0]

        if user_ids[i] in tracks_unique:
            if tracks[i] in track_dict[user_ids[i]]:
                new_track = new_track + [1]   
            else:
                new_track = new_track + [0]   
            track_aggregates = track_aggregates  + [len(track_dict[user_ids[i]])]   
        else:
            new_track = new_track + [-1]
            track_aggregates = track_aggregates  + [0]

        if user_ids[i] in charts_unique:
            if tracks[i] in chart_dict[user_ids[i]]:
                new_chart = new_chart + [1]    
            else:
                new_chart = new_chart + [0]   
            chart_aggregates = chart_aggregates  + [len(chart_dict[user_ids[i]])]   
        else:
            new_chart = new_chart + [-1]
            chart_aggregates = chart_aggregates  + [0]

        if user_ids[i] in albums_unique:
            if albums[i] in album_dict[user_ids[i]]:
                new_album = new_album + [1]   
            else:
                new_album = new_album + [0]   
            album_aggregates = album_aggregates  + [len(album_dict[user_ids[i]])]   
        else:
            new_album = new_album + [-1]
            album_aggregates = album_aggregates  + [0]

    output = pd.DataFrame()
    
    output["artist_liked"] = new_artist
    output["artist_like_count"] = artist_aggregates

    output["in_flow"] = new_flow
    output["number_of_items_in_flow"] = flow_aggregates

    output["track_liked"] = new_track
    output["number_of_tracks_liked"] = track_aggregates

    output["chart_liked"] = new_chart
    output["number_of_charts_liked"] = chart_aggregates

    output["album_liked"] = new_album
    output["number_of_albums_liked"] = album_aggregates
    return output, index
 

def run_this():
    
    test = pd.read_csv("./raw_dataset/test.csv",index_col = None) 
    train = pd.read_csv("./raw_dataset/train_deduplicated.csv",index_col = None)

    artist_dict = json_readup("./large_dumps/user_artists.json")
    flow_dict = json_readup("./large_dumps/user_flow.json")
    chart_dict = json_readup("./large_dumps/user_charts.json")
    track_dict = json_readup("./large_dumps/user_tracks.json")
    album_dict = json_readup("./large_dumps/user_albums.json")
    
    artist_dict = change_the_dict(artist_dict)
    flow_dict = change_the_dict(flow_dict)
    chart_dict = change_the_dict(chart_dict)
    track_dict = change_the_dict(track_dict)
    album_dict = change_the_dict(album_dict)
           
    new_test, test_index = dataset_integrator(test, artist_dict, flow_dict, chart_dict, track_dict, album_dict)
    new_train, train_index = dataset_integrator(train, artist_dict, flow_dict, chart_dict, track_dict, album_dict)

    new_test.to_csv("./raw_dataset/test_likes.csv",sep = ",", index = None)
    new_train.to_csv("./raw_dataset/train_pieces/train_" + str(train_index) + ".csv",sep = ",", index = None)
    
run_this()
