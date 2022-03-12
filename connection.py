#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 11:50:24 2022

@author: oscar
"""
#%% init
from web3 import Web3

ganache_url = 'http://127.0.0.1:7545'

web3 = Web3(Web3.HTTPProvider(ganache_url))
print(f'Connnected ganache: {web3.isConnected()}')
print(f'Block connected: {web3.eth.blockNumber}')

account_1 ='0xFEC3c1CdF3a743AF4FF914174d496edf9c9A24e4'
account_2 = '0x10D0AfC1Fb244e80CD1EdE2f6927fbfd0B386165'

private_key = '4bbc63b9faf174704494c5a1234eb86d0b757900d06abddb311167d9d4007956'

#%% get the nonce
nonce = web3.eth.getTransactionCount(account_1)

#%% build transaction
tx = {
      'nonce': nonce,
      'to': account_2,
      'value': web3.toWei(1, 'ether'),
      'gas': 2000000,
      'gasPrice': web3.toWei('50', 'gwei')
      }

#%% sign transaction
signed_tx = web3.eth.account.signTransaction(tx, private_key)

#%% send transaction
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

#%% get transaction hash
print(f'Transsaction hash: {web3.toHex(tx_hash)}')