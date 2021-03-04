# Quantegy
#####...it's immaterial...
## Backtest Strategy
### Identify Arbitrage Opportunities
- Ingest backtest data for all currency across all exchanges
- Look for historical arbitrage opportunities among correlating exchanges 
- Generate Signals based on observations above
### Execute signal Based Trades
- Ingest backtest data for all currency across single exchange (Binance.us)
- Generate indicator sets
- Identify trend signals
- Execute trades based on trend signals 

## Soak Strategy
- Running every 60s
- Compile real-time data
- Execute trades on mock-book
- Run for continuing period of time

## TODO
- Move backrest data to s3
- CodePipeline create docker image deploy to EC@
- Front end website
- Migrate to time stream
- Grafana node and dash
- Consolidate calls to exchange
- Consolidate calls to time stream
- Fix update portfolio for trading
