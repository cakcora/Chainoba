## api/pull_xchange_data.py
- [CCXT](https://github.com/ccxt/ccxt) library has been used to get exchange data. It provides a unified way to access the data from a variety of cryptocurrency exchanges.
-   Exchange data is returned as a set of Open High Low Close Volume (OHLCV) entries, detailing the trading data for that particular moment in time.
- All the data is saved as individual .csv files for each cryptocurrency pair. These files are grouped into folders based on the exchange it was pulled from. 
- `pull_data`function can be used to specify one or multiple exchanges to pull data from.
 
 ## analysis_pump_dump.py
- Analyses the exchange OHLCV data to detect cryptocurrency pump and dumps.
- `analyse_symbol` is the main function that carries out the analysis.
 - Analysis framework has been referred from:  
Kamps, Josh & Kleinberg, Bennett. (2018). To the moon: defining and detecting cryptocurrency pump-and-dumps. Crime Science. 7. 10.1186/s40163-018-0093-5.

