import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')

import pandas as pd
import urllib
import cv2
import numpy as np
import time

def image_crawler(file_name, id_column, link, image_path):
    
    """
    file_name: Name of the input file.
    id_column: Name of the column with links.
    link: Name of the column with links.
    image_path: Name of the output folder.
    """
    
    frame_with_links = pd.DataFrame.from_csv("./raw_dataset/" + file_name, sep = ",", index_col = None)

    links = frame_with_links[link].tolist() 
    ids = frame_with_links[id_column].tolist()
    
    for i in range(0,len(links)):
        proper_link = links[i]
        proper_id = ids[i]
        output_path = "./image/" + image_path + "/" + str(proper_id) + ".jpg"
        try:        
            resp = urllib.urlopen(proper_link)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            cv2.imwrite(output_path, image)
        except:
            pass
        time.sleep(0.1)

"""
Scraping the images.
"""
        
image_crawler("user_images.csv", "user_id", "link", "user")
image_crawler("artist_images.csv", "artist_id", "link", "artist")
image_crawler("album_images.csv", "user_id", "link", "album")
