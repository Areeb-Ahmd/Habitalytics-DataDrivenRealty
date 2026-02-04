import pandas as pd
import pickle
import requests
from bs4 import BeautifulSoup
import time
import os
import sys

# Force output to appear immediately
sys.stdout.reconfigure(encoding='utf-8')

print("--- SCRIPT STARTED ---")

def generate_image_database():
    # 1. Debug Directory
    current_dir = os.getcwd()
    print(f"Current Working Directory: {current_dir}")
    
    # 2. Check for dataset
    file_path = os.path.join(current_dir, 'datasets', 'link_loc.pkl')
    print(f"Looking for file at: {file_path}")
    
    if not os.path.exists(file_path):
        print("\n!!!!!!!!!!!!!! ERROR !!!!!!!!!!!!!!")
        print(f"Could not find: {file_path}")
        print("Make sure you are running this command from the PROJECT ROOT folder.")
        print("Your 'datasets' folder must be visible next to this script.")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return

    # 3. Load Data
    try:
        print("Loading pickle file... (this might take a second)")
        link_loc = pickle.load(open(file_path, 'rb'))
        print(f"Successfully loaded data. Found {len(link_loc)} properties.")
    except Exception as e:
        print(f"Error loading pickle file: {e}")
        return

    # 4. Setup Session
    session = requests.Session()
    mobile_headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1'
    }

    image_data = []
    count = 0
    total = len(link_loc)

    print("\n--- STARTING SCRAPING LOOP ---")
    
    # 5. Loop
    for property_name, url_series in link_loc.items():
        count += 1
        
        # Extract URL safely
        try:
            if hasattr(url_series, 'values'):
                url = url_series.values[0]
            else:
                url = url_series
        except:
            url = None

        # Print progress every item to ensure it's working
        print(f"Processing {count}/{total}: {property_name[:30]}...")

        img_src = None
        
        if url and isinstance(url, str) and url.startswith('http'):
            try:
                response = session.get(url, headers=mobile_headers, timeout=5)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    img_element = soup.select_one('img[src*="99acres"]')
                    
                    if img_element and img_element.get('src'):
                        raw_src = img_element.get('src')
                        # Clean up URL
                        if raw_src.startswith('//'):
                            img_src = 'https:' + raw_src
                        elif raw_src.startswith('/'):
                            img_src = 'https://www.99acres.com' + raw_src
                        else:
                            img_src = raw_src
                            
                        # High quality replacement
                        img_src = img_src.replace('_med.jpg', '_large.jpg').replace('_small.jpg', '_large.jpg')
                        print(f"   -> FOUND IMAGE")
                    else:
                        print(f"   -> No image tag found")
                else:
                    print(f"   -> Failed (Status: {response.status_code})")
            except Exception as e:
                print(f"   -> Error: {e}")
        else:
            print("   -> No valid URL")
        
        # Save result
        image_data.append({
            'PropertyName': property_name, 
            'ImageURL': img_src
        })
        
        # Save CSV every 10 items (so you don't lose data if you stop it)
        if count % 10 == 0:
            temp_df = pd.DataFrame(image_data)
            temp_df.to_csv('datasets/property_images.csv', index=False)
            print("   (Progress Saved to CSV)")

        # Sleep to be polite
        time.sleep(1.0)

    # Final Save
    final_df = pd.DataFrame(image_data)
    final_df.to_csv('datasets/property_images.csv', index=False)
    print("\n--- DONE! ---")
    print(f"Saved {len(final_df)} rows to datasets/property_images.csv")

if __name__ == "__main__":
    generate_image_database()