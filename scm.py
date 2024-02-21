import os
import sys
import bs4 as bs
from selenium import webdriver
import pandas as pd
import numpy as np
import time
import re
import json
from ast import literal_eval
from data import *

arg = sys.argv[1]

#selenium variables
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

def orderURL(item):
    nameid = item_nameids[item]
    url = ("https://steamcommunity.com/market/itemordershistogram?" +
            "country=US&language=english&currency=1&item_nameid=" +
            str(nameid) + "&two_factor=0")
    return url

def getPriceHistory(item):
    url = marketurls[item]
    driver.get(url)
    time.sleep(3)
    htmlSource = driver.page_source
    soup = bs.BeautifulSoup(htmlSource, "lxml")
    data = (literal_eval(soup.body.find_all("script")[4].string.splitlines()[25][13:-1]))
    data = np.transpose(np.array(data))
    df = {"date": data[0], "price": data[1], "quantity": data[2]}
    return pd.DataFrame(df)

def getBuySell(item):
    '''
    inputs string item, name of item as listed on the SCM
    returns dfs:
    df[0] == buy order df
    df[1] == sell order df
    '''
    url = orderURL(item)
    driver.get(url)
    time.sleep(3)
    htmlSource = driver.page_source
    soup = bs.BeautifulSoup(htmlSource, "lxml")
    data = json.loads(soup.text)

    buyOrders = data["buy_order_graph"]
    sellOrders = data["sell_order_graph"]
    buyPrices = []
    buyQuantities = []
    sellPrices = []
    sellQuantities = []
    for row in buyOrders:
        buyPrices.append(row[0])
        buyQuantities.append(row[1])
    for row in sellOrders:
        sellPrices.append(row[0])
        sellQuantities.append(row[1])

    for i in range(len(buyQuantities)-1, 0, -1):
        buyQuantities[i] -= buyQuantities[i-1]
    for i in range(len(sellQuantities)-1, 0, -1):
        sellQuantities[i] -= sellQuantities[i-1]
    dfs = [pd.DataFrame({"buyPrice": buyPrices, "buyQuantity": buyQuantities}),
           pd.DataFrame({"sellPrice": sellPrices, "sellQuantity": sellQuantities})]
    return dfs

def getOutputPath():
    cwd = os.getcwd()
    output = os.path.join(cwd,"Output")
    os.makedirs(output, exist_ok=True)
    return(output)

def getItemPath(path, group):
    output = os.path.join(path,group)
    os.makedirs(output, exist_ok=True)
    return(output)

def export2csv(arg):
    arg = str(arg)
    if arg in item_groups:
        group = item_groups[arg]
        path = getOutputPath()
        path = getItemPath(path, arg)
        for item in group:
            itempath = os.path.join(path,item)
            os.makedirs(itempath)
            buyselldfs = getBuySell(item)
            buyName = item+' Buy.csv'
            sellName = item+' Sell.csv'
            priceHistory = getPriceHistory(item)
            priceName = item+' Price.csv'
            priceHistory.to_csv(itempath+'/'+priceName, index=False)
            buyselldfs[0].to_csv(itempath+'/'+buyName, index=False)
            buyselldfs[1].to_csv(itempath+'/'+sellName, index=False)
    elif arg in item_nameids:
        path = getOutputPath()
        item = arg
        path = getItemPath(path, item)
        buyselldfs = getBuySell(item)
        buyName = item+' Buy.csv'
        sellName = item+' Sell.csv'
        priceHistory = getPriceHistory(item)
        priceName = item+' Price.csv'
        priceHistory.to_csv(path+'/'+priceName, index=False)
        buyselldfs[0].to_csv(path+'/'+buyName, index=False)
        buyselldfs[1].to_csv(path+'/'+sellName, index=False)
    else: return

export2csv(str(arg))