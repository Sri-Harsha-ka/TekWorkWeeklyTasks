# Generating teh swquence for time stamps of RNN / LSTM 

import numpy as np 

class SequenceGenerator: 
    
    def __init__(self , sequence_length = 12): 
        
        self.sequence_length = sequence_length
    
    def create_sequences(self , scaled_df):
        
        X = []
        y = []
        
        data = scaled_df.values
        for i in range(len(data) - self.sequence_length):
            X.append(data[i:i+self.sequence_length])

            y.append(data[i+self.sequence_length])
        
        X = np.array(X)
        y = np.array(y)
 
        print("\nSequence Generation Completed.")
 
        print(f"Input Shape : {X.shape}")
 
        print(f"Output Shape : {y.shape}")
 
        return X, y

if __name__ == "__main__":
 
    from src.data_loader import DataLoader
    from src.preprocessing import Preprocessor
 
    DATA_PATH = "./data/airline-passengers.csv"
 
    # Load dataset
    loader = DataLoader(DATA_PATH)
    df = loader.load_data()
 
    # Scale dataset
    preprocessor = Preprocessor()
    scaled_df = preprocessor.scale_data(df)
 
    # Generate sequences
    generator = SequenceGenerator(sequence_length=12)
 
    X, y = generator.create_sequences(scaled_df)
 
    print("\nFirst Input Sequence\n")
    print(X[0])
 
    print("\nFirst Target\n")
    print(y[0])