import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as tf

def get_sec_filing(ticker, filing_type='10-K'):
    base_url = "https://www.sec.gov/cgi-bin/browse-edgar"
    params = {
        'CIK': ticker,
        'type': filing_type,
        'output': 'atom'
    }
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, 'xml')
    entries = soup.find_all('entry')
    
    # Get latest filing
    if entries:
        latest = entries[0]
        accession_no = latest.id.text.split('/')[-1]
        return f"https://www.sec.gov/Archives/edgar/data/{ticker}/{accession_no}.txt"


def get_financial_news(api_key, company):
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={api_key}"
    response = requests.get(url)
    return response.json()['articles']

def get_stock_data(ticker, period='1y'):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist