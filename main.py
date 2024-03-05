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
''' usdt and usdc contracts for eth
usdt_contract_address_eth = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
usdc_contract_address_eth = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
USDT_ABI_ETH = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_upgradedAddress","type":"address"}],"name":"deprecate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"deprecated","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_evilUser","type":"address"}],"name":"addBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"upgradedAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"maximumFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_maker","type":"address"}],"name":"getBlackListStatus","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowed","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newBasisPoints","type":"uint256"},{"name":"newMaxFee","type":"uint256"}],"name":"setParams","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"issue","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"redeem","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"basisPointsRate","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"isBlackListed","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_clearedUser","type":"address"}],"name":"removeBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"MAX_UINT","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_blackListedUser","type":"address"}],"name":"destroyBlackFunds","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_initialSupply","type":"uint256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Issue","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"newAddress","type":"address"}],"name":"Deprecate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"feeBasisPoints","type":"uint256"},{"indexed":false,"name":"maxFee","type":"uint256"}],"name":"Params","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_blackListedUser","type":"address"},{"indexed":false,"name":"_balance","type":"uint256"}],"name":"DestroyedBlackFunds","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"AddedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"RemovedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"}]'
USDC_ABI_ETH = '[{"constant":false,"inputs":[{"name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newImplementation","type":"address"},{"name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"implementation","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newAdmin","type":"address"}],"name":"changeAdmin","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"admin","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_implementation","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":false,"name":"previousAdmin","type":"address"},{"indexed":false,"name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"implementation","type":"address"}],"name":"Upgraded","type":"event"}]'
usdt_contract_eth = web3_eth.eth.contract(address=usdt_contract_address_eth, abi=USDT_ABI_ETH)
usdc_contract_eth = web3_eth.eth.contract(address=usdc_contract_address_eth, abi=USDT_ABI_ETH)
'''

# Подключение к Arbitrum One
web3_arb = Web3(Web3.HTTPProvider("https://rpc.ankr.com/arbitrum/d3f71af2055e23c48079e7a59f5b1e813c69f858627362364fcc61473ab3fff2"))
''' usdt and usdc contracts for arb
usdt_contract_address_arb = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"
usdc_contract_address_arb = ""
USDT_ABI_ARB = '[{"inputs":[{"internalType":"address","name":"_logic","type":"address"},{"internalType":"address","name":"admin_","type":"address"},{"internalType":"bytes","name":"_data","type":"bytes"}],"stateMutability":"payable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"beacon","type":"address"}],"name":"BeaconUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"admin_","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newAdmin","type":"address"}],"name":"changeAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"implementation_","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
usdt_contract_arb = web3_eth.eth.contract(address=usdt_contract_address_arb, abi=USDT_ABI_ARB)
'''

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

''' usdt balance eth
def get_usdt_balance_eth(address):
    try:
        balance_usdt = usdt_contract_eth.functions.balanceOf(address).call()
        decimals = usdt_contract_eth.functions.decimals().call()
        balance_usdt = balance_usdt / 10**decimals
        return balance_usdt
    except Exception as e:
        return f"Ошибка при получении баланса USDT: {e}"
'''

''' usdt balance arb
def get_usdt_balance_arb(address):
    try:
        balance_usdt = usdt_contract_arb.functions.balanceOf(address).call()
        decimals = usdt_contract_arb.functions.decimals().call()
        balance_usdt = balance_usdt / 10**decimals
        return balance_usdt
    except Exception as e:
        return f"Ошибка при получении баланса USDT: {e}"
'''

''' usdc balance eth
def get_usdc_balance_eth(address):
    try:
        balance_usdc = usdc_contract_eth.functions.balanceOf(address).call()
        decimals = usdc_contract_eth.functions.decimals().call()
        balance_usdc = balance_usdc / 10**decimals
        return balance_usdc
    except Exception as e:
        return f"Ошибка при получении баланса USDC: {e}"
'''

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
