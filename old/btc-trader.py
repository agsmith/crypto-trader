#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gdax
import json
import os
import time
import requests
from datetime import datetime
from websocket import WebSocketApp
from json import dumps, loads
from pprint import pprint
import slackweb
import logging

APIKEY=os.environ['APIKEY']
APISECRET=os.environ['APISECRET']
APIPASSPHRASE=os.environ['APIPASSPHRASE']

##
#  Tunables
##

BUY_PTG=0.04
SELL_PTG=0.10
DIP_PTG=0.10
ORDER_SIZE=100.00
# Use the sandbox API (requires a different set of API access credentials)
# APIURL="https://api-public.sandbox.gdax.com"
APIURL = "https://api.gdax.com"
FEEDURL = "wss://ws-feed.gdax.com"

transslack = slackweb.Slack(url="https://hooks.slack.com/services/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")
hpslack = slackweb.Slack(url="https://hooks.slack.com/services/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")
logging.basicConfig(filename='trader.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

public_client = gdax.PublicClient()
auth_client = gdax.AuthenticatedClient(APIKEY, APISECRET, APIPASSPHRASE,APIURL)

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


def on_open(socket):
    """Callback executed at socket opening."""
    socket.curr_price=0.00
    socket.high_price=0.00
    socket.last_trans_price=0.00
    params = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}]
    }
    socket.send(dumps(params))

def make_magic(curr_price, last_trans_price, high_price):
  if(last_trans_price==0.00):
    return curr_price;
  if(curr_price > (last_trans_price + (last_trans_price * SELL_PTG))):
    transslack.notify(text=":metal: Selling BTC at $" + str(curr_price))
    # sellbtc(curr_price)
    return curr_price;
  elif(curr_price < (high_price - (high_price * BUY_PTG))):
    transslack.notify(text=":btc: Buying BTC at $" + str(curr_price))
    # buybtc(curr_price)
    return curr_price;
  else:
    return last_trans_price;



def on_message(socket, msg):
    """Callback executed when a message comes."""
    j=json.loads(msg)
    if u'price' in j:
      socket.curr_price=float(j[u'price'])
      socket.last_trans_price = make_magic(socket.curr_price, socket.last_trans_price, socket.last_trans_price)
      if(float(j[u'price']) > socket.high_price):
        socket.high_price = float(j[u'price'])
        hpslack.notify(text=":btc: BTC $" + str(socket.high_price) + " buy at $" + str(socket.high_price - (socket.high_price*BUY_PTG)) + " sell at " + str((socket.last_trans_price + (socket.last_trans_price * SELL_PTG))))

def buybtc( current_price ):
  "buy USD worth of BTC"
  s = str(truncate(ORDER_SIZE/current_price, 3))
  buy = auth_client.buy(price=str(ORDER_SIZE), size=s,product_id='BTC-USD')
  return;

def sellbtc( current_price ):
  "sell 100USD worth of BTC"
  s = str(truncate(ORDER_SIZE/current_price, 3))
  sell = auth_client.sell(price=str(ORDER_SIZE), size=s, product_id='BTC-USD')
  # print json.dumps(sell, indent=4, sort_keys=True)
  return;

def go():
    """Main function."""
    hpslack.notify(text=":1up: btc-trader restarted")
    ws = WebSocketApp(FEEDURL, on_open=on_open, on_message=on_message)
    ws.run_forever()

go()
