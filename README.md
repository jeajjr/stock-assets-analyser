# Stock Assets Analyser

## Overview

This project contains a tool intented to get insights from your stock assets
portifolio. It uses historical data from both the stock market and your portifolio
transactions and presents graphical data for analysing and comparing both histories.

The first ideas, still under elaboration, are to allow the user to learn from past 
portifolio transactions, allowing one to analyse and help validate their stock
market moves and *modus operandi*. It should allow the user to simulate the 
outcome of different past decisions.

## Scope

The project will first aim to analyse data from the Brazilian B3 stock exchange.
Future implementations may add other markets accordingly.

## Current Implementation

Current implementation is developed in Python 3. It should use matplotlib for 
graphing and other data analysis libraries as necessary.

The project incudes a stockutils module for:
* reading raw market data
* reading user transaction history data

A Jupyter notebook is used to execute the module and practicing with the data.

## Roadmap

Features currently or expected to be present on the project:
* Read raw data input file from stock exchange history - stage: done
* Parse raw data input file from stock exchange history - stage: done
* Cache parsed raw data input file from stock exchange history - stage: TODO
* Read user asset portifolio history - stage: done
* Present graphically market and portifolio data - stage: in progress
* Allow user to simulate other transactions for their timeling (say, what if I 
bought asset Y instead of asset X on this given day) - stage: TODO

## Data sources

There are three main sources of data for the project, all described below.

For stock exchange market history:
* [B3 stock exchange historical data](http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/cotacoes-historicas/)

For IBOV historical data
* [InfoMoney](https://www.infomoney.com.br/cotacoes/ibovespa/historico/)

For portifolio transactions history:
* currently: user's own curated history from personal portifolio control documents.
* future: integration with B3's website.

## Input data format

### B3 stock exchange market history

Historical data for the market should be in the format as described on B3's website
cite above.

### IBOV historical data

Ibovespa index historical data files should have a header and one day data per 
line, as the example below:

```
"DATA","ABERTURA","FECHAMENTO","VARIAÇÃO","MÍNIMO","MÁXIMO","VOLUME"
"30/12/2019","116.530","115.645","-0,76","115.599","117.086","15,39B"
```

### User transactions history

User transactions should be in the following format, one transaction per line:
```
TICKER DATE BUY_QTTY SELL_QTTY BUY_PRICE SELL_PRICE
```

Where DATE is in the *YYYY-MM-DD* format and prices should have a leading dollar
sign ($) and use dot (.) for decimal representation. Below is an entry example:

```
ABEV3	2019-04-10	35	0	$17.45	$0.00
```

This format only follows the data previously by the user before this project, and
may change in the future for optimization.

### Input data files

The table below shows information about the files of each data type.

| **data** | **folder** | **test file name preffix** | **production file name preffix** |
|--|--|--|--|
| stock market history | raw-input | tCOTA* | COTA* |
| IBOV historical data | raw-input | IBOV* | IBOV* |
|user transactions history | user-input | t* | exp* |
