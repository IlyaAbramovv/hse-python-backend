import requests
import time

BASE_URL = 'http://localhost:8080'


def create_cart():
    response = requests.post(f'{BASE_URL}/cart/')
    if 100 <= response.status_code < 300:
        cart_id = response.json().get('id')
        print(f'Создана корзина с ID: {cart_id}')
        return cart_id
    else:
        print('Ошибка создания корзины')
        return None


def get_cart(cart_id):
    response = requests.get(f'{BASE_URL}/cart/{cart_id}')
    if 200 <= response.status_code < 300:
        cart_data = response.json()
        print('Данные корзины:', cart_data)
    else:
        print('Ошибка получения корзины')


def add_item_to_cart(cart_id, item_id):
    response = requests.post(f'{BASE_URL}/cart/{cart_id}/add/{item_id}')
    if response.status_code < 300:
        print(f'Товар с ID {item_id} добавлен в корзину {cart_id}')
    else:
        print('Ошибка добавления товара в корзину')


def create_item():
    item_data = {
        "name": "Молоко \"Буреночка\" 1л.",
        "price": 159.99,
        "deleted": False
    }
    response = requests.post(f'{BASE_URL}/item/', json=item_data)
    if 200 <= response.status_code < 300:
        item_id = response.json().get('id')
        print(f'Создан товар с ID: {item_id}')
        return item_id
    else:
        print('Ошибка создания товара')
        return None


def get_item(item_id):
    response = requests.get(f'{BASE_URL}/item/{item_id}')
    if 200 <= response.status_code < 300:
        item_data = response.json()
        print('Данные товара:', item_data)
    else:
        print('Ошибка получения товара')


def run_client(duration=60):
    start_time = time.time()
    while time.time() - start_time < duration:
        cart_id = create_cart()
        if cart_id:
            item_id = create_item()
            if item_id:
                add_item_to_cart(cart_id, item_id)
                get_cart(cart_id)
                get_item(item_id)
        time.sleep(5)


if __name__ == "__main__":
    run_client(60)
