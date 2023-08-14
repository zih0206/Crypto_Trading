'''
Author: Zih0206
'''
import pandas as pd
import time
from get_binance_data import Binance_data
from get_okx_data import Okx_data
from scipy.stats import wilcoxon, mannwhitneyu


'''
We consider Nonparametric Methods. 
Because there might have some missing values when we are getting data from the two exchanges, 
we consider two test medthods for the problems of whether the funding rates of the token are paired or not.
'''  
def statTest(sample1, sample2):
    # Convert string lists to float lists
    sample1 = [float(rate) for rate in sample1]
    sample2 = [float(rate) for rate in sample2]
    if len(sample1) == sample2:
        stat, p = wilcoxon(sample1, sample2, alternative= 'two-sided')
    else:
        stat, p = mannwhitneyu(sample1, sample2, alternative='two_sided')
    
    return p


if __name__ == '__main__':
  Bin = Binance_data()  #initial your objective
  Okx = Okx_data()
  Time1 = 1691366400000  # Sunday, August 6, 2023 8:00:00 PM
  Time2 = 1691366400000

  bin_exchange_info = Bin.get_exchange_info()['symbols']
  df = pd.DataFrame(bin_exchange_info)
  bin_coin_name = df['symbol']  
  #coin = bin_coin_name.tolist()
  okx_info = Okx.get_instrument_info('SWAP')['data']
  okx_coin_name = pd.DataFrame(okx_info)['uly'].apply(lambda x: x.replace('-',''))

# merge two dataframe to get a big data frame
  merge_df = pd.merge(left=bin_coin_name, right=okx_coin_name, left_on='symbol', right_on= 'uly',how= 'inner')
  merge_df = merge_df.rename(columns={'symbol':'Binance','uly':'Okx'})
  print(merge_df)

# Get Binance funding rates and calculate the mean values for various coins
  bin_means = []
  for item in merge_df.Binance:
      try:
          his_data = Bin.get_his_fundingRate(symbol=item, start_time=Time1, limit=100)
          rates = [entry['fundingRate'] for entry in his_data]
          mean_rate = pd.Series(rates).astype(float).mean()
          bin_means.append(mean_rate)
      except Exception as e:
          print(f"An error occurred with item {item}: {e}")
          bin_means.append(None)
      finally:
          time.sleep(5)
  
  merge_df['bin_FR_mean'] = bin_means

# Similarly, get funding rates in Okx and get mean values, and upload to our dataframe
Okx_merge_df = merge_df.Okx.apply(lambda x: x.replace('USDT','-USDT-SWAP')).tolist()
okx_means=[]
for i in Okx_merge_df:
  try:
    fd_his_data = Okx.get_his_fundingRate(instid=i,before=Time2,limit=100)
    rates_okx = [entry['fundingRate'] for entry in fd_his_data['data']]
    mean_rate_okx = pd.Series(rates_okx).astype(float).mean()
    okx_means.append(mean_rate_okx)
  except Exception as e:
    print(f"An error occurred with item {item}: {e}")
    okx_means.append(None)
  finally:
    time.sleep(5)
merge_df['okx_FR_mean'] = okx_means

# Calculate P-value
P_value=[]
for bin_symbol, okx_symbol in zip(merge_df.Binance, Okx_merge_df):
  try:
    his_data_ =Bin.get_his_fundingRate(symbol=bin_symbol, start_time=Time1, limit=100)
    rates_bin= [entry['fundingRate'] for entry in his_data_]
    
    fd_his_data = Okx.get_his_fundingRate(instid=okx_symbol, before= Time2, limit=100)
    rates_okx1 = [entry['fundingRate'] for entry in fd_his_data['data']]
  except Exception as e:
    print(f"An error occurred with item {item}: {e}")
  else:
    P_value.append(statTest(rates_bin, rates_okx1))
  finally:
    time.sleep(5)

# update p_value to merged data frame
merge_df['P_value'] = P_value
merge_df['P_value'] = merge_df['P_value'].round(4)

# update test result
merge_df['Test_result'] = 0
merge_df['Test_result'] = np.where(merge_df['P_value']>0.05,'FTR','Reject')
print(merge_df)
  
