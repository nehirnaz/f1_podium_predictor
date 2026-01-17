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
    
    # Sort by Year and Round (Crucial for calculating points over time)
    df = df.sort_values(by=['year', 'round'])
    
    # 5. Get Driver Points Before Race
    # Group by year and driver, then take a cumulative sum of points.
    # shift(1) to get the points BEFORE this race.
    df['driver_points_before'] = df.groupby(['year', 'driverRef'])['points'].cumsum().shift(1)
    
    # The first race of the season will be NaN, so fill with 0
    df['driver_points_before'] = df['driver_points_before'].fillna(0)
    
    # Safety check: ensure
    df.loc[df['round'] == 1, 'driver_points_before'] = 0

    # 6. Rename columns
    df.rename(columns={
        'name': 'gp_name',
        'positionOrder': 'finish_position',
        'grid': 'grid_position',
        'constructorRef': 'team',
        'driverRef': 'driver'
    }, inplace=True)
    
    # 7. Filter: Keep only data from 1980 onwards
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
    
# Check if it worked
    print("\nSample: Hamilton 2021 (Notice points increasing?)")
    check = df[(df['driver'] == 'hamilton') & (df['year'] == 2021)][['round', 'driver_points_before', 'points']]
    print(check.head())