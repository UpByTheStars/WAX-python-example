import eospy
from eospy import cleos
from eospy import keys
import datetime as dt
import pytz
import requests
import os


ce = eospy.cleos.Cleos(url='https://wax.greymass.com:443')
#ce = eospy.cleos.Cleos(url='https://eos.greymass.com:443') <== use if you intend to work with eos network

def getbal(address, network):
    arguments = {
        "account": address,
        "code":"eosio.token",
        "symbol":network,
    }

    # Get Balance of the account
    get_bal=ce.get_currency_balance(arguments['account'], arguments['code'], arguments['symbol'])
    return float(get_bal[0].split(' ')[0])
  

print(getbal('upbythestars', 'WAX'))
