# -*- coding: utf-8 -*-
import numpy as np

#将one-hot输出还原成单列输出
def onehottoonecol(results_test):
    difference_results_test = np.zeros((len(results_test), 1))
    temp_difference_results_test = results_test[:, 1] - results_test[:, 0]
    
    i_temp_difference_results_test = 0
    for item_temp_difference_results_test in temp_difference_results_test:
        difference_results_test[i_temp_difference_results_test, 0] = item_temp_difference_results_test
        
        i_temp_difference_results_test = i_temp_difference_results_test + 1
    
    return difference_results_test


#数值输出转化成分类，且只取最高的n个输出
def scoretosignal(results_test, portfoliosize):
    temp_results_test = results_test.copy()
    array_outputsignal = np.zeros((len(temp_results_test), 1))
    
    if np.std(temp_results_test) > 0:
        for i_results_test in range(portfoliosize):
            array_outputsignal[np.argmax(temp_results_test), 0] = 1
            temp_results_test[np.argmax(temp_results_test), 0] = min(temp_results_test)
    
    return array_outputsignal


def stockweight(array_outputsignal):
    array_stockweight = np.zeros(array_outputsignal.shape)
    
    i_array_scoretosignal = 0
    for item_array_scoretosignal in array_outputsignal:
        array_stockweight[i_array_scoretosignal, 0] = item_array_scoretosignal / sum(array_outputsignal)
        
        i_array_scoretosignal = i_array_scoretosignal + 1
    
    return array_stockweight


#returns_samples和results_test都要是n*1维的数组
#results_test是已经转化好的分类
def backtest(returns_test_stocks, array_stockweight):
    returns_test_stocks_weighted = []
    
    for i_returns_test_stocks in range(len(returns_test_stocks)):
        returns_test_stocks_weighted.append(returns_test_stocks[i_returns_test_stocks] * 
                                            array_stockweight[i_returns_test_stocks])
    
    returns_test_portfolio = sum(returns_test_stocks_weighted)
    
    return returns_test_portfolio


def selectedstocks(array_outputsignal, list_stockdata):
    list_selectedstocks = []
    
    i_array_outputsignal = 0
    for item_array_outputsignal in array_outputsignal:
        if item_array_outputsignal >= 1:
            #list_selectedstocks.append(list_stockdata[i_array_outputsignal]['ts_code'][0])
            list_selectedstocks.append(list_stockdata[i_array_outputsignal]['code'][0])
            
        i_array_outputsignal = i_array_outputsignal + 1
    
    return list_selectedstocks
        
    

    
