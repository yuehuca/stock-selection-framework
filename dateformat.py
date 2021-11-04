# -*- coding: utf-8 -*-

def dateformat(stockdate):
    indexdate = stockdate[0:4] + '-' + stockdate[4:6] + '-' + stockdate[6:8]
        
    return indexdate