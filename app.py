import pandas as pd
import numpy as np
import ccxt
import ta
from datetime import datetime, timedelta

# Initialize the Binance exchange
exchange = ccxt.binance()

# Function to fetch OHLCV data
def fetch_ohlcv(symbol, timeframe='1h', limit=500):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Function to calculate MACD
def calculate_macd(df):
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['signal'] = macd.macd_signal()
    df['macd_hist'] = macd.macd_diff()

# Function to calculate RSI
def calculate_rsi(df):
    rsi = ta.momentum.RSIIndicator(df['close'], window=14)
    df['rsi'] = rsi.rsi()

# Function to detect bullish divergence
def detect_bullish_divergence(df):
    bullish_divergence_macd = False
    bullish_divergence_rsi = False
    
    # Bullish divergence on MACD
    macd_lows = df.loc[df['macd_hist'] < 0, 'macd_hist']
    price_lows = df.loc[df['macd_hist'] < 0, 'close']
    if len(macd_lows) >= 2 and price_lows.iloc[-1] > price_lows.iloc[-2] and macd_lows.iloc[-1] < macd_lows.iloc[-2]:
        bullish_divergence_macd = True
    
    # Bullish divergence on RSI
    rsi_lows = df.loc[df['rsi'] < 30, 'rsi']
    if len(rsi_lows) >= 2 and df['close'].iloc[-1] > df['close'].iloc[-len(rsi_lows)] and rsi_lows.iloc[-1] < rsi_lows.iloc[-len(rsi_lows)]:
        bullish_divergence_rsi = True
    
    return bullish_divergence_macd and bullish_divergence_rsi

# Fetch the list of symbols available on Binance
markets = exchange.load_markets()
symbols = [symbol for symbol in markets.keys() if '/USDT' in symbol]

# User input for timeframe
timeframe = input("Choose timeframe (1h, 4h, 1d): ").strip()

# Analyze each symbol
bullish_divergence_symbols = []

for symbol in symbols:
    try:
        df = fetch_ohlcv(symbol, timeframe=timeframe)
        calculate_macd(df)
        calculate_rsi(df)
        
        if detect_bullish_divergence(df):
            bullish_divergence_symbols.append(symbol)
    except Exception as e:
        print(f"Could not analyze {symbol}: {e}")

print("Symbols with bullish divergence:", bullish_divergence_symbols)
