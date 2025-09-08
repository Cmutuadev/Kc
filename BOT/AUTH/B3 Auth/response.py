import traceback
from FUNC.defs import *
from FUNC.usersdb_func import *


async def get_charge_resp(result, user_id, fullcc):
    try:
        if isinstance(result, str):
            return {
                "status": "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌",
                "response": result,
                "hits": "NO",
                "fullz": fullcc,
            }

        text = result.text.lower()

        success_phrases = [
            "succeeded",
            "thank you for your order",
            "thank you!",
            "thank you",
            "you have received a payout",
            "requires_action:true",
            "transaction_status:success",
            "key=wc_order",
            "secret",
        ]
        if any(phrase in text for phrase in success_phrases):
            status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
            response = "1000: 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
            hits = "YES"
            await forward_resp(fullcc, "sitebase Charge 1$", response)

        elif any(phrase in text for phrase in ["insufficient_funds", "card has insufficient funds."]):
            status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
            response = "Avs Live🟢"
            hits = "YES"
            await forward_resp(fullcc, "sitebase Charge 1$", response)

        elif any(phrase in text for phrase in ["incorrect_cvc", "security code is incorrect", "your card's security code is incorrect", "invalid security code"]):
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            response = "Gateway Rejected: cvv"
            hits = "NO"
            await forward_resp(fullcc, "sitebase Charge 1$", response)

        elif any(phrase in text for phrase in ["transaction_not_allowed", "currency_compliance"]):
            status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
            response = "Card Doesn't Support Currency 🔴"
            hits = "YES"
            await forward_resp(fullcc, "sitebase Charge 1$", response)

        elif '"cvc_check": "pass"' in text:
            status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
            response = "CVV LIVE 🔴"
            hits = "YES"
            await forward_resp(fullcc, "sitebase Charge 1$", response)

        elif "invalid_billing_address" in text:
            status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
            response = "AVS LIVE🟢"
            hits = "YES"
            await forward_resp(fullcc, "sitebase Charge 1$", response)

        elif "your session has expired" in text or "sorry, your session has expired" in text:
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            response = "Session Expired ❌"
            hits = "NO"

        elif any(phrase in text for phrase in ["three_d_secure_redirect", "card_error_authentication_required", "is3dsecurerequired", "#wc-stripe-confirm-pi", "stripe_3ds2_fingerprint"]):
            status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
            response = "3D Challenge Required ❎"
            hits = "YES"
            await forward_resp(fullcc, "sitebase Charge 1.50$", response)

        elif "your card does not support this type of purchase." in text:
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            response = "2044: Declined - Call Issuer"
            hits = "YES"
            await forward_resp(fullcc, "sitebase Charge 1.50$", response)

        elif any(phrase in text for phrase in ["generic_decline", "you have exceeded the maximum number of declines on this card in the last 24 hour period.", "card_decline_rate_limit_exceeded", "card_generic_error", "your card was declined", "the card was declined"]):
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            response = "Card was declined"
            hits = "NO"

        elif any(phrase in text for phrase in ["do_not_honor", "fraudulent", "stolen_card", "lost_card", "pickup_card", "invalid_cvc", "setup_intent_authentication_failure"]):
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            # Capitalize and format phrase for readability
            matched_phrase = next(p for p in ["do_not_honor", "fraudulent", "stolen_card", "lost_card", "pickup_card", "invalid_cvc", "setup_intent_authentication_failure"] if p in text)
            response = matched_phrase.replace('_', ' ').title() + " ❌"
            hits = "NO"

        elif any(phrase in text for phrase in ["incorrect_number", "your card number is incorrect.", "incorrect card number"]):
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            response = "Incorrect Card Number ❌"
            hits = "NO"

        elif any(phrase in text for phrase in ["your card has expired.", "expired_card"]):
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            response = "2004: Expired Card ❌"
            hits = "NO"

        elif any(phrase in text for phrase in ["invalid_account", "card is not supported."]):
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            response = "Card Not Supported or Dead Card ❌"
            hits = "NO"

        elif any(phrase in text for phrase in ["invalid api key provided", "testmode_charges_only", "api_key_expired", "your account cannot currently make live charges."]):
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            response = "Stripe error. Contact support@stripe.com for more details ❌"
            hits = "NO"

        elif "payment intent creation failed ❌" in text:
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            response = "Payment Intent Creation Failed ❌"
            hits = "NO"
            await refundcredit(user_id)

        elif "proxyerror" in text:
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            response = "Proxy Connection Refused ❌"
            hits = "NO"
            await refundcredit(user_id)

        else:
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            response = await find_between(result.text, "System was not able to complete the payment. ", ".")
            if not response:
                response = "Card Declined"
                await result_logs(fullcc, "Stripe Charge", result)
            response += " ❌"
            hits = "NO"

        return {
            "status": status,
            "response": response,
            "hits": hits,
            "fullz": fullcc,
        }

    except Exception as e:
        return {
            "status": "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌",
            "response": str(e) + " ❌",
            "hits": "NO",
            "fullz": fullcc,
        }
