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

APIKEY=os.environ['APIKEY']
APISECRET=os.environ['APISECRET']
APIPASSPHRASE=os.environ['APIPASSPHRASE']
WEBHOOK_URL=os.environ['SLACKURL']

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

public_client = gdax.PublicClient()
auth_client = gdax.AuthenticatedClient(APIKEY, APISECRET, APIPASSPHRASE,APIURL)

def on_open(socket):
    """Callback executed at socket opening."""
    socket.curr_price=0.00
    socket.high_price=0.00
    params = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}]
    }
    socket.send(dumps(params))

def on_message(socket, msg):
    """Callback executed when a message comes."""
    j=json.loads(msg)
    socket.curr_price=float(j[u'price'])
    if(float(j[u'price']) > socket.high_price):
      socket.high_price = float(j[u'price'])
      print ("New high: ", socket.high_price)
    elif (socket.high_price > (socket.curr_price + (socket.high_price * BUY_PTG))):
      print ("Buying at $", socket.curr_price)
      buybtc(socket.curr_price)
      socket.high_price = socket.curr_price

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def buybtc( current_price ):
  "buy USD worth of BTC"
  postToSlack("bought", str(current_price))
  s = str(truncate(ORDER_SIZE/current_price, 3))
  buy = auth_client.buy(price=str(ORDER_SIZE), size=s,product_id='BTC-USD')
  return;

def sellbtc( current_price ):
  "sell 100USD worth of BTC"
  postToSlack("sold", str(current_price))
  s = str(truncate(ORDER_SIZE/current_price, 3))
  sell = auth_client.sell(price=str(ORDER_SIZE), size=s, product_id='BTC-USD')
  print json.dumps(sell, indent=4, sort_keys=True)
  return;

def postToSlack( action, price ):
  "post transaction to slack"
  slack_data = {'text': "Just " + action + " at $" + price +" :moneybag:"}

  response = requests.post(
    WEBHOOK_URL, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
  )
  if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )
  return;

def go():
    """Main function."""
    ws = WebSocketApp(FEEDURL, on_open=on_open, on_message=on_message)
    ws.run_forever()

go()

