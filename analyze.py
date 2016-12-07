#analyze--homework3 part2

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import math
import sys
import numpy as np

def plot_analyze(df_portfolio):
	fig = plt.figure()
	df_portfolio.plot()
	plt.legend(loc = 'best')
	plt.xlabel('Date')
	fig.autofmt_xdate(rotation=45)
	plt.savefig('analyze.pdf', format = 'pdf')

def pull_data(dt_start, dt_end, compare_symbol):
	da_timeofday = dt.timedelta(hours=16)
	ldt_timestamps = du.getNYSEdays(dt_start,dt_end,da_timeofday)
	c_dataobj = da.DataAccess('Yahoo',cachestalltime=0)
	ls_port_syms = []
	ls_port_syms.append(compare_symbol)
	ls_keys = ['close']
	ldf_data = c_dataobj.get_data(ldt_timestamps, ls_port_syms, ls_keys)
	d_data = dict(zip(ls_keys, ldf_data))
	na_price = d_data['close'].values	
	return na_price

def normalized_price(init_cash, na_price):
	na_normalized_price = na_price / na_price[0,:]
	na_rets = na_normalized_price.copy() * init_cash
	return na_rets

def get_symbol_data(df_portfolio,compare_symbol):
	dt_start = dt.datetime.strptime(df_portfolio.values[0,0].split()[0],'%Y-%m-%d') 
	dt_end = dt.datetime.strptime(df_portfolio.values[-1,0].split()[0],'%Y-%m-%d') + dt.timedelta(days=1)
	na_price = pull_data(dt_start, dt_end, compare_symbol)
	init_cash = df_portfolio.values[0,1]
	normalized_na_price = normalized_price(init_cash, na_price)
	return normalized_na_price

def calculate_ratios(df_portfolio, column_name):
	df_portfolio_copy = df_portfolio.copy()
	na_portrets = df_portfolio_copy[column_name]	
	tsu.returnize0(na_portrets)	
	na_port_total = np.cumprod(na_portrets + 1)	
	average_daily_rest = np.mean(na_portrets)	
	k = math.sqrt(252)
	volatility = np.std(na_portrets)
	sharp_ratio = k * average_daily_rest / volatility
	ratios_list = [sharp_ratio, na_port_total[-1], volatility, average_daily_rest]
	return ratios_list

def print_result(ratios_list_portfolio, ratios_list_compare, compare_symbol, df_portfolio):
	final_value = df_portfolio.values[-1,0].split()[0] + ' ' + str(df_portfolio.iloc[-1,1])
	data_range = df_portfolio.values[0,0].split()[0] + ' to ' + df_portfolio.values[-1,0].split()[0]
	print 'The final value of the portfolio using the sample file is --', final_value
	print
	print 'Details of the Performance of the portfolio'
	print
	print 'Data Range :', data_range
	print
	print 'Sharpe Ratio of Fund :', ratios_list_portfolio[0]
	print 'Sharpe Ratio of ' + compare_symbol + ' :', ratios_list_compare[0]
	print
	print 'Total Return of Fund :', ratios_list_portfolio[1]
	print 'Total Return of ' + compare_symbol + ' :', ratios_list_compare[1]
	print
	print 'Standard Deviation of Fund :', ratios_list_portfolio[2]
	print 'Standard Deviation of ' + compare_symbol + ' :', ratios_list_compare[2]
	print
	print 'Average Daily Return of Fund :', ratios_list_portfolio[3]
	print 'Average Daily Return of ' + compare_symbol + ' :', ratios_list_compare[3]

def analyze(portfolio_file, compare_symbol):
	df_portfolio = pd.read_csv(portfolio_file)	
	normalized_na_price = get_symbol_data(df_portfolio,compare_symbol)	
	df_portfolio[compare_symbol] = normalized_na_price
	df_portfolio.index = df_portfolio.iloc[:,0].tolist()
	plot_analyze(df_portfolio)	
	ratios_list_portfolio = calculate_ratios(df_portfolio, 'portfolio') #ratios of portfolio
	ratios_list_compare = calculate_ratios(df_portfolio, compare_symbol) #ratios of compare_symbol	
	print_result(ratios_list_portfolio, ratios_list_compare, compare_symbol, df_portfolio)

if __name__ == '__main__':
	print "Program name", sys.argv[0]
	portfolio_file = sys.argv[1]
	compare_symbol = sys.argv[2]
	analyze(portfolio_file, compare_symbol)