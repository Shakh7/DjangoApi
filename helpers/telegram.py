import requests
from .env import load_env

def notify_new_quote(quote):
    token = load_env('APP_TELEGRAM_API_TOKEN')
    chat_id = load_env('APP_TELEGRAM_CHAT_ID')
    text = f'New lead ✅: \n\n' \
           f'Car Make: {quote.car_make.name}\n' \
           f'Car Model: {quote.car_model.name}\n' \
           f'Car Year: {quote.car_year} \n' \
           f'Pick Up: {quote.origin.zip_code} {quote.origin.city_name}, {quote.origin.state_code}\n' \
           f'Drop Off: {quote.destination.zip_code} {quote.destination.city_name}, {quote.destination.state_code}\n' \
           f'Pick Up Date: {quote.pick_up_date} \n' \
           f'Name: {quote.first_name} \n' \
           f'Email: {quote.email} \n\n' \
           f'Created At: {quote.created_at}'
    try:
        requests.get(
            f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=Markdown')
    except:
        pass

def send_auth_one_time_code(code):
    token = load_env('APP_TELEGRAM_API_TOKEN')
    chat_id = load_env('APP_TELEGRAM_CHAT_ID')
    text = f"Your login code is: {code}"

    requests.get(
        f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=Markdown')
