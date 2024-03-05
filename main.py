input = open('wallets.txt', 'r')
#https://mainnet.infura.io/v3/0386874bdf174c94b8686678f9615f3f
import pandas as pd
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from web3 import Web3
import datetime
import pytz
import configparser

start_time = time.time()

config = configparser.ConfigParser()
config.read('config.ini')

ethereum_enabled = config.getboolean('Networks', 'ethereum', fallback=False)
linea_enabled = config.getboolean('Networks', 'linea', fallback=False)
optimism_enabled = config.getboolean('Networks', 'optimism', fallback=False)
arbitrum_enabled = config.getboolean('Networks', 'arbitrum', fallback=False)
zksync_enabled = config.getboolean('Networks', 'zksync', fallback=False)


addresses_file_path = '/Users/meshok/Documents/coding/GitHub/balance_checker/wallets.txt'

# Подключение к Ethereum mainnet
web3_eth = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/0386874bdf174c94b8686678f9615f3f'))

# Подключение к Arbitrum One
web3_arb = Web3(Web3.HTTPProvider("https://rpc.ankr.com/arbitrum/d3f71af2055e23c48079e7a59f5b1e813c69f858627362364fcc61473ab3fff2"))

# Подключение к Optimism
web3_op = Web3(Web3.HTTPProvider("https://rpc.ankr.com/optimism/d3f71af2055e23c48079e7a59f5b1e813c69f858627362364fcc61473ab3fff2"))

# Подключение к Linea
web3_linea = Web3(Web3.HTTPProvider("https://linea-mainnet.infura.io/v3/0386874bdf174c94b8686678f9615f3f"))

# Подключение к zkSync Era
web3_zksync = Web3(Web3.HTTPProvider("https://rpc.ankr.com/zksync_era/d3f71af2055e23c48079e7a59f5b1e813c69f858627362364fcc61473ab3fff2"))

def read_addresses_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            addresses = [line.strip() for line in file if line.strip()]  # Исключаем пустые строки
        return addresses
    except Exception as e:
        print(f"Ошибка при чтении адресов из файла: {e}")
        return []

def get_ethereum_balance_eth(address):
    try:
        balance_eth = web3_eth.from_wei(web3_eth.eth.get_balance(address), 'ether')
        return balance_eth
    except Exception as e:
        return f"Ошибка при получении баланса: {e}"
    
def get_ethereum_balance_arb(address):
    try:
        balance_eth = web3_arb.from_wei(web3_arb.eth.get_balance(address), 'ether')
        return balance_eth
    except Exception as e:
        return f"Ошибка при получении баланса: {e}"

def get_ethereum_balance_op(address):
    try:
        balance_eth = web3_op.from_wei(web3_op.eth.get_balance(address), 'ether')
        return balance_eth
    except Exception as e:
        return f"Ошибка при получении баланса: {e}"

def get_ethereum_balance_linea(address):
    try:
        balance_eth = web3_linea.from_wei(web3_linea.eth.get_balance(address), 'ether')
        return balance_eth
    except Exception as e:
        return f"Ошибка при получении баланса: {e}"
    
def get_ethereum_balance_zksync(address):
    try:
        balance_eth = web3_zksync.from_wei(web3_zksync.eth.get_balance(address), 'ether')
        return balance_eth
    except Exception as e:
        return f"Ошибка при получении баланса: {e}"

def process_address(address):
    eth_balance_eth = get_ethereum_balance_eth(address)    
    eth_balance_arb = get_ethereum_balance_arb(address)
    eth_balance_op = get_ethereum_balance_op(address)
    eth_balance_linea = get_ethereum_balance_linea(address)
    eth_balance_zksync = get_ethereum_balance_zksync(address)
    return {'Address': address, 
            'ETH': eth_balance_eth, 'ETH_arb': eth_balance_arb, 
            'ETH_linea': eth_balance_linea, 'ETH_op': eth_balance_op,
            'ETH_zksync': eth_balance_zksync}

async def async_process_addresses(addresses):
    with ThreadPoolExecutor(max_workers=5) as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(executor, process_address, address) for address in addresses]
        return await asyncio.gather(*tasks)

async def main():
    addresses = read_addresses_from_file(addresses_file_path)
    results = await async_process_addresses(addresses)

    df = pd.DataFrame(results)

    excel_filename = 'ethereum_balances.xlsx'
    df.to_excel(excel_filename, index=False)
    print(f"Балансы сохранены в файл {excel_filename}")

if __name__ == "__main__":
    asyncio.run(main())


#Получение времени выполнения программы + запись в логи
with open('work_time_logs.txt', 'a') as work_time_logs:
    execution_time = time.time() - start_time
    current_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    work_time_logs.write(str(current_time) + '\n')
    work_time_logs.write(f"Время выполнения программы: {round(execution_time)} секунд\n")
    print(f"Время выполнения программы: {round(execution_time)} секунд\n")
    work_time_logs.write('\n')
