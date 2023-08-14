# Funding Rates Arbicharge Opportunity

## This project is related a cross exhcanges funding rates arbicharge strategy. 
## The exchanges: Binance, Okx

# What is Funding Rate?
## Funding rates are periodic payments either to traders that are long or short based on the difference between perpetual contract markets and spot prices. Therefore, depending on open positions, traders will either pay or receive funding. (source: Binance)

# Why is there an arbitrage opportunity between two exhcanges?
#### （Only consider the currencies that both exchanges have)
## Graphically:
![fund](https://github.com/zih0206/Crypto_Trading/assets/122567368/9beab9e2-3879-4777-8d7b-1c4a757a7381)
* Obviously: We can notice that the funding rates are different between Okx and Binance at 08/01/2023. 04:00:00

## Statistically: 
```python
def statTest(sample1, sample2):
    sample1 = [float(rate) for rate in sample1]
    sample2 = [float(rate) for rate in sample2]
    if len(sample1) == sample2:
        stat, p = wilcoxon(sample1, sample2, alternative= 'two-sided')
    else:
        stat, p = mannwhitneyu(sample1, sample2, alternative='two_sided')
    
    return p
```
### significance level: 0.05 
* Null Hypothesis: Mu_Bin = Mu_Okx
* Altnernaltive Hypothesis: Mu_Bin not equal to Mu_Okx
* test result: (P_values rounded to 4)
  |Binance| Okx|	bin_FR_Mean|	okx_FR_Mean| P_value|Test_result|
  ---|---|---|---|---|---|
  LINKUSDT|	LINKUSDT|	7.83E-05|	5.29E-05|	0.0015|	Reject
  LRCUSDT|	LRCUSDT|	8.02E-05|	5.88E-05|	0.2085|	FTR
  ETHUSDT|	ETHUSDT|	6.20E-05|	4.37E-05|	0.0009|	Reject
  BNBUSDT|	BNBUSDT|	-0.000137271|	-0.000191163|	0.7866|	FTR
  SOLUSDT|	SOLUSDT|	5.70E-05|	1.41E-05|	0.012|	Reject



### According to our results: we are going to pick up the cryptocurrencies with the result of Reject and obtain their funding rates.

|Binance| Okx| bin_FR_Mean|	okx_FR_Mean| P_value|Test_result|	bin_FR|	okx_FR|	abs_diff|
---|---|---|---|---|---|---|---|---|
LINKUSDT|   LINKUSDT|     0.000078|  5.294640e-05|   0.0015|      Reject|    0.000100| -0.000080|  1.804008e-04
ETHUSDT|    ETHUSDT|     0.000062|  4.367092e-05|   0.0009|      Reject|      0.000100|  0.000083|  1.697876e-05
SOLUSDT|    SOLUSDT|     0.000057|  1.412787e-05|   0.0120|      Reject|     0.000100|  0.000061|  3.900329e-05

### The coin with highest absolute difference is API3USDT.

|Binance|        API3USDT|
|---|---|
Okx|          API3USDT|
bin_FR_mean|   -0.000369
okx_FR_mean|   -0.000182
P_value     |     0.0356
Test_result  |    Reject
bin_FR  |      -0.024607
okx_FR   |     -0.015
abs_diff  |     0.03907

## Trading (API3USDT)
|Binance| Okx| bin_FR  | okx_FR   | abs_diff  |
---|---|---|---|---|
---|--- |-0.024607|-0.015|0.024235
--- |--- | Short| Short|---||

### We short this coin bewteen the two exchanges without leverage. (Commision fee: 0.09%. Commision fee might be different for different people)
* Profit (Daily): (0.024607 + 0.000372)*3 - 0.09% = 0.116431 ~ 11.6%
  





