import time
from web3 import Web3
from concurrent.futures import ThreadPoolExecutor

# Подключение к RPC-узлу сети Base
web3 = Web3(Web3.HTTPProvider('https://base-mainnet.rpcurl.com'))  # Замените на правильный RPC узел

# Проверяем подключение
if not web3.isConnected():
    print("Ошибка подключения к сети")
    exit()

# Данные кошелька отправителя
sender_address = '0xYourSenderAddress'  # Замените на ваш адрес отправителя
private_key = '0xYourPrivateKey'        # Замените на ваш приватный ключ

# Чтение списка адресов из файла
def read_recipients_from_file(file_path):
    with open(file_path, 'r') as f:
        recipients = [line.strip() for line in f if line.strip()]
    return recipients

# Функция отправки эфира
def send_ether(recipient, amount, nonce, gas_price, delay):
    try:
        # Подготовка транзакции
        tx = {
            'nonce': nonce,
            'to': recipient,
            'value': web3.toWei(amount, 'ether'),
            'gas': 21000,  # Стандартный лимит газа для отправки эфира
            'gasPrice': web3.toWei(gas_price, 'gwei'),
        }

        # Подписываем транзакцию
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)

        # Отправляем транзакцию
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Печатаем хэш транзакции
        print(f"Transaction sent to {recipient}: {web3.toHex(tx_hash)}")
        
        # Задержка между отправками
        time.sleep(delay)

    except Exception as e:
        print(f"Ошибка при отправке на {recipient}: {str(e)}")

# Основная функция массовой отправки
def bulk_send_ether(recipients, amount, gas_price, threads, delay):
    # Получаем текущий nonce отправителя
    nonce = web3.eth.getTransactionCount(sender_address)

    # Используем ThreadPoolExecutor для параллельной отправки
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for i, recipient in enumerate(recipients):
            executor.submit(send_ether, recipient, amount, nonce + i, gas_price, delay)

# Параметры
recipients_file = 'recipients.txt'  # Файл с адресами получателей
amount_to_send = 0.01  # Сумма, отправляемая каждому получателю в ETH
gas_price_gwei = 1     # Цена газа в gwei (оптимизируйте по ситуации)
threads_count = 5      # Количество одновременных потоков
delay_between_sends = 2  # Задержка между отправками в секундах

# Чтение адресов из файла
recipients_list = read_recipients_from_file(recipients_file)

# Запуск массовой отправки
bulk_send_ether(recipients_list, amount_to_send, gas_price_gwei, threads_count, delay_between_sends)
