# The Preprocessing of the data is write here 

import joblib 
import pandas as pd 

from sklearn.preprocessing import MinMaxScaler

class Preprocessor: 
    
    def __init__(self):
        self.sc = MinMaxScaler(feature_range=(0,1))
        
    def scale_data(self , df): 
        sc_values = self.sc.fit_transform(df[['Passengers']])
        
        sc_df = pd.DataFrame(sc_values , columns=["Passengers"] ,index=df.index)
        
        joblib.dump(self.sc , "models/scaler.pkl")
        
        return sc_df

if __name__ == "__main__":
 
    from src.data_loader import DataLoader
 
    DATA_PATH = "./data/airline-passengers.csv"

    loader = DataLoader(DATA_PATH)
    df = loader.load_data()
 
    preprocessor = Preprocessor()
 
    scaled_df = preprocessor.scale_data(df)
 
    print("\nScaled Dataset")
    print(scaled_df.head())