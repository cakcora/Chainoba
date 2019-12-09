# Anomaly

Please put your function signatures in the driver.py file. The actual implementation of the functions are not included 
in this file.

## Driver Functions
 -  `pump_dump(f_path, volume_thresh, price_thresh, window_size, candle_size)`
	 - Calls the main analysis function to detect crypto currency pump and dumps.
	 - Needs a .csv file input of exchange data gathered via pull_xchange_data.py.
	 - Returns dataframe with exchange name, symbol name, price spikes, volume spikes, number of alleged pumps and number of pump and dumps.

