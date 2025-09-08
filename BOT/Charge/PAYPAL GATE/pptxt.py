import json
import time
import asyncio
import httpx
from pyrogram import Client, filters
from datetime import timedelta
from FUNC.usersdb_func import *
from FUNC.defs import *
from .gate import *
from .response import *
from TOOLS.check_all_func import *
from TOOLS.getcc_for_mass import *

async def mchkfunc(fullcc, user_id):
    retries = 3
    for attempt in range(retries):
        try:
            proxies = await get_proxy_format()
            async with httpx.AsyncClient(timeout=30, proxies=proxies, follow_redirects=True) as session:
                result = await create_paypal_charge(fullcc, session) # your PayPal charge async func
                getresp = await get_charge_resp(result, user_id, fullcc)
                response = getresp["response"]
                status = getresp["status"]
                return f"Card↯ <code>{fullcc}</code>\n<b>Status - {status}</b>\n<b>Result -⤿ {response} ⤾</b>\n\n"
        except Exception:
            import traceback
            await error_log(traceback.format_exc())
            if attempt < retries - 1:
                await asyncio.sleep(0.5)
                continue
            else:
                return f"<code>{fullcc}</code>\n<b>Result - DECLINED ❌</b>\n"
@Client.on_message(filters.command("pptxt", [".", "/"]))
async def receive_massfile(Client, message):
    try:
        if not message.reply_to_message or not message.reply_to_message.document:
            await message.reply_text("Please reply to a TXT file with this command.", message.id)
            return
        
        document = message.reply_to_message.document

        if not document.file_name.lower().endswith(".txt"):
            await message.reply_text("Please reply to a valid TXT file.", message.id)
            return
        
        user_id = str(message.from_user.id)
        first_name = str(message.from_user.first_name)
        checkall = await check_all_thing(Client, message)

        if not checkall[0]:
            return

        role = checkall[1]

        file_path = await Client.download_media(message=message.reply_to_message)
        
        with open(file_path, "r", encoding="utf-8") as f:
            ccs = [line.strip() for line in f if line.strip()]

        if not ccs:
            await message.reply_text("The uploaded file contains no cards.", message.id)
            return

        # Limit to first 50 cards if more are provided
        if len(ccs) > 50:
            ccs = ccs[:50]
            await message.reply_text("You uploaded more than 50 cards. Only the first 50 will be processed.", message.id)

        resp = f"""
- 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  Mass Card Check 💎

- 𝐂𝐂 𝐀𝐦𝐨𝐮𝐧𝐭 - {len(ccs)}
- 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 - Checking Cards For {first_name}

- 𝐒𝐭𝐚𝐭𝐮𝐬 - Processing...⌛️
"""
        nov = await message.reply_text(resp, message.id)

        # rest of your code unchanged ...
        text = f"""
<b>↯ Mass Card Check [/massfile]

Number Of Cards Checked : [{len(ccs)}]
</b>\n
"""
        amt = 0
        start = time.perf_counter()

        worker_num = int(json.loads(open("FILES/config.json", "r", encoding="utf-8").read())["THREADS"])

        works = [mchkfunc(card, user_id) for card in ccs]

        while works:
            batch = works[:worker_num]
            batch_results = await asyncio.gather(*batch)
            for result_str in batch_results:
                amt += 1
                text += result_str
                if amt % 5 == 0:
                    try:
                        await Client.edit_message_text(message.chat.id, nov.id, text)
                    except Exception:
                        pass
            await asyncio.sleep(1)
            works = works[worker_num:]

        taken = str(timedelta(seconds=time.perf_counter() - start))
        results = await getuserinfo(user_id)

        text += f"""
╚━━━━━━「 𝑰𝑵𝑭𝑶 」━━━━━━╝
⚜️ 𝑻𝒊𝒎𝒆 𝑺𝒑𝒆𝒏𝒕 -» {time.perf_counter() - start:0.2f} seconds
⚜️ 𝑪𝒉𝒆c𝒌𝒆𝗱 𝒃𝒚: <a href='tg://user?id={message.from_user.id}'> {first_name}</a> [ {role} ]
⚜️ 𝑶𝒘𝒏𝒆𝒓: <a href='tg://user?id=6622603977'>𝑵𝒂𝒊𝒓𝒐𝒃𝒊𝒂𝒏𝒈𝒐𝒐𝒏</a>
╚━━━━━━「𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃 𝐂𝐇𝐄𝐂𝐊𝐄𝐑」━━━━━━╝
"""
        await Client.edit_message_text(message.chat.id, nov.id, text)
        await massdeductcredit(user_id, len(ccs))
        await setantispamtime(user_id)

    except Exception:
        import traceback
        await error_log(traceback.format_exc())

