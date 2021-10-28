from hotbit.base_request.base_request import HotbitBaseRestApi
import json
from typing import List


class TradeData(HotbitBaseRestApi):
    def __init__(
        self, key: str, secret: str, url: str = "https://api.hotbit.io", api_level: int = 2
    ):
        super().__init__(key=key, secret=secret, url=url, api_level=api_level)
        self.api_key = key
        self.secret_key = secret

    def create_limit_order(self, symbol: str, side: str, size: float, price: float) -> dict:
        """
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param side: place direction buy or sell (Mandatory)
        :type: str
        :param size: amount of base currency to buy or sell (Mandatory)
        :type: float
        :param price: price per base currency (Mandatory)
        :type: float
        :return: {
            "error": null,
            "result":
            {
            "id":8688803,    #order-ID
                "market":"ETHBTC",
                "source":"web",    #The source identification of data request
                "type":1,	       #Type of order pladement 1-limit order
                "side":2,	       #Identification of buyers and sellers 1-Seller，2-buyer
                "user":15731,
                "ctime":1526971722.164765, #Time of order establishment(second)
                "mtime":1526971722.164765, #Time of order update(second)
                "price":"0.080003",
                "amount":"0.4",
                "taker_fee":"0.0025",
                "maker_fee":"0",
                "left":"0.4",
                "deal_stock":"0",
                "deal_money":"0",
                "deal_fee":"0",
                "status":0,
                "fee_stock":"HTB",	#Name of deductable token
                "alt_fee":"0.5",	#The discount of deductable tokens
                "deal_fee_alt":"0.123" #Amount deducted
                },
            "id": 1521169460
        }
        """
        assert side in ["buy", "sell"], "use side as 'buy' or 'sell' "
        params = {
            "api_key": self.api_key,
            "market": symbol,
            "side": 2 if side == "buy" else 1,
            "amount": size,
            "price": price,
            "isfee": 0,
        }

        self._set_permission_level(2)
        return self._request(
            method="POST", uri="order.put_limit", params=params, timeout=5, auth=True
        )

    def get_balances(self, symbols: List[str]) -> dict:
        """
        :param symbols: symbols (Mandatory)
        :type: list
        :return:
        {
            'USDT': {
                'available': '20.38121558',
                'freeze': '0'
                },
            'BTC': {
                'available': '0.00000000',
                'freeze': '0'
                }
        }
        """
        self._set_permission_level(2)
        default_return = {"available": "0.00000000", "freeze": "0"}
        params = {"api_key": self.api_key, "assets": json.dumps(symbols)}
        result = self._request(method="GET", uri="balance.query", params=params, auth=True)

        for symbol in symbols:
            result.setdefault(symbol, default_return)

        return result
