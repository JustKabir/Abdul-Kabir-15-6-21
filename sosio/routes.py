import requests
from sosio import app
from flask import render_template
import json
import csv
import pandas as pd

expirey = "24-Jun-2021"
headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

def fetch_oi():
	r = requests.get(url, headers = headers)
	req = json.loads(r.text)
	if expirey:
		ce_values = [data['CE']for data in req['records']['data'] if "CE" in data and str(data['expiryDate']).lower() == str(expirey).lower()] 
		pe_values = [data['PE']for data in req['records']['data'] if "PE" in data and str(data['expiryDate']).lower() == str(expirey).lower()] 
	else:
		ce_values = [data['CE']for data in req['filtered']['data'] if "CE" in data] 
		pe_values = [data['PE']for data in req['filtered']['data'] if "PE" in data] 
	
	ce_data = pd.DataFrame(ce_values)
	pe_data = pd.DataFrame(pe_values)
	ce_data = ce_data.sort_values(['strikePrice'])
	pe_data = pe_data.sort_values(['strikePrice'])
	
	with open('pe_data.txt', 'w') as f:
		f.write(str(pe_data))
	with open('ce_data.txt', 'w') as f:
		f.write(str(ce_data))
	
	

@app.route('/')
def index():
	fetch_oi()
	return render_template('index.html')
	