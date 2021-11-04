# -*- coding: utf-8 -*-
#import tushare as ts
import numpy as np
from retry import retry
import time
import datetime
import baostock as bs
import pandas as pd


class gettingtusharedata(object):
    
    def __init__(self, token_tushare, ts_code, start_date_train_index, end_date_train_index,
                 start_date_test_index, end_date_test_index, start_date_train, 
                 end_date_train, start_date_test, end_date_test, start_date_forecast_index, 
                 end_date_forecast_index, start_date_forecast, end_date_forecast,
                 start_date_portfolio, end_date_portfolio):
        self.token_tushare = token_tushare
        self.ts_code = ts_code
        self.start_date_train_index = start_date_train_index
        self.end_date_train_index = end_date_train_index
        self.start_date_test_index = start_date_test_index
        self.end_date_test_index = end_date_test_index
        self.start_date_train = start_date_train
        self.end_date_train = end_date_train
        self.start_date_test = start_date_test
        self.end_date_test = end_date_test
        self.start_date_forecast_index = start_date_forecast_index
        self.end_date_forecast_index = end_date_forecast_index
        self.start_date_forecast = start_date_forecast
        self.end_date_forecast = end_date_forecast
        self.start_date_portfolio = start_date_portfolio
        self.end_date_portfolio = end_date_portfolio
        
#    def tokensetup(self):
#        ts.set_token(self.token_tushare)
#        self.pro = ts.pro_api()
        
    def tokensetup(self):
        # 登陆系统
        lg = bs.login()
        # 显示登陆返回信息
        print('login respond error_code:'+lg.error_code)
        print('login respond  error_msg:'+lg.error_msg)
        #bs.logout()
    
    def baostocklogout(self):
        bs.logout()

    def baostocklist():
        rs = bs.query_stock_basic(code="")
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        
        result = pd.DataFrame(data_list, columns=rs.fields)
        result_688 = result[result['code'].str.contains('sh.688')]
        index_result_688 = result_688.index
        result_no688 = result.drop(index_result_688)
        result_final =  result_no688[(result_no688['type']=='1') & (result_no688['status']=='1')]

        bao_code = result_final['code']
        
        return bao_code

    def baostock_hs300_list():
        # 获取沪深300成分股
        rs = bs.query_hs300_stocks()
        
        hs300_stocks = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            hs300_stocks.append(rs.get_row_data())
        result = pd.DataFrame(hs300_stocks, columns=rs.fields)
        baostock_hs300_code = result['code'].to_list()
        
        return baostock_hs300_code

#    def getindexdata(self, start_date, end_date):
#        self.df_index = ts.get_hist_data('sh', ktype='D', start=start_date, end=end_date) #从tushare老接口获取上证综指周线数据
#        return self.df_index

    def getindexdata(self, start_date, end_date):
        rs = bs.query_history_k_data_plus("sh.000001",
        "date,code,open,high,low,close",
        start_date=start_date, end_date=end_date,
        frequency="d", adjustflag="2")
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        
        self.df_index = pd.DataFrame(data_list, columns=rs.fields)
        self.df_index = self.df_index.sort_values(by='date', ascending=0)
        self.df_index.index = range(0,len(self.df_index))
        
        return self.df_index

#    def findtradingdate(self):
#        index_index_train = self.df_index.index_train #提取周信息
#        index_index_test = self.df_index_index_test
#        self.list_index_train = index_index_train.tolist()
#        self.list_index_test = index_index_test.tolist()
    
#    def cleandataformat(self):
#        #去除老接口上证综指日期中的'-'
#        self.list_index_train_1 = []
#        for item_list_index in self.list_index:
#            self.list_index_1.append(item_list_index.replace('-',''))
    
#    @retry()
#    def getstockdata(self, stockname, start_date, end_date):
#        #从tushare新接口提取日线数据
#        #self.df_stock = self.pro.daily(ts_code=stockname, start_date=start_date, end_date=end_date)
#        self.df_stock = ts.pro_bar(ts_code=stockname, adj='qfq', freq='D', start_date=start_date, end_date=end_date)
#        return self.df_stock

    #@retry()
    def getstockdata(self, stockname, start_date, end_date):
        rs = bs.query_history_k_data_plus(stockname,
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST,peTTM,pbMRQ",
        start_date=start_date, end_date=end_date,
        frequency="d", adjustflag="2")
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
            
        self.df_stock = pd.DataFrame(data_list, columns=rs.fields)
        self.df_stock = self.df_stock.sort_values(by='date', ascending=0)
        self.df_stock = self.df_stock[(self.df_stock['tradestatus']=='1')]
        self.df_stock = self.df_stock[(self.df_stock['isST']=='0')]
        self.df_stock = self.df_stock.drop(['adjustflag', 'tradestatus', 'isST'], axis = 1)
        self.df_stock.index = range(0,len(self.df_stock))
        
        if len(data_list) == 0:
            self.df_stock = pd.DataFrame()
        
        return self.df_stock
        
#    def switchindexdata(self):
#        #设置交易日期为索引
#        self.df_stock = self.df_stock.set_index(['trade_date'])
    
#    def matchdate(self):
#        #根据索引提取数据块
#        self.df_stock_validdate = self.df_stock.loc[self.list_index_1[0]:self.list_index_1[1]]
#        return self.df_stock_validdate
    
    def collectdata(self, ts_code, start_date_train_index, end_date_train_index,
                 start_date_test_index, end_date_test_index, start_date_train, 
                 end_date_train, start_date_test, end_date_test, start_date_forecast_index, 
                 end_date_forecast_index, start_date_forecast, end_date_forecast, realtimedownload):
        list_stockdata_train = []
        list_stockdata_test = []
        list_stockdata_forecast = []
        list_stockdata_drop = []
        df_index_test = self.getindexdata(start_date_test_index, end_date_test_index)
        if realtimedownload == 0:
            df_index_train = self.getindexdata(start_date_train_index, end_date_train_index)
        else:
            df_index_train = df_index_test
        df_index_forecast = self.getindexdata(start_date_forecast_index, end_date_forecast_index)
        

        time_tick_difference = 0
        list_time_tick_difference = [0, 0, 0, 0, 0]
        i_item_ts_code = 0
        for item_ts_code in ts_code:
            time_tick_start = time.time()
            list_time_tick_difference.append(time_tick_difference)
            mean_time_tick_difference = np.mean(list_time_tick_difference[-5 : len(list_time_tick_difference)])
            time_left = mean_time_tick_difference * (len(ts_code) - i_item_ts_code)
            i_item_ts_code = i_item_ts_code + 1
            print('...正在检索' + str(item_ts_code) + '，进度' + str(i_item_ts_code) + ' / ' + str(len(ts_code)) + 
                  '，预计耗时' + str(datetime.timedelta(seconds=time_left)))
            df_temp_stockdata_test = self.getstockdata(item_ts_code, start_date_test, end_date_test)
            if realtimedownload == 0:
                df_temp_stockdata_train = self.getstockdata(item_ts_code, start_date_train, end_date_train)
            else:
                df_temp_stockdata_train = df_temp_stockdata_test.copy()
            df_temp_stockdata_forecast = self.getstockdata(item_ts_code, start_date_forecast, end_date_forecast)
            if df_temp_stockdata_train is not None and df_temp_stockdata_test is not None and df_temp_stockdata_forecast is not None:
                if len(df_index_train) == len(df_index_test) == len(df_index_forecast):
                    if len(df_temp_stockdata_train) == len(df_index_train):
                        if len(df_temp_stockdata_test) == len(df_index_test):
                            if len(df_temp_stockdata_forecast) == len(df_index_forecast):
                                print('......' + str(item_ts_code) + '满足交易日长度条件，正在采集')
                                list_stockdata_train.append(df_temp_stockdata_train)
                                list_stockdata_test.append(df_temp_stockdata_test)
                                list_stockdata_forecast.append(df_temp_stockdata_forecast)
                            else:
                                print('......' + str(item_ts_code) + '不满足交易日长度条件')
                                list_stockdata_drop.append(item_ts_code)
                        else:
                            print('......' + str(item_ts_code) + '不满足交易日长度条件')
                            list_stockdata_drop.append(item_ts_code)
                    else:
                        print('......' + str(item_ts_code) + '不满足交易日长度条件')
                        list_stockdata_drop.append(item_ts_code)
                else:
                    print('......' + str(item_ts_code) + '不满足交易日长度条件')
                    list_stockdata_drop.append(item_ts_code)
            else:
                print('......' + str(item_ts_code) + '不满足交易日长度条件')
                list_stockdata_drop.append(item_ts_code)
                
            time_tick_end = time.time()
            time_tick_difference = time_tick_end - time_tick_start
            
        return list_stockdata_train, list_stockdata_test, list_stockdata_forecast, list_stockdata_drop


    def getportfoliostockreturn(self, ts_code, start_date_portfolio, end_date_portfolio, exitratio_high, exitratio_low):
        list_stockdata_portfolio = []
        list_portfoliostockreturn = []
        list_portfolio_suspension = []
        
        time_tick_difference = 0
        i_ts_code = 0
        for item_ts_code in ts_code:
            time_tick_start = time.time()
            time_left = time_tick_difference * (len(ts_code) - i_ts_code)
            print('...正在下载' + item_ts_code + '，预计耗时' + str(datetime.timedelta(seconds=time_left)))
            df_temp_stockdata_portfolio = self.getstockdata(item_ts_code, start_date_portfolio, end_date_portfolio)
            list_stockdata_portfolio.append(df_temp_stockdata_portfolio)
            if len(df_temp_stockdata_portfolio) == 0:
                list_portfoliostockreturn.append(0)
                list_portfolio_suspension.append(item_ts_code)
            else:
                if np.float(max(df_temp_stockdata_portfolio['high'][0 : -1])) >= (exitratio_high * np.float(df_temp_stockdata_portfolio[
                    'open'][len(df_temp_stockdata_portfolio['open']) - 1])):
                    list_portfoliostockreturn.append(exitratio_high - 1)
                elif np.float(min(df_temp_stockdata_portfolio['low'][0 : -1])) <= (exitratio_low * np.float(df_temp_stockdata_portfolio[
                    'open'][len(df_temp_stockdata_portfolio['open']) - 1])):
                    list_portfoliostockreturn.append(exitratio_low - 1)
                else:
                    list_portfoliostockreturn.append((np.float(df_temp_stockdata_portfolio['close'][0]) - 
                          np.float(df_temp_stockdata_portfolio['open'][len(df_temp_stockdata_portfolio['open']) - 1])) / 
                          np.float(df_temp_stockdata_portfolio['open'][len(df_temp_stockdata_portfolio['open']) - 1]))
                    
            i_ts_code = i_ts_code + 1
            
            time_tick_end = time.time()
            time_tick_difference = time_tick_end - time_tick_start
        
        return list_stockdata_portfolio, list_portfoliostockreturn, list_portfolio_suspension
    
  