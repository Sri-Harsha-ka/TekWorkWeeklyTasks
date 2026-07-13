# This is used to load the data from the data set 

import pandas as pd 
import os

class DataLoader: 
    def __init__(self , file_path):
        self.file_path = file_path
        
    def load_data(self):
        
        # ERROR Handling if needed
        # if not os.path.exists(self.file_path):
        #     raise FileNotFoundError(
        #         f"Dataset not found at:\n{self.file_path}"
        #     )
        
        df = pd.read_csv(self.file_path)
        
        # Displaying the first 5 rows 
        print(" ----- The First Five Rows ----- ")
        print(df.head())
        
        print(" The Info of the data ")
        print(df.info())
        
        df["Month"] = pd.to_datetime(df["Month"])
 
        print("\nData Types After Conversion")
        print(df.dtypes)
        
        df.set_index("Month", inplace=True)
        
        print(" ----- Final Data set ----- ")
        print(df.head())
        
        return df
    
if __name__ == "__main__":
 
    DATA_PATH = "./data/airline-passengers.csv"
 
    loader = DataLoader(DATA_PATH)
 
    df = loader.load_data()
 
    print("\nProcessed Dataset")
    print(df.head())