#!/bin/bash
gcloud compute copy-files --zone us-central1-b ./btc-trader.py agsmith11@instance-2:/home/agsmith11/crypto-trader
gcloud compute copy-files --zone us-central1-b ./eth-trader.py agsmith11@instance-2:/home/agsmith11/crypto-trader
gcloud compute copy-files --zone us-central1-b ./ltc-trader.py agsmith11@instance-2:/home/agsmith11/crypto-trader
gcloud compute copy-files --zone us-central1-b ./start.sh agsmith11@instance-2:/home/agsmith11/crypto-trader
gcloud compute copy-files --zone us-central1-b ./stop.sh agsmith11@instance-2:/home/agsmith11/crypto-trader

