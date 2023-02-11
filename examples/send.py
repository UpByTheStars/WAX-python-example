import eospy
from eospy import cleos
from eospy import keys
import datetime as dt
import pytz
import requests
import os

global ADDRESS
global ACC_PK
global ce

ACC_PK='YOU_PRIVATE_KEY' #you wax/eos account private key
ADDRESS='YOUR_ADDRESS' #the name of the address for the private key



ce = eospy.cleos.Cleos(url='https://wax.greymass.com:443')
#ce = eospy.cleos.Cleos(url='https://eos.greymass.com:443') <== use if you intend to work with eos network



#make sure account exists before attempting transaction
def does_exist(account, network):
    arguments = {
        "account": "{}".format(account),
        "code":"eosio.token",
        "symbol":f"{network}",
    }

    # Get Balance of the account
    try:
        ce.get_currency_balance(arguments['account'], arguments['code'], arguments['symbol'])
        return True
    except:
        return False


#send
def send(sendto, value, memo, network):
    if network == 'WAX':
        while len((str(value).split('.'))[1]) < 8:
            value = str(value) + '0'
    elif network == 'EOS':
        while len((str(value).split('.'))[1]) < 4:
            value = str(value) + '0'
    payload = [
        {
            'args': {
                "from": ADDRESS,  # sender
                "to": sendto,  # receiver
                "quantity": f'{value} {network}',  # In WAX
                "memo": memo,
            },
            "account": "eosio.token",
            "name": "transfer",
            "authorization": [{
                "actor": ADDRESS,
                "permission": "active",
            }],
        }
    ]
    data=ce.abi_json_to_bin(payload[0]['account'],payload[0]['name'],payload[0]['args'])
    payload[0]['data']=data['binargs']

    payload[0].pop('args')

    trx = {"actions":[payload[0]]}


    trx['expiration'] = str((dt.datetime.utcnow() + dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))

    key = eospy.keys.EOSKey(ACC_PK)
    try:
        result = ce.push_transaction(trx, key, broadcast=True)
    except:
        return False, 'Something went wrong - too poor, cpu full, or invalid key are all possible problems'
    return True, result["transaction_id"]


SENDTO = 'upbythestars'
value = '0.1' #wax has 8 decimal minimum (0.00000001) and eos has 4 decimal minimum (0.0001)
memo = 'Hello, world!'
network = 'WAX' #network must be in all caps and either WAX or EOS depending on your prefered network
#network = 'EOS'
x = send(SENDTO, value, memo, network)
if x[0] == True:
    print(f'Transaction confirmed! TX: {x[1]}')
elif x[0] == False:
    print(f'Something went wrong! Response: {x[1]}')
