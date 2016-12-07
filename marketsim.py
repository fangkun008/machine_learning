#marketsim

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



def get_timestamps(date_lists):
	dt_start = date_lists[0]
	dt_end = date_lists[-1] + dt.timedelta(days=1)
	dt_timeofday = dt.timedelta(hours=16)
	ldt_timestamps = du.getNYSEdays(dt_start,dt_end,dt_timeofday)
	return ldt_timestamps

def get_data(ldt_timestamps,symbol_list):
	
	c_dataobj = da.DataAccess('Yahoo',cachestalltime=0)
	ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
	ldf_data = c_dataobj.get_data(ldt_timestamps, symbol_list, ls_keys)
	d_data = dict(zip(ls_keys, ldf_data))	
	return d_data

def find_date(order_file):
	csvfile = open(order_file,'rU')
	reader = csv.reader(csvfile,delimiter=',')
	sortedlist = sorted(reader,key=lambda x:(int(x[0]),int(x[1]),int(x[2])))
	date_lists = []
	for row in sortedlist:
		time_list = dt.datetime(int(row[0]),int(row[1]), int(row[2]))
		date_lists.append(time_list)	
	return date_lists

def find_symboles(order_file):
	csvfile = open(order_file,'rU')
	reader = csv.reader(csvfile,delimiter=',')
	symbol_list = []
	for row in reader:
		symbol_list.append(row[3])
	symbol_list = list(set(symbol_list))
	csvfile.close()
	return symbol_list

def mark_shares(df_trade_matrix, order_file):
	csvfile = open(order_file,'rU')
	reader = csv.reader(csvfile,delimiter=',')
	sortedlist = sorted(reader,key=lambda x:(int(x[0]),int(x[1]),int(x[2])))
	for row in sortedlist:
		time_index = dt.datetime(int(row[0]),int(row[1]), int(row[2])) + dt.timedelta(hours=16)
		symbol = row[3]
		if row[4] == 'Buy':
			buysell = 1
		else:
			buysell = -1
		shares = int(row[5])
		df_trade_matrix.loc[time_index,symbol] += buysell * shares
	return df_trade_matrix

def calcu_portfolio(init_cash, df_trade_matrix_marked, d_data):	
	holding_flow = np.cumsum(df_trade_matrix_marked.values, axis = 0)
	valuse_flow = np.sum(holding_flow * d_data['close'].values, axis = 1)
	cash_flow = np.zeros(len(df_trade_matrix_marked.index))
	cash_flow[0] = init_cash
	cash_used_gain = np.sum(df_trade_matrix_marked.values * d_data['close'].values, axis = 1) * -1
	cash_used_gain[0] += init_cash
	cash_flow = np.cumsum(cash_used_gain, axis = 0)
	portfolio = cash_flow + valuse_flow
	#print portfolio
	return portfolio
	

def marketsim(init_cash, order_file, value_file):
	init_cash = float(init_cash)
	symbol_list = find_symboles(order_file)
	date_lists = find_date(order_file)
	ldt_timestamps = get_timestamps(date_lists)
	d_data = get_data(ldt_timestamps,symbol_list)
	na_vals = np.zeros((len(ldt_timestamps), len(symbol_list)))	
	df_trade_matrix = pd.DataFrame(na_vals,index = [ldt_timestamps], columns = symbol_list)
	df_trade_matrix_marked = mark_shares(df_trade_matrix, order_file)	
	portfolio = calcu_portfolio(init_cash, df_trade_matrix_marked, d_data)
	portfolio_column = ['portfolio']	
	df_portfolio = pd.DataFrame(portfolio, index = [ldt_timestamps], columns = portfolio_column)
	df_portfolio.to_csv(value_file)
	


if __name__ == '__main__':
	print "Program name:", sys.argv[0]
	init_cash = sys.argv[1]
	order_file = sys.argv[2]
	value_file = sys.argv[3]

	marketsim(init_cash, order_file, value_file)