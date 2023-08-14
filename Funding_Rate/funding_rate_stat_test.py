import pandas as pd
import time
from get_binance_data import Binance_data
from get_okx_data import Okx_data
from scipy.stats import wilcoxon, mannwhitneyu


if __name__ == '__main__':
  Bin = Binance_data()  #initial your objective
  Okx = Okx_data()
  Time1 = 1688515200000  # Tuesday, July 4, 2023 8:00:00 PM
  Time2 = 1688515200000

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
  
