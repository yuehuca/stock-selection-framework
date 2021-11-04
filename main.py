# -*- coding: utf-8 -*-
#stock selection

import dateformat
#import tushare as ts
import silence_tensorflow.auto
import downloaddata
import samples
import portfolioselection
import saveresults
import baostock as bs


token_tushare = '6e7cf8c1c16acbbf551404cbc8eb1dbec961846afdc3ff65b3d86cdf'

#ts.set_token(token_tushare)
#pro = ts.pro_api()

# 登陆baostock系统
lg = bs.login()
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

#ts_code = pro.stock_basic(exchange='', list_status='L', fields='ts_code')
bao_code = downloaddata.gettingtusharedata
#ts_code = bao_code.baostocklist() #baostock获取全市场列表时需启用此行
#ts_code = ts_code.values.tolist() #baostock获取全市场列表时需启用此行
ts_code = bao_code.baostock_hs300_list() #沪深300列表直接输出为list

#list_ts_code = []
#for item_ts_code in ts_code:
#    list_ts_code.append(item_ts_code[0])
#ts_code = list_ts_code

#ts_code = ts_code[0:10]

start_date_train = '2020-10-26' #当realtimedownload为1时train集合只是占位项
end_date_train = '2020-10-30'

start_date_test = '2021-10-11'
end_date_test = '2021-10-15'

start_date_forecast = '2021-10-18'
end_date_forecast = '2021-10-22'

start_date_portfolio = '2021-10-25'
end_date_portfolio = '2021-10-29'

#start_date_train_index = dateformat.dateformat(start_date_train)
#end_date_train_index = dateformat.dateformat(end_date_train)
#start_date_test_index = dateformat.dateformat(start_date_test)
#end_date_test_index = dateformat.dateformat(end_date_test)
#start_date_forecast_index = dateformat.dateformat(start_date_forecast)
#end_date_forecast_index = dateformat.dateformat(end_date_forecast)

start_date_train_index = start_date_train
end_date_train_index = end_date_train
start_date_test_index = start_date_test
end_date_test_index = end_date_test
start_date_forecast_index = start_date_forecast
end_date_forecast_index = end_date_forecast


#下载股票数据
downloaddata_main = downloaddata.gettingtusharedata(token_tushare, ts_code, 
                 start_date_train_index, end_date_train_index,
                 start_date_test_index, end_date_test_index, 
                 start_date_train, end_date_train, start_date_test, end_date_test, 
                 start_date_forecast_index, end_date_forecast_index, 
                 start_date_forecast, end_date_forecast, 
                 start_date_portfolio, end_date_portfolio)

downloaddata_main.tokensetup()

realtimedownload = 1
list_stockdata = downloaddata_main.collectdata(ts_code, start_date_train_index,
                 end_date_train_index, start_date_test_index, end_date_test_index, 
                 start_date_train, end_date_train, start_date_test, end_date_test, 
                 start_date_forecast_index, end_date_forecast_index, start_date_forecast, 
                 end_date_forecast, realtimedownload)

downloaddata_main.baostocklogout()


#构造样本
#止盈止损只能启用其中之一，若要同时启用需要重构代码，因为不确定最高价和最低价谁先出现
exitratio_high = 999 #训练集使用最高价和初始价，exitratio只影响测试集的回测, 999, 1.1
exitratio_low = -999 #-999, 0.95
np_samples = samples.buildingsamples(list_stockdata, exitratio_high, exitratio_low)

realtime = 1 #0为使用train, test和forecast集合训练模型，用于调试模型结构
             #1为实盘预测，使用test和forecast集合训练模型，预测未来股票组合
#当realtimedownload为1时realtime必须为1，当realtimedownload为0时realtime可为0或1
if realtimedownload == 1:
    realtime = 1
             
#当需要进行预测时开启该语句块
if realtime == 1:
    #一般情况下，先禁用该语句块进行模型结构调优，之后再启用该预测语句块
    np_samples_traintest = (np_samples[0].copy(), np_samples[1].copy(), np_samples[2].copy(), 
                            np_samples[3].copy(), np_samples[4].copy())
    np_samples = samples.forecastsamples(np_samples)
############################


#训练模型并构建投资组合
portfoliosize = 10
seed_value = range(100) #range(1)等同于(0, )
#注意！更换int型seed_value为range型时需要重启ide，反之亦然！是python内部随机数加载的问题。
#或者在使用range型后想要使用int型seed_value，可以写成数组形式如range(1)等同于(0, )
seed_value_shuffle = range(10) #固定混淆样本随机数
minseedsnumber = 500 #选取n个val_loss最小的结果，n应当小于等于seed_value的长度乘以seed_value_shuffle的长度，默认取一半
threshold_loss = 0.3 #选取val_loss的标准，一般失效loss是0.5左右，默认0.4
#当测试样本中的前portfoliosize个样本过于集中在输出的投资组合中时，说明纳入了过多失效模型，此时需要降低threshold_loss
#当minseedsnumber使用最大值seed_value*seed_value_shuffle，且threshold_loss使用大于等于1的值时，
#算法会将所有不全为同一个输出值的结果都记录
sizelimit = 1 #1为True，0为False
stockdropout = 0 #去除得分最高的几个股票，避免过拟合
results_portfolioselection = portfolioselection.portfolioselection(np_samples, list_stockdata, portfoliosize, 
                                                                   seed_value, minseedsnumber, sizelimit, 
                                                                   stockdropout, seed_value_shuffle, threshold_loss)

returns_test_exceed = results_portfolioselection[0]
list_selectedstocks = results_portfolioselection[1]
total_array_outputsignal = results_portfolioselection[2]
list_selectedstocks_outputsignal = results_portfolioselection[3]
list_droppedstocks = results_portfolioselection[4]
list_droppedstocks_outputsignal = results_portfolioselection[5]
validseednumber = results_portfolioselection[6]

#因为之前的测试集都没有单独列表保存有数据的股票的名称，所以在这里单独提取
list_stocknames = []
for i_list_stockdata in range(len(list_stockdata[0])):
    list_stocknames.append(list_stockdata[0][i_list_stockdata]['code'][0])

#使用测试集时需要把日期修正
if realtime == 0:
    start_date_portfolio = start_date_forecast
    end_date_portfolio = end_date_forecast
############################

#计算实盘投资组合的收益率
downloaddata_main.tokensetup()
realportfolio = downloaddata_main.getportfoliostockreturn(list_selectedstocks, 
                            start_date_portfolio, end_date_portfolio, exitratio_high, exitratio_low)
list_portfoliostockreturn = realportfolio[1]
list_portfolio_suspension = realportfolio[2]
return_realportfolio = portfolioselection.realportfolioreturn(list_selectedstocks_outputsignal, 
                                                                    list_portfoliostockreturn)
print('修正组合收益：')
print(return_realportfolio[0])

#检查被drop的股票的收益率
realportfolio_dropped = downloaddata_main.getportfoliostockreturn(list_droppedstocks, 
                            start_date_portfolio, end_date_portfolio, exitratio_high, exitratio_low)
list_portfoliostockreturn_dropped = realportfolio_dropped[1]
return_realportfolio_dropped = portfolioselection.realportfolioreturn(list_droppedstocks_outputsignal, 
                                                                    list_portfoliostockreturn_dropped)
print('被丢弃股票组合收益')
print(return_realportfolio_dropped)

downloaddata_main.baostocklogout()


#保存结果
a1 = list_selectedstocks
a2 = list_droppedstocks
a3 = list_selectedstocks_outputsignal
a4 = list_droppedstocks_outputsignal
a5 = list_portfoliostockreturn
a6 = list_portfoliostockreturn_dropped
a7 = return_realportfolio
a8 = return_realportfolio_dropped
a9 = list_portfolio_suspension
a10 = list_stocknames
a11 = total_array_outputsignal

finalresults = [a10, a11, a1, a3, a5, [a7], a2, a4, a6, [a8], a9]
list_finalresultsname = ['Sample Stocks', 'Frequency', 
                         'Selected Stocks', 'Frequency', 'Returns', 'Portfolio Returns', 
                         'Dropped Stocks', 'Frequency', 'Returns', 'Portfolio Returns', 
                         'Suspension Stocks']
settings = ['Seed Value: ' + str(max(seed_value)+1), 
            'Active Seeds: ' + str(minseedsnumber), 
            'Loss Threshold: ' + str(threshold_loss), 
            'Valid Seeds: ' + str(validseednumber), 
            'Shuffle Seed Value: ' + str(max(seed_value_shuffle)+1), 
            'Size Limit: ' + str(sizelimit), 
            'Stock Dropout: ' + str(stockdropout), 
            'First Day: ' + str(start_date_portfolio), 
            'Last Day: ' + str(end_date_portfolio), 
            'Exit Ratio High: ' + str(exitratio_high), 
            'Exit Ratio Low: ' + str(exitratio_low),
            'Real Time: ' + str(realtime)]

savepath = 'C:/downloads/stockselection/results/'
saveresults.saveresults(finalresults, list_finalresultsname, settings, savepath)


