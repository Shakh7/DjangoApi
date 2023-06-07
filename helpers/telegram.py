import requests
from .env import load_env
from django.core.mail import send_mail


def notify_new_quote(quote):
    token = load_env('APP_TELEGRAM_API_TOKEN')
    chat_id = load_env('APP_TELEGRAM_CHAT_ID')
    text = f'New lead ✅: \n\n' \
           f'Car Make: {quote.car_make.name}\n' \
           f'Car Model: {quote.car_model.name}\n' \
           f'Car Year: {quote.car_year} \n' \
           f'Pick Up: {quote.origin.zip_code} {quote.origin.city_name}, {quote.origin.state_code}\n' \
           f'Drop Off: {quote.destination.zip_code} {quote.destination.city_name}, {quote.destination.state_code}\n' \
           f'Full Name: {quote.shipper.get_full_name()} \n' \
           f'Email: {quote.shipper.email} \n\n' \
           f'Created At: {quote.created_at}'
    try:
        requests.get(
            f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=Markdown')
    except:
        pass

    try:
        send_mail(
            "Car Shipping Request",
            f"Dear {quote.shipper.first_name},\n\n"
            f"Thank you for choosing our car shipping service. "
            f"We have received your request to ship your {quote.car_year} {quote.car_make} {quote.car_model}.\n\n"
            f"We will review your request and get back to you with further details shortly.\n\n"
            f"Best regards,\n"
            f"ShipperAuto.com",
            "shipperauto.com@gmail.com",
            [quote.shipper.email],
            fail_silently=False,
        )
    except:
        pass


def send_auth_one_time_code(code):
    token = load_env('APP_TELEGRAM_API_TOKEN')
    chat_id = load_env('APP_TELEGRAM_CHAT_ID')
    text = f"Your login code is: {code}"

    requests.get(
        f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=Markdown')
