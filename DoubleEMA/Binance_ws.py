import json
from datetime import datetime

from base_websocket import BaseWebsocket



# Here we only subscribe the ticker data
class BinanceDataWebsocket(BaseWebsocket):
    def __init__(self, ping_interval=20, on_tick_callback=None):
        host = "wss://fstream.binance.com/stream?streams="
        super(BinanceDataWebsocket,self).__init__(host=host, ping_interval=ping_interval)
        self.on_tick_callback = on_tick_callback
        self.symbol = set()
        # self.symbol.add('btcusdt')


    def on_open(self):
        print(f"websocket open at:{datetime.now()}")

    def on_close(self):
        print(f"websocket close at:{datetime.now()}")

    def on_msg(self, message: str):
        msg = json.loads(message)
        # print(msg)

        stream = msg['stream']
        data = msg['data']

        symbol, channel = stream.split('@')

        if channel == 'ticker':
            ticker = {"volume": float(data['v']),
                      "open_price": float(data['o']),
                      "high_price": float(data['h']),
                      "low_price": float(data['l']),
                      "last_price": float(data['c']),
                      "datetime": datetime.fromtimestamp(float(data['E']) / 1000),
                      "symbol": symbol.upper()
                      }

            if self.on_tick_callback:
                self.on_tick_callback(ticker)

    def on_error(self, exception_type: type, exception_value: Exception, tb):
        print(f"websocket_Error，status：{exception_type}, info：{exception_value}")

    def subscribe(self, symbols):
        # for symbol in symbols:
        self.symbol.add(symbols)

        if self._active:
            self.stop()
            self.join()

        channel = []

        for symbol in self.symbol:
            channel.append(symbol.lower() + '@ticker')
            # channel.append(symbol.lower() + "@depth5")

        self.host = self.host + '/'.join(channel)

        print(self.host)
        self.start()


def test(data):
    print(data)

if __name__ == '__main__':
    ws = BinanceDataWebsocket(ping_interval=20, on_tick_callback=test)
    ws.subscribe('btcusdt')


