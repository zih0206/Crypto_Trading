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
### significance level: 0.05 
* Null Hypothesis: Mu_Bin = Mu_Okx
* Altnernaltive Hypothesis: Mu_Bin not equal to Mu_Okx
* test result:

### According to our results: we are going to pick up the cryptocurrencies that have funding rate differences that may exist between the two exchanges. (Previous 24hrs)

|Binance| Okx|	bin_FR|	okx_FR|	abs_diff|
---|---|---|---|---|
LINKUSDT|	LINKUSDT|	0.0001|	-8.04E-05|	0.000180401
LRCUSDT	|LRCUSDT|	0.0001|	0.000272194|	0.000172194
ETHUSDT	|ETHUSDT|	0.0001|	8.30E-05|	1.70E-05
BNBUSDT	|BNBUSDT|	0|	8.92E-05|	8.92E-05

### The coin that has highest absolute difference is 





