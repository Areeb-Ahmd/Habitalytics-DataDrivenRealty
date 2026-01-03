from geopy.geocoders import Nominatim
import pandas as pd
import time

# Initialize geolocator
geolocator = Nominatim(user_agent="gurgaon_sector_locator")

data = []

# Iterate over sectors to get coordinates
for sector in range(1, 116):
    location_name = f"Sector {sector}, Gurgaon, Haryana, India"
    location = geolocator.geocode(location_name)
    
    if location:
        lat, lon = location.latitude, location.longitude
        print(f"{location_name} -> ({lat}, {lon})")
        data.append({'Sector': f'Sector {sector}', 'Latitude': lat, 'Longitude': lon})
    else:
        print(f"{location_name} -> Not found")
        data.append({'Sector': f'Sector {sector}', 'Latitude': None, 'Longitude': None})
    
    # Add a short delay to avoid hitting API rate limits
    time.sleep(1)

# Convert to DataFrame and save
df = pd.DataFrame(data)
df.to_csv('sector_coordinates.csv', index=False)

print("\n✅ Coordinates saved successfully!")