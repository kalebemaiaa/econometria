import numpy as np
import pandas as pd
import json
import sys

import pnadcibge

if __name__ == "__main__":
    FOLDER_PATH = "/home/lucasfelipe/Documents/PNADC_032019_20220916"
    
    with open("./RV.json") as f:
        random_variables = json.load(f)
    
    dict_paths = pnadcibge.download_data(year=2019, trimestre=3)
    if dict_paths is None:
        print("Deu merda")
        sys.exit(1)
    dict_paths = pnadcibge.extract_data(paths = dict_paths)
    
    df = pnadcibge.create_dataframe(dict_paths, 
                               columns_intrested=random_variables.keys(), 
                               sample_size=0.1, 
                               random_seed=221704017)
    df.to_csv("./pnad_3T19.csv")