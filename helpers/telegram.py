import requests
from .env import load_env


def notify_new_quote(quote):
    TOKEN = load_env('APP_TELEGRAM_API_TOKEN')
    CHAT_ID = load_env('APP_TELEGRAM_CHAT_ID')
    text = f'New lead ✅: \n\n' \
           f'Car Make: {quote.car_make.name}\n' \
           f'Car Model: {quote.car_model.name}\n' \
           f'Car Year: {quote.car_year} \n' \
           f'Pick Up: {quote.origin.zip_code} {quote.origin.city_name}, {quote.origin.state_code}\n' \
           f'Drop Off: {quote.destination.zip_code} {quote.destination.city_name}, {quote.destination.state_code}\n' \
           f'Pick Up Date: {quote.pick_up_date} \n' \
           f'Name: {quote.customer.full_name} \n' \
           f'Email: {quote.customer.email} \n\n' \
           f'Created At: {quote.created_at}'

    requests.get(
        f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}&parse_mode=Markdown')
