import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import math
import sys
import numpy as np

def simulate(startdate, enddate, symbols, allocations):    
	ls_port_syms = symbols.split(',')
	lf_port_alloc = allocations.split(',')
	lf_port_alloc = map(float,lf_port_alloc)
	stdate = startdate.split(',')
	endate = enddate.split(',')
	dt_start = dt.datetime(int(stdate[0]),int(stdate[1]),int(stdate[2]))
	dt_end = dt.datetime(int(endate[0]),int(endate[1]),int(endate[2]))
	da_timeofday = dt.timedelta(hours=16)
	ldt_timestamps = du.getNYSEdays(dt_start,dt_end,da_timeofday)

	c_dataobj = da.DataAccess('Yahoo',cachestalltime=0)
	ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
	ldf_data = c_dataobj.get_data(ldt_timestamps, ls_port_syms, ls_keys)
	d_data = dict(zip(ls_keys, ldf_data))
	na_price = d_data['close'].values
	na_normalized_price = na_price / na_price[0,:]
	na_rets = na_normalized_price.copy()
	tsu.returnize0(na_rets)

	na_portrets = np.sum(na_rets * lf_port_alloc, axis=1)
	na_port_total = np.cumprod(na_portrets + 1)	
	average_daily_rest = np.mean(na_portrets)	
	k = math.sqrt(252)
	volatility = np.std(na_portrets)
	sharp_ratio = k * average_daily_rest / volatility	

	print "Start Date:", dt_start
	print "End Date:", dt_end
	print "Symboles:", ls_port_syms
	print "Optimal Allocations:", lf_port_alloc
	print "Sharp Ratio:", sharp_ratio
	print "Volatility:", volatility
	print "Average Daily Return:", average_daily_rest
	print "Cumulative Return:", na_port_total[-1]


#print sys.argv

if __name__ == '__main__':
	print "Program name", sys.argv[0]
	startdate = sys.argv[1]
	enddate = sys.argv[2]
	symbols = sys.argv[3]
	allocations = sys.argv[4]
	simulate(startdate,enddate,symbols,allocations)





	
