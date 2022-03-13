from fastapi import FastAPI
import uvicorn
from starlette.templating import Jinja2Templates
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

app = FastAPI()
infura_url = 'https://rinkeby.infura.io/v3/3f2545d53b7e4daeb7889f92e1ef4a27'
SECRET_FILE = json.load(open("config.json", "r"))
SECRET_KEY = SECRET_FILE["SECRET_KEY"]

templates = Jinja2Templates(directory="templates")

@app.get('/connect/')
async def connect(test_address: str):
    web3 = Web3(Web3.HTTPProvider(infura_url))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    balance = web3.eth.getBalance(test_address)

    return f"Balance: {web3.fromWei(balance, 'ether')}"


@app.get("/send_tokens/")
async def send_tokens(wallet1: str, wallet2: str, send: int):

    web3 = Web3(Web3.HTTPProvider(infura_url))
    #web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    #%% get the nonce
    nonce = web3.eth.getTransactionCount(wallet1)
 
    #%% build transaction
    tx = {
    'nonce': nonce,
    'to': wallet2,
    'value': web3.toWei(send, 'ether'),
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei')
    }

    #%% sign transaction
    signed_tx = web3.eth.account.signTransaction(tx, SECRET_KEY)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    balance = web3.eth.getBalance(wallet1)

    d = {"balance": balance}

    return json.dumps(d)



if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)



