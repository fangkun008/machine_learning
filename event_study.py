#CompInvesti Homework 4
#2016-12-12
#Fang Kun

import QSTK.qstkutil.qsdateutil as du
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

def find_event(argv_lis):
	dt_start = dt.datetime(int(argv_lis[0]), 1, 1)
	dt_end = dt.datetime(int(argv_lis[1]), 12, 31)
	spy500_year = argv_lis[3]
	ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

	dataobj = da.DataAccess('Yahoo')
	ls_symbols = dataobj.get_symbols_from_list(spy500_year)
	ls_symbols.append('SPY')

	ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
	ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
	d_data = dict(zip(ls_keys, ldf_data))

	for s_key in ls_keys:
		d_data[s_key] = d_data[s_key].fillna(method='ffill')
		d_data[s_key] = d_data[s_key].fillna(method='bfill')
		d_data[s_key] = d_data[s_key].fillna(1.0)		

	df_close = d_data['actual_close']
	ts_market = df_close['SPY']
	print "Finding Events"

	df_events = copy.deepcopy(df_close)

	ldt_timestamps = df_close.index
	event_price = float(argv_lis[2])
	order_lis = []

	for s_sym in ls_symbols:
		for i in range(1, len(ldt_timestamps)):            
			f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
			f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]            

            # Event is found if the symbol     
            # price[t-1] >= 5.0
    		# price[t] < 5.0             
			if f_symprice_today < event_price and f_symprice_yest >= event_price:
				time_lis = ldt_timestamps[i].strftime("%Y,%m,%d").split(',')
				buy_order = [time_lis[0], time_lis[1], time_lis[2], s_sym, 'Buy', '100']
				if i + 5 >= len(ldt_timestamps):
					time_lis = ldt_timestamps[-1].strftime("%Y,%m,%d").split(',')
				else:
					time_lis = ldt_timestamps[i + 5].strftime("%Y,%m,%d").split(',')
				sell_order = [time_lis[0], time_lis[1], time_lis[2], s_sym, 'Sell', '100']
                #order_str = ldt_timestamps[i].strftime("%Y,%m,%d") + ',' + s_sym \
				#+ ',' + 'Buy' + ',' + '100'				
				order_lis.append(buy_order)
				#order_str = ldt_timestamps[i + 5].strftime("%Y,%m,%d") + ',' + s_sym \
				#+ ',' + 'Sell' + ',' + '100'				
				order_lis.append(sell_order)
				


	return order_lis

def write_to_csv(order_lis):
	writer = csv.writer(open('orders.csv', 'wb'))
	for item in order_lis:
		writer.writerow(item)


if __name__ == '__main__':
	print "Program name:", sys.argv[0]	
	argv_str = raw_input("Input start year, end year, event price, SPY500 year, seperated by ',': \n")
	argv_lis = argv_str.split(',')
	order_lis = find_event(argv_lis)
	write_to_csv(order_lis)
	