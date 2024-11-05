import tkinter as tk
from tkinter import messagebox
import requests
from loguru import logger
from PIL import Image, ImageTk  # Импортируем для работы с изображениями


def get_crypto_price(crypto_id, vs_currency="usd"):
    """
    Функция для получения курса криптовалюты к заданной валюте.

    :param crypto_id: Идентификатор криптовалюты (например, 'bitcoin').
    :param vs_currency: Валюта, к которой необходимо получить курс (по умолчанию 'usd').
    :return: Курс криптовалюты к заданной валюте.
    :raises: requests.exceptions.RequestException если возникает ошибка при запросе к API,
             KeyError если данные от API имеют неверный формат.
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={vs_currency}"
        response = requests.get(url)
        response.raise_for_status()  # Проверка статуса ответа

        data = response.json()
        price = data[crypto_id][vs_currency]
        logger.info(f"Курс {crypto_id} к {vs_currency.upper()}: {price}")
        return price
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к API CoinGecko: {e}")
        raise
    except KeyError:
        logger.error("Ошибка формата данных от API")
        raise


def on_check_price():
    """
    Функция обработки события нажатия кнопки для получения курса криптовалюты.

    Проверяет выбранную криптовалюту и отображает ее курс.
    Выводит предупреждение, если криптовалюта не выбрана, и сообщение об ошибке в случае неудачи.
    """
    selected_crypto = crypto_var.get()
    if not selected_crypto:
        messagebox.showwarning("Предупреждение", "Выберите криптовалюту")
        return

    crypto_id = crypto_dict[selected_crypto]
    try:
        price = get_crypto_price(crypto_id)
        result_label.config(text=f"Курс {selected_crypto}: ${price}")
    except Exception as e:
        logger.error(f"Ошибка при получении курса: {e}")
        messagebox.showerror("Ошибка", "Не удалось получить данные о курсе криптовалюты.")


# Настройка интерфейса Tkinter
root = tk.Tk()
root.title("Курс обмена валюты")
root.geometry("300x300")

# Загружаем логотип
logo_image = Image.open(
    r'C:\Users\wangr\OneDrive\Изображения\photo_2024-11-05_11-02-28-fotor-bg-remover-2024110511450.png')  # Замените на путь к вашему логотипу
logo_image = logo_image.resize((150, 150), Image.LANCZOS)  # Изменяем размер изображения
logo_photo = ImageTk.PhotoImage(logo_image)

# Установка логотипа как иконки окна
root.iconphoto(False, logo_photo)

# Заголовок окна
title_label = tk.Label(root, text="Курс обмена валюты", font=("Arial", 14, "bold"))
title_label.pack(pady=5)

# Надпись для базовой валюты
base_currency_label = tk.Label(root, text="Базовая валюта")
base_currency_label.pack(pady=5)

# Выпадающий список для выбора базовой валюты (по ТЗ оставляем только доллар США)
base_var = tk.StringVar(value="USD")
base_dropdown = tk.OptionMenu(root, base_var, "USD")
base_dropdown.config(width=15)
base_dropdown.pack(pady=5)

# Надпись для целевой валюты
target_currency_label = tk.Label(root, text="Целевая валюта")
target_currency_label.pack(pady=5)

# Список целевых валют
crypto_dict = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Ripple": "ripple",
    "Litecoin": "litecoin",
    "Cardano": "cardano"
}

# Выпадающий список для выбора целевой валюты
crypto_var = tk.StringVar()
crypto_dropdown = tk.OptionMenu(root, crypto_var, *crypto_dict.keys())
crypto_dropdown.config(width=15)
crypto_dropdown.pack(pady=5)

# Кнопка для проверки курса
check_button = tk.Button(root, text="Получить курс обмена", command=on_check_price)
check_button.pack(pady=10)

# Метка для отображения результата
result_label = tk.Label(root, text="Курс появится здесь")
result_label.pack(pady=10)

root.mainloop()
