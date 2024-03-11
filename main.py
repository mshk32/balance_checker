import pandas as pd
import time
import asyncio
from web3 import Web3
import datetime
import pytz
import configparser

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
web3_arb_nova = connect_to_network('arbitrum_nova', config.get('RPCs', 'arbitrum_nova'))

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
        if web3:
            balance_wei = await loop.run_in_executor(None, web3.eth.get_balance, address)
            balance_eth = round(web3.from_wei(balance_wei, 'ether'), 5)
            return balance_eth
        return '-'
    except Exception as e:
        return f"Ошибка при получении баланса: {e}"


async def process_address(address, loop):
    tasks = [
        get_eth_balance_async(loop, web3_eth, address),
        get_eth_balance_async(loop, web3_arb, address),
        get_eth_balance_async(loop, web3_op, address),
        get_eth_balance_async(loop, web3_linea, address),
        get_eth_balance_async(loop, web3_zksync, address),
        get_eth_balance_async(loop, web3_scroll, address),
        get_eth_balance_async(loop, web3_base, address),
        get_eth_balance_async(loop, web3_mode, address),
        get_eth_balance_async(loop, web3_blast, address),
        get_eth_balance_async(loop, web3_arb_nova, address)
    ]
    
    try:
        results = await asyncio.gather(*tasks)
        return {'Address': address, 'ETH': results[0], 'ETH_arb': results[1],
                'ETH_op': results[2], 'ETH_linea': results[3],
                'ETH_zksync': results[4], 'ETH_scroll': results[5],
                'ETH_base': results[6], 'ETH_mode': results[7], 
                'ETH_blast': results[8], 'ETH_arb_nova': results[9]}
    except Exception as e:
        return f"Ошибка при обработке адреса {address}: {e}"


async def main():
    addresses = read_addresses_from_file(addresses_file_path)
    tasks = []

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
    with open(addresses_file_path, 'r') as wallets:
        number_of_wallets = len(wallets.readlines())
        work_time_logs.write(f"Кошельков обработано: {number_of_wallets}")
    work_time_logs.write('\n')
    work_time_logs.write('\n')