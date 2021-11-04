# -*- coding: utf-8 -*-
import numpy as np
import samples
import CNN_keras
import backtest
import time
import datetime

def portfolioselection(np_samples, list_stockdata, portfoliosize, seed_value, minseedsnumber, sizelimit, stockdropout, 
                       seed_value_shuffle, threshold_loss):
    np_targets_classification = samples.classification(np_samples)
    
    array_samples_train = samples.inputtoarray(np_samples[0])
    array_samples_test = samples.inputtoarray(np_samples[1])
    
    array_targets_classification_train = samples.targettoarray_classification(np_targets_classification[0])
    array_targets_classification_test = samples.targettoarray_classification(np_targets_classification[1])
    
    array_targets_classification_onecol_train = samples.targettoarray_classification_onecol(np_targets_classification[0])
    array_targets_classification_onecol_test = samples.targettoarray_classification_onecol(np_targets_classification[1])
    
    array_target_train = samples.targettoarray(np_samples[2])
    array_targets_test = samples.targettoarray(np_samples[3])
    
    list_loss_train = []
    list_temp_array_outputsignal = []
    
    time_tick_difference = 0
    i_seed_value_shuffle = 1
    for item_seed_value_shuffle in seed_value_shuffle:
        
        i_seed_value = 1
        for item_seed_value in seed_value:
            time_tick_start = time.time()
            time_left = time_tick_difference * (len(seed_value) * len(seed_value_shuffle) - 
                                                (i_seed_value + i_seed_value_shuffle * len(seed_value) - len(seed_value)) + 1)
            print('...正在训练第' + str(i_seed_value_shuffle) + '个shuffle_seed，共' + str(len(seed_value_shuffle)) 
                  + '个，当前是第' + str(i_seed_value) + '个seed，共' + str(len(seed_value)) + '个，预计耗时' + 
                  str(datetime.timedelta(seconds=time_left)))
            results_test_temp = CNN_keras.cnn_keras(array_samples_train, array_samples_test, 
                          array_targets_classification_train, array_targets_classification_test, 
                          array_targets_classification_onecol_train, array_targets_classification_onecol_test, 
                          array_target_train, array_targets_test, item_seed_value, item_seed_value_shuffle)
            
            results_test = results_test_temp[0]
            y_train = results_test_temp[1]
            list_loss_train.append(results_test_temp[2])
                
            if y_train.shape[1] == 1:
                temp_array_outputsignal = backtest.scoretosignal(results_test, portfoliosize)
            else:
                difference_results_test = backtest.onehottoonecol(results_test)
                temp_array_outputsignal = backtest.scoretosignal(difference_results_test, portfoliosize)
            
            list_temp_array_outputsignal.append(temp_array_outputsignal)
            
            i_seed_value = i_seed_value + 1
            
            time_tick_end = time.time()
            time_tick_difference = time_tick_end - time_tick_start
            
        i_seed_value_shuffle = i_seed_value_shuffle + 1
     
    temp_list_loss_train = list_loss_train.copy()
    list_array_outputsignal = []
    validseednumber = 0
    for i_temp_list_loss_train in range(minseedsnumber):
        if min(temp_list_loss_train) <= threshold_loss:
            if sum(list_temp_array_outputsignal[np.argmin(temp_list_loss_train)]) > 0:
                list_array_outputsignal.append(list_temp_array_outputsignal[np.argmin(temp_list_loss_train)])
                temp_list_loss_train[np.argmin(temp_list_loss_train)] = max(temp_list_loss_train)
                validseednumber = validseednumber + 1
            else:
                temp_list_loss_train[np.argmin(temp_list_loss_train)] = max(temp_list_loss_train)
        else:
            temp_list_loss_train[np.argmin(temp_list_loss_train)] = max(temp_list_loss_train)
    
    total_array_outputsignal = sum(list_array_outputsignal)


    #去除得分最高的n只股票，缓解过拟合问题
    temp_total_array_outputsignal = total_array_outputsignal.copy()
    
    list_droppedstocks = []
    list_droppedstocks_outputsignal = []
    for i_temp_total_array_outputsignal in range(stockdropout):
        array_outputsignal_dropout = np.zeros((len(temp_total_array_outputsignal), 1))
        array_outputsignal_dropout[np.argmax(temp_total_array_outputsignal), 0] = 1
        list_droppedstocks.append(backtest.selectedstocks(array_outputsignal_dropout, list_stockdata[0])[0])
        list_droppedstocks_outputsignal.append(temp_total_array_outputsignal[np.argmax(
                                                        temp_total_array_outputsignal), 0])
        temp_total_array_outputsignal[np.argmax(temp_total_array_outputsignal), 0] = min(
                                                            temp_total_array_outputsignal)
    
    total_array_outputsignal = temp_total_array_outputsignal
    

    #限制股票数量，若不限制则直接使用temp_array_outputsignal作为最终输出
    if sizelimit == 1:
        temp_total_array_outputsignal = total_array_outputsignal.copy()
        
        array_outputsignal = np.zeros((len(temp_total_array_outputsignal), 1))
        
        list_selectedstocks = []
        list_selectedstocks_outputsignal = []
        for i_temp_total_array_outputsignal in range(portfoliosize):
            temp_array_outputsignal = np.zeros((len(temp_total_array_outputsignal), 1))
            temp_array_outputsignal[np.argmax(temp_total_array_outputsignal), 0] = 1
            array_outputsignal[np.argmax(temp_total_array_outputsignal), 0] = temp_total_array_outputsignal[
                                                                np.argmax(temp_total_array_outputsignal), 0]
            list_selectedstocks.append(backtest.selectedstocks(temp_array_outputsignal, list_stockdata[0])[0])
            list_selectedstocks_outputsignal.append(temp_total_array_outputsignal[np.argmax(
                                                            temp_total_array_outputsignal), 0])
            temp_total_array_outputsignal[np.argmax(temp_total_array_outputsignal), 0] = min(
                                                                temp_total_array_outputsignal)
        
        
    else:
        array_outputsignal = total_array_outputsignal
        list_selectedstocks_outputsignal = []
        
        i_array_outputsignal = 0
        for item_array_outputsignal in array_outputsignal:
            if item_array_outputsignal >= 1:
               list_selectedstocks_outputsignal.append(item_array_outputsignal)
                
            i_array_outputsignal = i_array_outputsignal + 1
        
        list_selectedstocks = backtest.selectedstocks(array_outputsignal, list_stockdata[0])

    array_stockweight = backtest.stockweight(array_outputsignal)
    
    returns_test_portfolio = backtest.backtest(np_samples[3], array_stockweight)
    
    returns_test_wholesample = np.mean(np_samples[3])
    
    returns_test_exceed = returns_test_portfolio - returns_test_wholesample
    
    
    print('组合收益：' + str(returns_test_portfolio[0]))
    print('全样本收益：' + str(returns_test_wholesample))
    print('超额收益：' + str(returns_test_exceed[0]))
    print('选中的股票：')
    print(list_selectedstocks)
    print('选中股票的出现次数：')
    print(list_selectedstocks_outputsignal)
    print('被丢弃的股票：')
    print(list_droppedstocks)
    print('被丢弃股票的出现次数：')
    print(list_droppedstocks_outputsignal)
    
    return returns_test_exceed, list_selectedstocks, total_array_outputsignal, list_selectedstocks_outputsignal, list_droppedstocks, list_droppedstocks_outputsignal, validseednumber


def realportfolioreturn(list_selectedstocks_outputsignal, list_portfoliostockreturn):
    array_selectedstocks_outputsignal = np.zeros((len(list_selectedstocks_outputsignal), 1))
    
    i_list_selectedstocks_outputsignal = 0
    for item_list_selectedstocks_outputsignal in list_selectedstocks_outputsignal:
        array_selectedstocks_outputsignal[i_list_selectedstocks_outputsignal, 0] = item_list_selectedstocks_outputsignal
        
        i_list_selectedstocks_outputsignal = i_list_selectedstocks_outputsignal + 1
        
    array_portfoliostockweight = backtest.stockweight(array_selectedstocks_outputsignal)
    return_realportfolio = backtest.backtest(list_portfoliostockreturn, array_portfoliostockweight)

    return return_realportfolio

