from hotbit.base_request.base_request import HotbitBaseRestApi
import numpy as np
from typing import List


class MarketData(HotbitBaseRestApi):
    def __init__(self, url: str = "https://api.hotbit.io", api_level: int = 2):
        super().__init__(key="", secret="", url=url, api_level=api_level)

    def get_kline(self, symbol: str, start_time: str, end_time: str, interval: str) -> List[list]:
        """
        :param symbol: symbol (Mandatory)
        :type: str
        :param kline_type: Type of candlestick patterns (Mandatory)
        :type: str
        :param kwargs: [Optional] startAt, endAt, currentPage, pageSize
        :return:
        [
          [
              "1545904980",             //Start time of the candle cycle
              "0.058",                  //opening price
              "0.049",                  //closing price
              "0.058",                  //highest price
              "0.049",                  //lowest price
              "0.018",                  //Transaction amount
              "0.000945"                //Transaction volume
          ],
          [
              "1545904920",
              "0.058",
              "0.072",
              "0.072",
              "0.058",
              "0.103",
              "0.006986"
          ]
        ]
        """
        self._set_permission_level(1)
        params = {
            "market": symbol,
            "start_time": np.uint64(start_time),
            "end_time": np.uint64(end_time),
            "interval": np.int32(interval),
        }

        return self._request(
            method="GET", uri="market.kline", params=params, timeout=500, auth=False
        )

    def get_last_kline(self, symbol: str, kline_interval: str) -> List[list]:
        """
        :param symbol: symbol (Mandatory)
        :type: str
        :param kline_interval: Type of candlestick patterns (Mandatory)
        :type: str
        :return:
        {
            'IsChange': False,
            'period': 300,
            'open': '0.06887348',
            'last': '0.06884198',
            'high': '0.06887446',
            'low': '0.06884198',
            'volume': '6.42',
            'deal': '0.4421284727',
            'close': '0.06884198',
            'base_volume': '6.42',
            'quote_volume': '0.4421284727'
        }
        """
        self._set_permission_level(1)
        interval_dict = {
            "24h": 86400,
            "1h": 3600,
            "5m": 300,
            "1m": 60,
        }
        if kline_interval not in interval_dict.keys():
            val_lst = list(interval_dict.keys())
            raise NotImplementedError(
                f"'{kline_interval}' kline interval not implemented. Try one of {val_lst}"
            )
        params = {"market": symbol, "period": np.int32(interval_dict[kline_interval])}

        return self._request(
            method="GET", uri="market.status", params=params, timeout=500, auth=False
        )

    def get_symbol_list(self) -> List[dict]:

        """
        :return:
        [
          {
              'name': 'QASHBTC',
              'stock': 'QASH',
              'money': 'BTC',
              'fee_prec': 4,
              'stock_prec': 2,
              'money_prec': 10,
              'min_amount': '0.100000'
            }
        ]
        """

        self._set_permission_level(1)
        return self._request(method="GET", uri="market.list", params={}, timeout=5, auth=False)

    def get_all_tickers(self) -> List[dict]:
        """
        :return:
        [
          {
              'buy': '0.00007237',
              'close': '0.00007303',
              'high': '0.00007612',
              'last': '0.00007303',
              'low': '0.00007166',
              'open': '0.00007476',
              'sell': '0.00007383',
              'symbol': 'OM_ETH',
              'vol': '491438.8',
              'base_volume': '491438.8',
              'quote_volume': '35.940036912'
          }
        ]
        """

        self._set_permission_level(1)
        return self._request(method="GET", uri="allticker", params={}, timeout=5, auth=False)

    def get_ticker(self, symbol: str) -> dict:
        """
        :param symbol: symbol (Mandatory)
        :type: str
        :return:
        {
              'buy': '0.00007237',
              'close': '0.00007303',
              'high': '0.00007612',
              'last': '0.00007303',
              'low': '0.00007166',
              'open': '0.00007476',
              'sell': '0.00007383',
              'symbol': 'OM_ETH',
              'vol': '491438.8',
              'base_volume': '491438.8',
              'quote_volume': '35.940036912'
          }
        """

        all_tickers = self.get_all_tickers()
        for symbol_ticker in all_tickers:
            if symbol_ticker["symbol"] == symbol:
                return symbol_ticker

        raise KeyError(f"Symbol {symbol} not found!")
