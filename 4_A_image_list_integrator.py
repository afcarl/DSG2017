import json
import glob
import pandas as pd

def json_integrator(path_name, id_column, picture_column_to_test, new_id_name, link_name, output_path):
    
    """
    :path_name:
    :id_column:
    :picture_column_to_test:
    :new_id_name:
    :link_name:
    :output_path:
    """
    
    jsons = glob.glob("./dumps/" + path_name + "/*json")

    overall_dataset = []

    for js in jsons:
        with open(js) as data_file:
            dataset = json.load(data_file)
            new_dataset = []
            if id_column in dataset.keys():
                new_dataset = new_dataset +[dataset[id_column]]
            else:
                new_dataset = new_dataset + [ int(js.split("/")[-1].replace(".json",""))]
        
            if picture_column_to_test in dataset.keys():
                new_dataset = new_dataset +[dataset[picture_column_to_test]]
            else:
                new_dataset = new_dataset + [0]

        overall_dataset = overall_dataset + [new_dataset]

    js_data = pd.DataFrame(overall_dataset, index = None)
    js_data.columns = [new_id_name, link_name]
    js_data.to_csv("./raw_dataset/" + output_path, sep = ",", index_col = None)

json_integrator("artist", "id", "picture", "artist_id", "link", "artist_images.csv")
json_integrator("user", "id", "picture", "user_id", "link", "user_images.csv")
json_integrator("album", "id", "cover", "album_id", "link", "album_images.csv")
