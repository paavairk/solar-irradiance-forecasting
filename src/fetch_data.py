import os
import requests
import pandas as pd
import time

def fetch_nasa_power_data(lat=49.5910, lon=11.0078, start_date="20100101", end_date="20241231", max_retries=5):
    """
    Fetches daily GHI, Temperature, Cloud Amount, and Wind Speed from NASA POWER API.
    Includes a retry mechanism to handle 'Connection reset by peer' errors.
    """
    print(f"🛰️ Requesting data from NASA POWER API for Lat: {lat}, Lon: {lon}...")
    
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    parameters = ["ALLSKY_SFC_SW_DWN", "T2M", "CLOUD_AMT", "WS10M"]
    
    params = {
        "parameters": ",".join(parameters),
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "start": start_date,
        "end": end_date,
        "format": "JSON"
    }
    
    # Adding headers tells NASA who is calling, making the connection more stable
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) SolarIrradianceProject/1.0"
    }

    # Retry loop
    for attempt in range(1, max_retries + 1):
        try:
            print(f"🔄 Connection attempt {attempt} of {max_retries}...")
            response = requests.get(url, params=params, headers=headers, timeout=20)
            response.raise_for_status()
            data = response.json()
            break # Success! Break out of the retry loop
        except (requests.exceptions.RequestException, ConnectionResetError) as e:
            print(f"⚠️ Attempt {attempt} failed due to network glitch: {e}")
            if attempt == max_retries:
                print("❌ All retry attempts failed. The NASA API server might be down temporarily.")
                return None
            print("⏳ Waiting 5 seconds before trying again...")
            time.sleep(5)

    print("📊 Parsing API response into a clean table...")
    records = {}
    for param in parameters:
        records[param] = data["properties"]["parameter"][param]
        
    df = pd.DataFrame(records)
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    df.index.name = "date"
    df = df.reset_index()
    
    print(f"✅ Successfully retrieved {len(df)} days of historical data.")
    return df

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    
    ERLANGEN_LAT = 49.5910 
    ERLANGEN_LON = 11.0078
    
    df_erlangen = fetch_nasa_power_data(
        lat=ERLANGEN_LAT, 
        lon=ERLANGEN_LON, 
        start_date="20100101", 
        end_date="20241231"
    )
    
    if df_erlangen is not None:
        output_path = "data/raw/erlangen_nasa_power.csv"
        df_erlangen.to_csv(output_path, index=False)
        print(f"💾 Raw data saved successfully to: {output_path}")