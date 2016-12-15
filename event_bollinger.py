#CompInvesti Homework 6
#event study-bollinger
#2016 12 15
#By Frank FANG

import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import math
import sys
import numpy as np
import csv
import operator as op
import copy
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkstudy.EventProfiler as ep

def get_boll_value(d_data, ldt_timestamps, symbol):
	ls_symbol = [symbol]
	d_data = copy.deepcopy(d_data['close'])
	na_price = d_data[symbol].values	
	df_symbol = pd.DataFrame(na_price, index = ldt_timestamps, columns = ls_symbol)	
	symbol_rolling = df_symbol.rolling(window = 20)	
	symbol_mean = symbol_rolling.mean()	
	symbol_std = symbol_rolling.std()	
	symbol_bollinger_val = df_symbol.copy()	
	symbol_bollinger_val = symbol_bollinger_val * np.NAN	
	symbol_bollinger_val = (df_symbol - symbol_mean) / symbol_std	
	return symbol_bollinger_val


def find_event(argv_lis, bollinger_lis):
	dt_start = dt.datetime(int(argv_lis[0]), 1, 1)
	dt_end = dt.datetime(int(argv_lis[1]), 12, 31)
	spy500_year = argv_lis[2]
	ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
	dataobj = da.DataAccess('Yahoo')
	ls_symbols = dataobj.get_symbols_from_list(spy500_year)
	ls_symbols.append('SPY')
	ls_keys = ['close']
	ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
	d_data = dict(zip(ls_keys, ldf_data))
	for s_key in ls_keys:
		d_data[s_key] = d_data[s_key].fillna(method='ffill')
		d_data[s_key] = d_data[s_key].fillna(method='bfill')
		d_data[s_key] = d_data[s_key].fillna(1.0)
	df_close = d_data['close']
	ts_market = df_close['SPY']
	print "Finding Events"
	df_events = copy.deepcopy(df_close)
	df_events = df_events * np.NAN
	ldt_timestamps = df_close.index
	bollinger_trigger = float(bollinger_lis[0])
	bollinger_SPY = float(bollinger_lis[1])	
	SPY_bollinger_val = get_boll_value(d_data, ldt_timestamps, 'SPY')
	for s_sym in ls_symbols:
		symbol_bollinger_val = get_boll_value(d_data, ldt_timestamps, s_sym)
		for i in range(1, len(ldt_timestamps)):            
			f_bollinger_val_today = symbol_bollinger_val.ix[ldt_timestamps[i]].values
			SPY_bollinger_val_today = SPY_bollinger_val.ix[ldt_timestamps[i]].values
			f_bollinger_val_yest = symbol_bollinger_val.ix[ldt_timestamps[i - 1]].values			     
			if f_bollinger_val_today <= bollinger_trigger and f_bollinger_val_yest > bollinger_trigger:
				if SPY_bollinger_val_today >= bollinger_SPY:
					df_events[s_sym].ix[ldt_timestamps[i]] = 1
	plot_filename = 'bollinger_' + str(bollinger_trigger) + 'SPY_' + str(bollinger_SPY) + '.pdf'	
	print "Creating Study"
	ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename=plot_filename, b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')

if __name__ == '__main__':
	print "Program name:", sys.argv[0]	
	argv_str = raw_input("Input start year, end year, SPY500 year, seperated by ',': \n")
	bollinger_str = raw_input("Input bollinger value for event, and for SPY,seperated by ',': \n")
	bollinger_lis = bollinger_str.split(',')
	argv_lis = argv_str.split(',')
	find_event(argv_lis, bollinger_lis)
	
