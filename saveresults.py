# -*- coding: utf-8 -*-
import pandas as pd
import time

def saveresults(finalresults, list_finalresultsname, settings, savepath):
    df_finalresults = pd.DataFrame()
    
    i_finalresults = 0
    for item_finalresults in finalresults :
        df_finalresults = pd.concat([df_finalresults, pd.DataFrame(item_finalresults, 
                          columns=[list_finalresultsname[i_finalresults]])], axis=1)
        
        i_finalresults = i_finalresults + 1
        
    df_settings = pd.DataFrame(settings, columns=['Settings'])
    df_finalresults = pd.concat([df_finalresults, df_settings], axis=1)
    
    savefilename = time.strftime("%Y%m%d%H%M%S", time.localtime())
    df_finalresults.to_csv(savepath + str(savefilename) + '.csv')
    
    