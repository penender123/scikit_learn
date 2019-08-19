import pandas as pd
import os
import time
from datetime import datetime

path = "/Users/huixia/Documents/ScikitLearn/intraQuarter"


def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path+'/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]     #x[0] is directory len=561, x[1] is folder name len = 561, x[2] is html file name, len = 561
    # print len(stock_list)
    # print stock_list
    df = pd.DataFrame(columns = ['Date','Unix','Ticker','DE Ratio'])
    sp500_df = pd.DataFrame.from_csv('ALPHAVANTAGE-INDEX.csv')


    for each_dir in stock_list[1:]:
        print "each_dir:"+ each_dir
        each_file = os.listdir(each_dir)
        # print(each_file)
        # time.sleep(15)
        # ticker = each_dir.split("\\")[1]
        ticker = each_dir.split('/Users/huixia/Documents/ScikitLearn/intraQuarter/_KeyStats/')[1]
        if len(each_file) > 0:
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                # print date_stamp,unix_time
                full_file_path = each_dir+'/'+file
                # print full_file_path
                source = open(full_file_path, 'r').read()  #normally this will be a urllib.urlopen if this is a url
                # print source

                try:
                    value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        # print sp500_date
                        # row = sp500_df[(sp500_df['Date'] == sp500_date)]
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        # row = sp500_df[sp500_df["Open"] <= 1200]

                        sp500_value = float(row["Adj Close"])
                    except:
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        # print "exceptttttt!!!1", row
                        sp500_value = float(row["Adj Close"])
                    # print "+++++++++++++++++"

                    stock_price =  float(source.split('</small><big><b>')[1].split('<b><big>')[0])
                    print 'stock price:', stock_price, "ticker:", ticker
                    df = df.append({'Date':date_stamp,'Unix':unix_time,'Ticker':ticker,'DE Ratio':value,},ignore_index = True)
                except Exception as e:
                    pass
                    # print full_file_path
                    # value = float('nan')
    save = gather.replace(' ', '').replace(')', '').replace('(', '').replace('/', '') + str('.csv')
    print save
    df.to_csv(save)
                # print(ticker+":",value)


            # time.sleep(15)

Key_Stats()
