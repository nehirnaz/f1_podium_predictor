import pandas as pd

def load_and_merge_data():
    # 1. Load the core CSVs
    print("Loading CSVs...")
    results = pd.read_csv("data/results.csv")
    races = pd.read_csv("data/races.csv")
    drivers = pd.read_csv("data/drivers.csv")
    constructors = pd.read_csv("data/constructors.csv")
    
    # 2. Merge Results with Races
    df = pd.merge(results, races[['raceId', 'year', 'round', 'circuitId', 'name', 'date']], on='raceId', how='left')
    
    # 3. Merge with Drivers
    df = pd.merge(df, drivers[['driverId', 'driverRef', 'code']], on='driverId', how='left')
    
    # 4. Merge with Constructors 
    df = pd.merge(df, constructors[['constructorId', 'constructorRef']], on='constructorId', how='left')
    
    # 5. Rename columns
    df.rename(columns={
        'name': 'gp_name',
        'positionOrder': 'finish_position',
        'grid': 'grid_position',
        'constructorRef': 'team',
        'driverRef': 'driver'
    }, inplace=True)
    
    # 6. Filter: Keep only data from 1980 onwards
    # Using older data (1950s) can confuse the model due to different rules/cars
    df = df[df['year'] >= 2000]
    
    print(f"Merged Data Shape: {df.shape}")
    print(f"Years covered: {df['year'].min()} to {df['year'].max()}")
    
    return df

if __name__ == "__main__":
    df = load_and_merge_data()
    
    # Save this cleaned version
    df.to_csv("data/f1_merged_data.csv", index=False)
    print("Saved merged dataset to 'data/f1_merged_data.csv'")
    
