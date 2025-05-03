import os, requests, json
from datetime import datetime, timedelta

API_KEY = os.environ['RESCUETIME_API_KEY']

yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')


url = 'https://www.rescuetime.com/anapi/daily_summary_feed'
params = {'key': API_KEY, 'format': 'json'}
resp = requests.get(url, params=params)
data = resp.json()


summary = next(item for item in data if item['date'] == yesterday)



devices = {
    'macOS': summary.get('software_development_percentage'),
    'iPad': summary.get('communication_and_scheduling_percentage'),
    'Pixel9': summary.get('social_networking_percentage')
}


with open('data/usage.json', 'w') as f:
    json.dump({'date': yesterday, 'devices': devices}, f, indent=2)
