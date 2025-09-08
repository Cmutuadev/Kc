from FUNC.defs import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command("buy", [".", "/"]))
async def cmd_buy(client, message):
    try:
        price_list = """
📝 <b>ᴍᴀꜱᴛᴇʀ ᴄʜᴇᴄᴋᴇʀ ᴋᴇPlans :</b>
━━━━━━━━━━━━━━
● <b>Starter</b> - Unlimited Credits + Premium Access For 1 Week at <b>$4</b>

● <b>Silver</b> - Unlimited Credits + Premium Access For 15 Days at <b>$7</b>

● <b>Gold</b> - Unlimited Credits + Premium Access For 1 Month at <b>$13</b>

● <b>Custom Plan</b> - You can buy any custom plan above 1 month...

<i>Note: All plans are available for 7, 15, or 30 days. Once your plan expires, you will need to purchase a new one to continue using our services. Please note that all purchases are non-refundable, and you cannot transfer plans to another account.</i>
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛎 Knock Admin",
                        url="http://t.me/nairobiangoon",
                    ),
                    InlineKeyboardButton(
                        text="💳 Payment Area",
                        callback_data="show_payment_methods",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Exit",
                        callback_data="close_message",
                    )
                ]
            ]
        )
        await message.reply_text(price_list, reply_markup=keyboard, disable_web_page_preview=True)

    except Exception:
        import traceback
        await error_log(traceback.format_exc())


@Client.on_callback_query(filters.regex("show_payment_methods"))
async def show_payment_methods(client, callback_query):
    try:
        payment_info = """
📝 <b>ᴍᴀꜱᴛᴇʀ ᴄʜᴇᴄᴋᴇʀ ᴋᴇ⚡️ Methods:</b>
━━━━━━━━━━━━━━

💰 <b>BINANCE ID/PAY</b> - <code>550157299</code>

💰 <b>USDT [TRC20]</b> - <code>TJdQfLWo6mCSa2XnvjAV72eTK4qeWNDdRw</code>

<i>Note: After completing the payment, click Knock Admin, then send the transaction screenshot with your Telegram ID.</i>
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📋 Plan List",
                        callback_data="show_price_list",
                    ),
                    InlineKeyboardButton(
                        text="🛎 Knock Admin",
                        url="http://t.me/nairobiangoon",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Exit",
                        callback_data="close_message",
                    )
                ]
            ]
        )
        await callback_query.message.edit_text(payment_info, reply_markup=keyboard)

    except Exception:
        import traceback
        await error_log(traceback.format_exc())


@Client.on_callback_query(filters.regex("show_price_list"))
async def show_price_list(client, callback_query):
    try:
        price_list = """
📝 <b>ᴍᴀꜱᴛᴇʀ ᴄʜᴇᴄᴋᴇʀ ᴋᴇ ⚡️ Plans :</b>
━━━━━━━━━━━━━━
● <b>Starter</b> - Unlimited Credits + Premium Access For 1 Week at <b>$4</b>

● <b>Silver</b> - Unlimited Credits + Premium Access For 15 Days at <b>$7</b>

● <b>Gold</b> - Unlimited Credits + Premium Access For 1 Month at <b>$13</b>

<i>Note: All plans are available for 7, 15, or 30 days. Once your plan expires, you will need to purchase a new one to continue using our services. Please note that all purchases are non-refundable, and you cannot transfer plans to another account.</i>
        """
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛎 Knock Admin",
                        url="http://t.me/nairobiangoon",
                    ),
                    InlineKeyboardButton(
                        text="💳 Payment Area",
                        callback_data="show_payment_methods",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Exit",
                        callback_data="close_message",
                    )
                ]
            ]
        )
        await callback_query.message.edit_text(price_list, reply_markup=keyboard)

    except Exception:
        import traceback
        await error_log(traceback.format_exc())


@Client.on_callback_query(filters.regex("close_message"))
async def close_message(client, callback_query):
    try:
        await callback_query.message.delete()
        await callback_query.message.reply_text("")

    except Exception:
        import traceback
        await error_log(traceback.format_exc())