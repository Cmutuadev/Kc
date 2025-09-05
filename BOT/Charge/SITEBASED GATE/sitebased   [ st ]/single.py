import httpx
import time
import asyncio
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from FUNC.defs import *
from TOOLS.check_all_func import *
from TOOLS.getbin import *
from .response import *
from .gate import *


@Client.on_message(filters.command("st", [".", "/"]))
async def stripe_auth_cmd(Client, message):
    try:
        user_id = str(message.from_user.id)
        checkall = await check_all_thing(Client, message)

        gateway = "Non Sk [5$]"

        if checkall[0] == False:
            return

        role = checkall[1]
        getcc = await getmessage(message)
        if getcc == False:
            resp = f"""<b>
Gate Name: {gateway} ♻️
CMD: /st

Message: No CC Found in your input ❌

Usage: /st cc|mes|ano|cvv</b>"""
            await message.reply_text(resp, message.id)
            return

        cc, mes, ano, cvv = getcc[0], getcc[1], getcc[2], getcc[3]
        fullcc = f"{cc}|{mes}|{ano}|{cvv}"

        firstresp = f"""
↯ Checking.

- 𝐂𝐚𝐫𝐝 - <code>{fullcc}</code> 
- 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  <i>{gateway}</i>
- 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ■□□□
</b>
"""
        await asyncio.sleep(0.5)
        firstchk = await message.reply_text(firstresp, message.id)

        secondresp = f"""
↯ Checking..

- 𝐂𝐚𝐫𝐝 - <code>{fullcc}</code> 
- 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  <i>{gateway}</i>
- 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ■■■□
"""
        await asyncio.sleep(0.5)
        secondchk = await Client.edit_message_text(message.chat.id, firstchk.id, secondresp)

        start = time.perf_counter()
        # proxies = await get_proxy_format()
        session = httpx.AsyncClient(timeout=30, follow_redirects=True)
        sks = await getallsk()
        result = await create_cvv_charge(fullcc, session)
        getbin = await get_bin_details(cc)
        getresp = await get_charge_resp(result, user_id, fullcc)

        status = getresp.get("status", "").strip()
        response = getresp.get("response", "").strip()

        # DEBUG: Print status and response for troubleshooting
        print(f"DEBUG: status = '{status}', response = '{response}'")

        thirdresp = f"""
↯ Checking...

- 𝐂𝐚𝐫𝐝 - <code>{fullcc}</code> 
- 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  <i>{gateway}</i>
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

𝗖𝗮𝗿𝗱- <code>{fullcc}</code> 
𝐆𝐚𝐭𝐞𝐰𝐚𝐲- <i>{gateway}</i>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞- ⤿ <i>{response}</i> ⤾

𝗜𝗻𝗳𝗼- {brand} - {type_} - {level}
𝐁𝐚𝐧𝐤- {bank} 
𝐂𝐨𝐮𝐧𝐭𝐫𝐲- {country} - {flag} - {currency}

𝗧𝗶𝗺𝗲- {time.perf_counter() - start:0.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
"""
        await asyncio.sleep(0.5)
        await Client.edit_message_text(message.chat.id, thirdcheck.id, finalresp)
        await setantispamtime(user_id)
        await deductcredit(user_id)

        # More flexible check for approved status
        approved_keywords = ["approved", "success", "paid"]
        if any(keyword in status.lower() for keyword in approved_keywords):
            await sendcc(finalresp, session)

        await session.aclose()

    except Exception:
        import traceback
        await error_log(traceback.format_exc())
