# Stock Assets Analyser

## Overview

This project contains a tool intented to get insights from your stock assets
portifolio. It uses historical data from the stock market and your portifolio
and presents graphical data for analysing and comparing both histories.

The first ideas, still under decision, are to allow the user to learn from past 
portifolio transactions, allowing one to analyse and help validate their stock
market moves and *modus operandi*. It should allow the user to simulate the 
outcome of different past decisions.

## Scope

The project will first aim to analyse data from the Brazilian B3 stock exchange.
Future implementations may add other markets accordingly.

## Current Implementation

Current implementation is developed in Python 3. It should use matplotlib for 
graphing and other data analysis libraries as necessary.

## Roadmap

Features currently or expected to be present on the project:
* Read raw data input file from stock exchange history - stage: TODO
* Parse raw data input file from stock exchange history - stage: TODO
* Cache parsed raw data input file from stock exchange history - stage: TODO
* Read user asset portifolio history - stage: TODO
* Present graphically market and portifolio data - stage: TODO
* Allow user to simulate other transactions for their timeling (say, what if I 
bought asset Y instead of asset X on this given day) - stage: TODO

## Data source

For stock exchange market history:
* [B3 stock exchange historical data](http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/cotacoes-historicas/)

For portifolio transactions history:
* currently: user's own curated history from personal portifolio control documents.
* future: integration with B3's website.