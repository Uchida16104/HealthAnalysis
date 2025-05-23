import os, requests, json
from datetime import datetime, timedelta

API_KEY_MACOS   = os.environ['RESCUETIME_API_KEY_MACOS']
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
    return next((item for item in data if item['date'] == date_str), None)

summary_macos  = extract_summary(data_macos, yesterday)  or {}
summary_ipad   = extract_summary(data_ipad, yesterday)   or {}
summary_pixel9 = extract_summary(data_pixel9, yesterday) or {}

devices = {
    'macOS':  summary_macos.get('software_development_percentage', 0),
    'iPad':   summary_ipad.get('communication_and_scheduling_percentage', 0),
    'Pixel9': summary_pixel9.get('social_networking_percentage', 0)
}

os.makedirs('data', exist_ok=True)
history_path = 'data/usage.json'
try:
    with open(history_path, 'r') as f:
        history = json.load(f)
        if isinstance(history, dict):
            history = [history]
except (FileNotFoundError, json.JSONDecodeError):
    history = []

history = [h for h in history if h.get('date') != yesterday]

if history:
    base = history[0]['devices']
    devices_independent = {
        name: max(devices.get(name, 0) - base.get(name, 0), 0)
        for name in devices
    }
else:
    devices_independent = devices

history.append({'date': yesterday, 'devices': devices_independent})

with open(history_path, 'w') as f:
    json.dump(history, f, indent=2)

print(f"Saved usage data for {yesterday}: {devices_independent}")
