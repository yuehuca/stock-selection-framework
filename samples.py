# -*- coding: utf-8 -*-
import numpy as np

def buildingsamples(list_stockdata, exitratio_high, exitratio_low):
    list_df_stockdata_train = list_stockdata[0].copy()
    list_df_stockdata_test = list_stockdata[1].copy()
    list_df_stockdata_forecast = list_stockdata[2].copy()
    
    list_stockdata_train = []
    list_stockdata_test = []
    list_stockdata_forecast = []
    
    for item_list_df_stockdata_train in list_df_stockdata_train:
        np_item_list_df_stockdata_train = (item_list_df_stockdata_train.to_numpy())[:,2:item_list_df_stockdata_train.shape[1]]
        temp_item_list_df_stockdata_train = np.zeros(np_item_list_df_stockdata_train.shape)
        for i_temp_item_list_df_stockdata_train in range(np_item_list_df_stockdata_train.shape[0]):
            for j_temp_item_list_df_stockdata_train in range(np_item_list_df_stockdata_train.shape[1]):
                temp_item_list_df_stockdata_train[
                i_temp_item_list_df_stockdata_train, j_temp_item_list_df_stockdata_train] = np.float(np_item_list_df_stockdata_train[
                    i_temp_item_list_df_stockdata_train, j_temp_item_list_df_stockdata_train])
        list_stockdata_train.append(temp_item_list_df_stockdata_train)
    for item_list_df_stockdata_test in list_df_stockdata_test:
        np_item_list_df_stockdata_test = (item_list_df_stockdata_test.to_numpy())[:,2:item_list_df_stockdata_test.shape[1]]
        temp_item_list_df_stockdata_test = np.zeros(np_item_list_df_stockdata_test.shape)
        for i_temp_item_list_df_stockdata_test in range(np_item_list_df_stockdata_test.shape[0]):
            for j_temp_item_list_df_stockdata_test in range(np_item_list_df_stockdata_test.shape[1]):
                temp_item_list_df_stockdata_test[
                i_temp_item_list_df_stockdata_test, j_temp_item_list_df_stockdata_test] = np.float(np_item_list_df_stockdata_test[
                    i_temp_item_list_df_stockdata_test, j_temp_item_list_df_stockdata_test])
        list_stockdata_test.append(temp_item_list_df_stockdata_test)
    for item_list_df_stockdata_forecast in list_df_stockdata_forecast:
        np_item_list_df_stockdata_forecast = (item_list_df_stockdata_forecast.to_numpy())[:,2:item_list_df_stockdata_forecast.shape[1]]
        temp_item_list_df_stockdata_forecast = np.zeros(np_item_list_df_stockdata_forecast.shape)
        for i_temp_item_list_df_stockdata_forecast in range(np_item_list_df_stockdata_forecast.shape[0]):
            for j_temp_item_list_df_stockdata_forecast in range(np_item_list_df_stockdata_forecast.shape[1]):
                temp_item_list_df_stockdata_forecast[
                i_temp_item_list_df_stockdata_forecast, j_temp_item_list_df_stockdata_forecast] = np.float(np_item_list_df_stockdata_forecast[
                    i_temp_item_list_df_stockdata_forecast, j_temp_item_list_df_stockdata_forecast])
        list_stockdata_forecast.append(temp_item_list_df_stockdata_forecast)
        
    list_target_train = [] #train集合的target使用test集合的价格得到
    list_target_test = [] #test集合的target使用forecast集合的价格得到
       
    for item_list_stockdata_test in list_stockdata_test:
        list_target_train.append((max(item_list_stockdata_test[0 : -1, 1]) - 
        item_list_stockdata_test[(item_list_stockdata_test.shape[0] - 1), 0]) / 
        item_list_stockdata_test[(item_list_stockdata_test.shape[0] - 1), 0])
    for item_list_stockdata_forecast in list_stockdata_forecast:
        if max(item_list_stockdata_forecast[0 : -1, 1]) >= (exitratio_high * item_list_stockdata_forecast[(
               item_list_stockdata_forecast.shape[0] - 1), 0]):
            list_target_test.append(exitratio_high - 1)
        elif min(item_list_stockdata_forecast[0 : -1, 2]) <= (exitratio_low * item_list_stockdata_forecast[(
               item_list_stockdata_forecast.shape[0] - 1), 0]):
            list_target_test.append(exitratio_low - 1)
        else:
            list_target_test.append((item_list_stockdata_forecast[0, 3] - 
            item_list_stockdata_forecast[(item_list_stockdata_forecast.shape[0] - 1), 0]) / 
            item_list_stockdata_forecast[(item_list_stockdata_forecast.shape[0] - 1), 0])
        
    return list_stockdata_train, list_stockdata_test, list_target_train, list_target_test, list_stockdata_forecast


def classification(np_samples):
    list_target_train = np_samples[2]
    list_target_test = np_samples[3]
    
    list_target_train_classification = []
    list_target_test_classification = []
    
    for item_list_target_train in list_target_train:
        if item_list_target_train >= np.median(list_target_train):
            list_target_train_classification.append(1)
        else:
            list_target_train_classification.append(0)
    for item_list_target_test in list_target_test:
        if item_list_target_test >= np.median(list_target_test):
            list_target_test_classification.append(1)
        else:
            list_target_test_classification.append(0)
    
    return list_target_train_classification, list_target_test_classification


#把样本集转换成(n, p, q, 1)的数组，n个样本，每个样本p行，q列（在python中其实是每一个p中有几个q），每行每列1个元素
def inputtoarray(list_stockdata):
    
    array_stockdata = np.ones((len(list_stockdata), max(list_stockdata[0].shape), 
                                    max(list_stockdata[0].shape), 1))*(-999)

    i_list_stockdata = 0
    for item_list_stockdata in list_stockdata:
        temp_item_list_stockdata = item_list_stockdata.reshape(item_list_stockdata.shape[0] * 
                                         item_list_stockdata.shape[1], 1)
        
        for row_item_list_stockdata in range(item_list_stockdata.shape[0]):
            for col_item_list_stockdata in range(item_list_stockdata.shape[1]):
                array_stockdata[i_list_stockdata, row_item_list_stockdata, 
                col_item_list_stockdata, 0] = item_list_stockdata[
                row_item_list_stockdata, col_item_list_stockdata]
        
        i_temp_item_list_stockdata = 0
        for row_array_stockdata in range(array_stockdata[0, 0].shape[0]):
            for col_array_stockdata in range(array_stockdata[0, 0].shape[0]):
                if array_stockdata[i_list_stockdata, row_array_stockdata, 
                    col_array_stockdata, 0] == -999:
                    array_stockdata[i_list_stockdata, row_array_stockdata, 
                    col_array_stockdata, 0] = temp_item_list_stockdata[i_temp_item_list_stockdata]
                    i_temp_item_list_stockdata = i_temp_item_list_stockdata + 1
                    if i_temp_item_list_stockdata >= len(temp_item_list_stockdata):
                        i_temp_item_list_stockdata = 0
        
        i_list_stockdata = i_list_stockdata + 1
        
    return array_stockdata
    
    
def targettoarray_classification(np_targets):
    array_targets_classification = np.ones((len(np_targets), 2))
    
    i_np_targets = 0
    for item_np_targets in np_targets:
        if item_np_targets == 0:
            array_targets_classification[i_np_targets, 0] = 1
            array_targets_classification[i_np_targets, 1] = 0
        else:
            array_targets_classification[i_np_targets, 0] = 0
            array_targets_classification[i_np_targets, 1] = 1
            
        i_np_targets = i_np_targets + 1
    
    return array_targets_classification


def targettoarray_classification_onecol(np_targets_classification):
    array_targets_classification_onecol = np.ones((len(np_targets_classification), 1))
    
    i_np_targets_classification = 0
    for item_np_targets_classification in np_targets_classification:
        array_targets_classification_onecol[i_np_targets_classification, 0] = item_np_targets_classification
        
        i_np_targets_classification = i_np_targets_classification + 1
    
    return array_targets_classification_onecol


def targettoarray(np_targets):
    array_targets = np.ones((len(np_targets), 1))
    
    i_np_targets = 0
    for item_np_targets in np_targets:
        array_targets[i_np_targets, 0] = item_np_targets
        
        i_np_targets = i_np_targets + 1
    
    return array_targets


def forecastsamples(np_samples):
    list_stockdata_train_forecast = np_samples[1]
    list_stockdata_test_forecast = np_samples[4]
    list_target_train_forecast = np_samples[3]
    list_target_test_forecast = []
    
    for item_list_target_train_forecast in list_target_train_forecast:
        list_target_test_forecast.append(np.ones(np.shape(item_list_target_train_forecast)))
    
    return list_stockdata_train_forecast, list_stockdata_test_forecast, list_target_train_forecast, list_target_test_forecast





