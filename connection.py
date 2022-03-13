#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 10:23:55 2022

@author: oscar
"""

from web3 import Web3
from web3.middleware import geth_poa_middleware

infura_url = 'https://rinkeby.infura.io/v3/3f2545d53b7e4daeb7889f92e1ef4a27'

web3 = Web3(Web3.HTTPProvider(infura_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

test_address = '0x5027323B073841Dfb6481F2a2AFf38c1f393B9fb'
print(f'Connected rinkeby: {web3.isConnected()}')

balance = web3.eth.getBalance(test_address)
print(f"Balance: {web3.fromWei(balance, 'ether')}")

lates_block = web3.eth.get_block('latest')
print('Lates block :')
print(lates_block)

