import traceback
from FUNC.defs import *
from FUNC.usersdb_func import *

async def get_charge_resp(result, user_id, fullcc):
    try:
        print(f"[DEBUG] Incoming result (truncated): {repr(result)[:500]}")

        status = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌"
        response = "Card Declined ❌"
        hits = "NO"

        # Successful charges
        if (
            '"status": "succeeded"' in result or
            "Thank You For Donation" in result or
            "Your payment has already been processed" in result or
            "ADD_SHIPPING_ERROR" in result or
            "Success" in result
        ):
            status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
            response = "Thank You For Donation 🔥"
            hits = "YES"
            await forward_resp(fullcc, "PayPal Charge", response)

        elif "is3DSecureRequired" in result or "OTP" in result:
            status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
            response = "3D Secure Challenge Required 🔐"
            hits = "YES"
            await forward_resp(fullcc, "PayPal Charge", response)

        elif "INVALID_SECURITY_CODE" in result:
            status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
            response = "CCN Live ✅"
            hits = "YES"
            await forward_resp(fullcc, "PayPal Charge", response)

        elif "INVALID_BILLING_ADDRESS" in result:
            status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
            response = "Invalid billing address🏡"
            hits = "YES"
            await forward_resp(fullcc, "PayPal Charge", response)

        elif "EXISTING_ACCOUNT_RESTRICTED" in result:
            status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
            response = "EXISTING_ACCOUNT_RESTRICTED"
            hits = "YES"
            await forward_resp(fullcc, "PayPal Charge", response)

        elif "ProxyError" in result or "ConnectionError" in result:
            status = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌"
            response = "Proxy Connection Failed 🔌"
            hits = "NO"
            await refundcredit(user_id)

        elif "COUNTRY_NOT_SUPPORTED" in result:
            status = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌"
            response = "Card not supported in your country ❌"
            hits = "NO"

        elif "CARD_DECLINED" in result:
            status = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌"
            response = "Card was declined by the bank ❌"
            hits = "NO"

        elif "declined" in result:
            status = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌"
            response = "Card declined ❌"
            hits = "NO"

        elif "CARD_GENERIC_ERROR" in result:
            status = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌"
            response = "GENERIC_ERROR ❌"
            hits = "NO"

        elif "invalid_card" in result:
            status = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌"
            response = "Invalid card number ❌"
            hits = "NO"

        elif "RISK_DISALLOWED" in result:
            status = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌"
            response = "RISK_DISALLOWED ❌"
            hits = "NO"

        elif "cardNumber" in result:
            status = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌"
            response = "Card Generic error ❌"
            hits = "NO"

        elif "VALIDATION_ERROR" in result:
            status = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌"
            response = "VALIDATION_ERROR ❌"
            hits = "NO"

        else:
            # fallback extraction - be tolerant if substrings missing
            extracted_msg = await find_between(result, "System was not able to complete the payment. ", ".")
            if extracted_msg:
                response = extracted_msg + " ❌"
            else:
                response = "Card Declined ❌"
                await result_logs(fullcc, "PayPal Charge", result)
            hits = "NO"

        json_response = {
            "status": status,
            "response": response,
            "hits": hits,
            "fullz": fullcc,
        }
        return json_response

    except Exception as e:
        return {
            "status": "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝗱 ❌",
            "response": f"{str(e)} ❌",
            "hits": "NO",
            "fullz": fullcc,
        }
