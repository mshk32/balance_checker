import pandas as pd
import time
import asyncio
from web3 import Web3
import datetime
import pytz
import configparser
import aiohttp

start_time = time.time()

config = configparser.ConfigParser()
config.read('config.ini')
# словарь для хранения значений сетей
network_to_process = {key: config.getboolean('Networks', key) for key in config['Networks']}
# Проверка на отсутствие включенных сетей
if not(any(network_to_process.values())):
    raise ValueError("Не выбрана ни одна сеть в конфигурационном файле. Выберите хотя бы одну сеть.")

addresses_file_path = config.get('addresses', 'file_path', fallback='no wallets file found')

# Подключение ко всем выбранным сетям
def connect_to_network(network_name, provider_url):
    if network_to_process.get(network_name):
        return Web3(Web3.HTTPProvider(provider_url))
    return None
web3_eth = connect_to_network('ethereum', config.get('RPCs', 'ethereum'))
web3_arb = connect_to_network('arbitrum', config.get('RPCs', 'arbitrum'))
web3_op = connect_to_network('optimism', config.get('RPCs', 'optimism'))
web3_linea = connect_to_network('linea', config.get('RPCs', 'linea'))
web3_zksync = connect_to_network('zksync', config.get('RPCs', 'zksync'))
web3_scroll = connect_to_network('scroll', config.get('RPCs', 'scroll'))
web3_base = connect_to_network('base', config.get('RPCs', 'base'))
web3_mode = connect_to_network('mode', config.get('RPCs', 'mode'))
web3_blast = connect_to_network('blast', config.get('RPCs', 'blast'))

def read_addresses_from_file(file_path):
    addresses = []
    try:
        with open(file_path, 'r') as file:
            addresses = [line.strip() for line in file if line.strip()]  # Исключаем пустые строки
    except Exception as e:
        print(f"Ошибка при чтении адресов из файла: {e}")
    return addresses

async def get_eth_balance_async(loop, web3, address):
    try:
        balance_wei = await loop.run_in_executor(None, web3.eth.get_balance, address)
        balance_eth = round(web3.from_wei(balance_wei, 'ether'), 5)
        return balance_eth
    except Exception as e:
        return f"Ошибка при получении баланса: {e}"

def create_task(network_name, web3_instance, address, loop):
    if network_to_process.get(network_name):
        return get_eth_balance_async(loop, web3_instance, address)
    return '-'


async def process_address(address, loop):
    tasks = [
        create_task('ethereum', web3_eth, address, loop),
        create_task('arbitrum', web3_arb, address, loop),
        create_task('optimism', web3_op, address, loop),
        create_task('linea', web3_linea, address, loop),
        create_task('zksync', web3_zksync, address, loop),
        create_task('scroll', web3_scroll, address, loop),
        create_task('base', web3_base, address, loop),
        create_task('mode', web3_mode, address, loop),
        create_task('blast', web3_blast, address, loop),
    ]
    
    try:
        results = await asyncio.gather(*tasks)
        return {'Address': address, 'ETH': results[0], 'ETH_arb': results[1],
                'ETH_op': results[2], 'ETH_linea': results[3],
                'ETH_zksync': results[4], 'ETH_scroll': results[5],
                'ETH_base': results[6], 'ETH_mode': results[7], 
                'ETH_blast': results[8]}
    except Exception as e:
        return f"Ошибка при обработке адреса {address}: {e}"


async def main():
    addresses = read_addresses_from_file(addresses_file_path)
    tasks = []

    async with aiohttp.ClientSession() as session:
        loop = asyncio.get_event_loop()

        for address in addresses:
            task = process_address(address, loop)
            tasks.append(task)

        results = await asyncio.gather(*tasks)

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
    work_time_logs.write("Обработаны сети: ")
    for network in network_to_process:
        if network_to_process[network]: work_time_logs.write(f"{network} ")
    work_time_logs.write('\n')
    work_time_logs.write('\n')
