import os, requests, json
from datetime import datetime, timedelta

API_KEY_MACOS   = os.environ['B63RkBQOBjasyXEHrHojug50a1BBz_td41jTPXr9']
API_KEY_IPAD    = os.environ['RESCUETIME_API_KEY_IPAD']
API_KEY_PIXEL9  = os.environ['RESCUETIME_API_KEY_PIXEL9']

yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

url = 'https://www.rescuetime.com/anapi/daily_summary_feed'

def fetch_summary(api_key):
    params = {'key': api_key, 'format': 'json'}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()

data_macos  = fetch_summary(API_KEY_MACOS)
data_ipad   = fetch_summary(API_KEY_IPAD)
data_pixel9 = fetch_summary(API_KEY_PIXEL9)

def extract_summary(data, date_str):
    return next(item for item in data if item['date'] == date_str)

summary_macos  = extract_summary(data_macos, yesterday)
summary_ipad   = extract_summary(data_ipad, yesterday)
summary_pixel9 = extract_summary(data_pixel9, yesterday)

devices = {
    'macOS':  summary_macos.get('software_development_percentage'),
    'iPad':   summary_ipad.get('communication_and_scheduling_percentage'),
    'Pixel9': summary_pixel9.get('social_networking_percentage')
}

os.makedirs('data', exist_ok=True)
with open('data/usage.json', 'w') as f:
    json.dump({'date': yesterday, 'devices': devices}, f, indent=2)

print(f"Saved usage data for {yesterday}: {devices}")
