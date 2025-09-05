import json
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters
from FUNC.usersdb_func import getuserinfo, directcredit, get_last_claim_time, update_last_claim_time


@Client.on_message(filters.command("claim", [".", "/"]))
async def cmd_claim(client, message):
    try:
        user_id = str(message.from_user.id)
        
        # Config load if you want OWNER_ID check, otherwise skip below lines
        OWNER_ID = json.loads(open("FILES/config.json", "r", encoding="utf-8").read())["OWNER_ID"]

        # Optional: restrict command only to non-owners (or you can remove this)
        # if user_id in OWNER_ID:
        #     await message.reply_text("Owners can't use this command.")
        #     return

        # Credit to be claimed
        claim_amount = 250

        # Fetch user's last claim time (stored as timestamp)
        last_claim = await get_last_claim_time(user_id)  # You need to implement this

        now = datetime.utcnow()

        # Check if user has claimed in last 24 hours (86400 seconds)
        if last_claim:  # if there's an existing claim time
            last_claim_time = datetime.utcfromtimestamp(float(last_claim))
            time_diff = now - last_claim_time

            if time_diff < timedelta(hours=24):
                # Calculate how many hours left
                remaining = timedelta(hours=24) - time_diff
                hrs, rem = divmod(remaining.seconds, 3600)
                mins, secs = divmod(rem, 60)
                await message.reply_text(
                    f"You have already claimed your daily credits.\n"
                    f"Please wait {hrs}h {mins}m {secs}s before claiming again."
                )
                return

        # User can claim now
        user_info = await getuserinfo(user_id)
        previous_credit = int(user_info.get("credit", 0))
        new_credit = previous_credit + claim_amount

        # Update user's credits
        await directcredit(user_id, new_credit)

        # Update last claim time to now
        await update_last_claim_time(user_id, now.timestamp())

        await message.reply_text(
            f"🎉 You have successfully claimed {claim_amount} credits!\n"
            f"Previous credit: {previous_credit}\n"
            f"New credit balance: {new_credit}"
        )

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
        await message.reply_text("An error occurred while processing your claim.")
