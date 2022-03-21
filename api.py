from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from starlette.requests import Request
import uvicorn
import pyodbc
import subprocess
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

app = FastAPI()
SECRET_FILE = json.load(open("config.json", "r"))
INFURA_URL = SECRET_FILE["INFURA_URL"]
SECRET_KEY = SECRET_FILE["SECRET_KEY"]
SERVER = SECRET_FILE["SERVER"]
DATABASE = SECRET_FILE["DATABASE"]
USERNAME = SECRET_FILE["USERNAME"]
PASSWORD = SECRET_FILE["PASSWORD"]
DRIVER = SECRET_FILE["DRIVER"]

def send_tk(fwallet1, fwallet2, send):

    web3 = Web3(Web3.HTTPProvider(INFURA_URL))
    #web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    nonce = web3.eth.getTransactionCount(fwallet1)

    tx = {
    'nonce': nonce,
    'to': fwallet2,
    'value': web3.toWei(send, 'ether'),
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei')
    }

    signed_tx = web3.eth.account.signTransaction(tx, SECRET_KEY)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    balance = web3.eth.getBalance(fwallet1)


    return balance

templates = Jinja2Templates(directory="templates")

@app.get('/connect/')
async def connect(test_address: str):
    web3 = Web3(Web3.HTTPProvider(INFURA_URL))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    balance = web3.eth.getBalance(test_address)

    return f"Balance: {web3.fromWei(balance, 'ether')}"


@app.get("/send_tokens/")
async def send_tokens(wallet1: str, wallet2: str, send: int):

    d = send_tk(fwallet1=wallet1, fwallet2=wallet2, send=send)

    p = {'balance' : d}

    return json.dumps(p)

@app.get('/get_data_esp/')
async def get_data_esp(humidity: float, temp: float, source: str, wallet1: str, wallet2: str, send: int):

    print(''.center(60, '='))
    print(f'humedad: {humidity} ,temperatura: {temp}, origen: {source}')

    # incert data in db
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        with conn.cursor() as cursor:
            count = cursor.execute(f"INSERT INTO esp8266.dbo.registro_h_t (HUMEDAD, TEMPERATURA, FECHA, ORIGEN) VALUES ({humidity}, {temp}, DEFAULT, {source});").rowcount
            conn.commit()
            print(f'Rows inserted: {str(count)}' )

    print(''.center(60, '='))

    if humidity >= 80:

        print(''.center(60, '='))
        print('TARGET!!!! OK!!!!')
        print(''.center(60, '='))

        d = send_tk(fwallet1=wallet1, fwallet2=wallet2, send=send)

        result = {'humidity': humidity,
                'temp': temp,
                'source': source,
                'rows incert': count,
                'balance' : d}

    else:

        result = {'humidity': humidity,
                'temp': temp,
                'source': source,
                'rows incert': count,
                'balance' : None}

    return result

@app.get('/dashboard/')
async def dashboard(request: Request):
    subprocess.call("/home/oriojas/esp8266_dht11_azure/dashboard.py", shell=True)
    return templates.TemplateResponse("new_plot.html", {"request": request})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)



