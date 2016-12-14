#bollinger bands
# 2016,12,13
# By Frank FANG

import QSTK.qstkutil.DataAccess as da
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import sys
import QSTK.qstkutil.qsdateutil as du
import copy
import numpy as np

def get_symbol():
	ls_symbol = []
	symbol_input = raw_input("Type in the symbol: ")
	ls_symbol.append(symbol_input)
	return ls_symbol

def get_time(time_mark):
	print "Type in the", time_mark, "time, with the format 'year,month,day': "
	time_str = raw_input()
	time_lis = time_str.split(',')
	return time_lis

def get_data(ls_symbol, ldt_timestamps):	
	c_dataobj = da.DataAccess('Yahoo',cachestalltime=0)
	ls_keys = ['close']
	ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbol, ls_keys)
	d_data = dict(zip(ls_keys, ldf_data))	
	return d_data

def get_time_lis(start_time, end_time):
	dt_start = dt.datetime(int(start_time[0]),int(start_time[1]), int(start_time[2]))
	dt_end = dt.datetime(int(end_time[0]),int(end_time[1]), int(end_time[2]))
	dt_timeofday = dt.timedelta(hours=16)
	ldt_timestamps = du.getNYSEdays(dt_start,dt_end,dt_timeofday)
	return ldt_timestamps

def moving_average_ploting(symbol_mean, df_symbol, ldt_timestamps, ls_symbol):
	plt.clf()
	fig = plt.figure()
	plt.plot(ldt_timestamps, df_symbol.values)
	plt.plot(ldt_timestamps, symbol_mean.values)
	ls_names = [ls_symbol[0], 'Moving Avg.']
	plt.legend(ls_names)
	plt.ylabel('Adjusted Close')
	plt.xlabel('Date')
	fig.autofmt_xdate(rotation = 45)
	pdf_file_name = ls_symbol[0] + '_moving_avg.pdf'
	plt.savefig(pdf_file_name, format = 'pdf')

def bollinger_val_ploting(symbol_bollinger_val, symbol_mean, symbol_std, df_symbol, ldt_timestamps, ls_symbol):
	upper_band = symbol_mean + symbol_std
	lower_band = symbol_mean - symbol_std	
	fig = plt.figure(1)

	plt.subplot(211)
	plt.plot(ldt_timestamps, df_symbol.values)	
	plt.fill_between(ldt_timestamps, lower_band[ls_symbol[0]], upper_band[ls_symbol[0]], alpha=0.2, facecolor='#7EFF99')
	ls_names = [ls_symbol[0]]
	plt.legend(ls_names)
	plt.ylabel('Adjusted Close')	
	
	plt.subplot(212)
	plt.plot(ldt_timestamps, symbol_bollinger_val.values)
	plt.fill_between(ldt_timestamps, np.ones(len(ldt_timestamps)), np.ones(len(ldt_timestamps))*-1\
		, alpha=0.2, facecolor='#7EFF99')
	plt.ylabel('Bollinger Feature')
	fig.autofmt_xdate(rotation = 45)

	pdf_file_name = ls_symbol[0] + '_bollinger_val.pdf'
	plt.savefig(pdf_file_name, format = 'pdf')

def get_bollinger_val_of_symbol(d_data, ldt_timestamps, ls_symbol):
	na_price = d_data['close'].values
	df_symbol = pd.DataFrame(na_price, index = ldt_timestamps, columns = ls_symbol)	
	symbol_rolling = df_symbol.rolling(window = 20)	
	symbol_mean = symbol_rolling.mean()	
	symbol_std = symbol_rolling.std()	
	symbol_bollinger_val = df_symbol.copy()	
	symbol_bollinger_val = symbol_bollinger_val * np.NAN	
	symbol_bollinger_val = (na_price - symbol_mean) / symbol_std
	moving_average_ploting(symbol_mean, df_symbol, ldt_timestamps, ls_symbol)
	bollinger_val_ploting(symbol_bollinger_val, symbol_mean, symbol_std, df_symbol, ldt_timestamps, ls_symbol)
	return symbol_bollinger_val

def save_bollval(symbol_bollinger_val, ls_symbol):
	csv_file_name = ls_symbol[0] + '_bollingerVal.csv'
	symbol_bollinger_val.to_csv(csv_file_name)

if __name__ == '__main__':
	print "Program name:", sys.argv[0]
	ls_symbol = get_symbol()
	start_time = get_time('start')
	end_time = get_time('end')
	ldt_timestamps = get_time_lis(start_time, end_time)
	d_data = get_data(ls_symbol, ldt_timestamps)
	symbol_bollinger_val = get_bollinger_val_of_symbol(d_data, ldt_timestamps, ls_symbol)	
	save_bollval(symbol_bollinger_val, ls_symbol)
	
	

