# -*- coding: utf-8 -*-
import numpy as np
import samples
import CNN_keras
import backtest

def portfolioselection(np_samples, list_stockdata, portfoliosize, seed_value):
    np_targets_classification = samples.classification(np_samples)
    
    array_samples_train = samples.inputtoarray(np_samples[0])
    array_samples_test = samples.inputtoarray(np_samples[1])
    
    array_targets_classification_train = samples.targettoarray_classification(np_targets_classification[0])
    array_targets_classification_test = samples.targettoarray_classification(np_targets_classification[1])
    
    array_targets_classification_onecol_train = samples.targettoarray_classification_onecol(np_targets_classification[0])
    array_targets_classification_onecol_test = samples.targettoarray_classification_onecol(np_targets_classification[1])
    
    array_target_train = samples.targettoarray(np_samples[2])
    array_targets_test = samples.targettoarray(np_samples[3])
    
    results_test_temp = CNN_keras.cnn_keras(array_samples_train, array_samples_test, 
                  array_targets_classification_train, array_targets_classification_test, 
                  array_targets_classification_onecol_train, array_targets_classification_onecol_test, 
                  array_target_train, array_targets_test, seed_value)
    
    results_test = results_test_temp[0]
    y_train = results_test_temp[1]
        
    if y_train.shape[1] == 1:
        array_outputsignal = backtest.scoretosignal(results_test, portfoliosize)
    else:
        difference_results_test = backtest.onehottoonecol(results_test)
        array_outputsignal = backtest.scoretosignal(difference_results_test, portfoliosize)
    
    
    array_stockweight = backtest.stockweight(array_outputsignal)
    
    returns_test_portfolio = backtest.backtest(np_samples[3], array_stockweight)
    
    returns_test_wholesample = np.mean(np_samples[3])
    
    returns_test_exceed = returns_test_portfolio - returns_test_wholesample
    
    list_selectedstocks = backtest.selectedstocks(array_outputsignal, list_stockdata[0])
    
    print('Portfolio Return: ' + str(returns_test_portfolio[0]))
    print('Whole Sample Return: ' + str(returns_test_wholesample))
    print('Exceed Return: ' + str(returns_test_exceed[0]))
    print(list_selectedstocks)
    
    return returns_test_exceed, list_selectedstocks
