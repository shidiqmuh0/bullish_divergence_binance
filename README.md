# README.md

## Bullish Divergence Detector for Binance

This script analyzes cryptocurrency pairs on Binance to detect bullish divergences using MACD and RSI indicators. A bullish divergence occurs when the price of a cryptocurrency makes a lower low, but the indicator makes a higher low, signaling a potential price reversal.

### Features
- Fetches OHLCV data for multiple symbols from Binance.
- Calculates MACD and RSI indicators.
- Detects bullish divergences based on MACD and RSI.
- Lists symbols that exhibit bullish divergence.

### Prerequisites
- Python 3.x
- `pandas` library
- `numpy` library
- `ccxt` library
- `ta` library

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/shidiqmuh0/bullish_divergence_binance.git
   cd bullish_divergence_binance
   ```

2. Install the required Python packages:
   ```bash
   pip install pandas numpy ccxt ta
   ```

### Usage
Run the script to detect symbols with bullish divergence:

```bash
python app.py
```

## Result

![image](https://github.com/shidiqmuh0/bullish_divergence_binance/assets/57977381/9de53e51-a16c-49f6-bf4c-de33bd990b1e)


### Script Explanation

#### 1. Initialize the Binance Exchange
```python
exchange = ccxt.binance()
```

#### 2. Fetch OHLCV Data
The `fetch_ohlcv` function retrieves OHLCV (Open, High, Low, Close, Volume) data for a given symbol and timeframe from Binance.
```python
def fetch_ohlcv(symbol, timeframe='1h', limit=500):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df
```

#### 3. Calculate MACD
The `calculate_macd` function computes the MACD (Moving Average Convergence Divergence) indicator.
```python
def calculate_macd(df):
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['signal'] = macd.macd_signal()
    df['macd_hist'] = macd.macd_diff()
```

#### 4. Calculate RSI
The `calculate_rsi` function computes the RSI (Relative Strength Index) indicator.
```python
def calculate_rsi(df):
    rsi = ta.momentum.RSIIndicator(df['close'], window=14)
    df['rsi'] = rsi.rsi()
```

#### 5. Detect Bullish Divergence
The `detect_bullish_divergence` function checks for bullish divergence based on MACD and RSI indicators.
```python
def detect_bullish_divergence(df):
    bullish_divergence_macd = False
    bullish_divergence_rsi = False
    
    macd_lows = df.loc[df['macd_hist'] < 0, 'macd_hist']
    price_lows = df.loc[df['macd_hist'] < 0, 'close']
    if len(macd_lows) >= 2 and price_lows.iloc[-1] > price_lows.iloc[-2] and macd_lows.iloc[-1] < macd_lows.iloc[-2]:
        bullish_divergence_macd = True
    
    rsi_lows = df.loc[df['rsi'] < 30, 'rsi']
    if len(rsi_lows) >= 2 and df['close'].iloc[-1] > df['close'].iloc[-len(rsi_lows)] and rsi_lows.iloc[-1] < rsi_lows.iloc[-len(rsi_lows)]:
        bullish_divergence_rsi = True
    
    return bullish_divergence_macd and bullish_divergence_rsi
```

#### 6. Analyze Symbols
The script fetches the list of available symbols from Binance, analyzes each one for bullish divergence, and prints the symbols that exhibit bullish divergence.
```python
markets = exchange.load_markets()
symbols = [symbol for symbol in markets.keys() if '/USDT' in symbol]

bullish_divergence_symbols = []

for symbol in symbols:
    try:
        df = fetch_ohlcv(symbol)
        calculate_macd(df)
        calculate_rsi(df)
        
        if detect_bullish_divergence(df):
            bullish_divergence_symbols.append(symbol)
    except Exception as e:
        print(f"Could not analyze {symbol}: {e}")

print("Symbols with bullish divergence:", bullish_divergence_symbols)
```

### Repository
The code is available at [GitHub](https://github.com/shidiqmuh0/bullish_divergence_binance.git).

### License
This project is licensed under the MIT License.

---

This `README.md` provides an overview of the script, its features, prerequisites, installation steps, and a detailed explanation of each part of the script.
