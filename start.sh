#!/bin/bash
source /home/agsmith11/crypto-trader/.gdax
python /home/agsmith11/crypto-trader/btc-trader.py&
python /home/agsmith11/crypto-trader/eth-trader.py&
python /home/agsmith11/crypto-trader/ltc-trader.py&
