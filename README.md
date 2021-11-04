# stock-selection-framework
This is a stock selection framework based on Convolutional Neural Network. You can get a list of stocks that may perform better than others by seting up your desired date periods. All processes can be done automatically.
The data source could be either [Tushare](https://tushare.pro/) or [baostock](http://baostock.com/). The current version is based on baostock.

1. Go to the [main.py](https://github.com/yuehuca/stock-selection-framework/blob/main/main.py) and edit the dates:

**Notice: in the default 'realtimedownload' mode, 'start_date_train' and 'end_date_train' are disabled. You should always set the framework under 'realtimedownload' mode unless you are going to change the CNN structure and want to see the validation results.

start_date_test = 'The start date of training set.' 

end_date_test = 'The end date of training set.' 

start_date_forecast = 'The start date of testing set.' 

end_date_forecast = 'The end date of testing set.' 

start_date_portfolio = 'The start date of forecasting set.' #could be dates in the real future 

end_date_portfolio = 'The end date of forecasting set' #could be dates in the real future 

**Notice: All the 3 date periods should have the same length. Please take holidays into consideration.
**Notice: The default version only collects data from the CSI300 Index stocks. Enable 'ts_code = bao_code.baostocklist()' and disable 'ts_code = bao_code.baostock_hs300_list()' to get a larger stock pool.

2. Run through the code. The downloading process may take about 5 minutes (for CSI300 Index stocks) and the training process may take about 45 minutes (for CSI300 Index stocks). The final CSV file contains a list of stocks that may have better performance in the next period (portfolio period). You may change the program settings according to your testing results.
'exitratio_high': High exit ratio.
'exitratio_low': Low exit ratio.
'seed_value':  Train the model on different initial random seeds.
'seed_value_shuffle': Shuffle the data on different random seeds.
'minseedsnumber': Output 'n' portfolios that have the smallest validation loss, and 'n' should smaller than 'seed_value' * 'seed_value_shuffle'.
'threshold_loss': Only pick portfolios that have validation loss smaller than the threshold. Default is 0.3. When you are using a large threshold, there will be a lot of fail models and the stock list will contain many fake results.
'sizelimit': Limit the size of stock list. '1' or '0'.
'stockdropout': Remove several stocks that have the highest ranking from the list. Enable this when the stocks are very concentrated.

3. The core model is a Convolutional Neural Network based on Keras. You can edit the model structure in [CNN_keras.py](https://github.com/yuehuca/stock-selection-framework/blob/main/CNN_keras.py).

4. This framework is intented to build a stock selection framework for studying and research. The author do not responsible for any outcomes brought by this framework.
