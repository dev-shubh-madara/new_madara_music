import asyncio
import io
import qrcode
from pyrogram import filters
from pyrogram.types import Message, InlineQuery, InlineQueryResultPhoto, InputMediaPhoto
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.mongo import mongodb as db
from config import BANNED_USERS

upi_db = db.upi_ids

QR_EXPIRY_SECONDS = 600


def generate_upi_qr(upi_id: str, amount: float, name: str = "Merchant") -> io.BytesIO:
    upi_uri = f"upi://pay?pa={upi_id}&pn={name}&am={amount:.2f}&cu=INR"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    buf.name = "upi_qr.png"
    return buf


@app.on_message(filters.command(["setupi"]) & ~BANNED_USERS)
async def set_upi(client, message: Message):
    args = message.command
    if len(args) < 2:
        return await message.reply_text(
            "❌ <b>Usage:</b> <code>/setupi yourupi@bank</code>\n\n"
            "<i>Example: /setupi ragini@upi or /setupi 9876543210@paytm</i>"
        )
    upi_id = args[1].strip()
    if "@" not in upi_id:
        return await message.reply_text(
            "❌ <b>Invalid UPI ID.</b>\n"
            "<i>A valid UPI ID looks like: name@bank or number@paytm</i>"
        )
    user_id = message.from_user.id
    await upi_db.update_one(
        {"_id": user_id},
        {"$set": {"upi_id": upi_id, "name": message.from_user.first_name}},
        upsert=True,
    )
    await message.reply_text(
        f"✅ <b>UPI ID saved securely!</b>\n\n"
        f"🔐 <b>Your UPI ID :</b> <code>{upi_id}</code>\n\n"
        f"<i>Now use /gen {'<amount>'} to generate a payment QR code.</i>"
    )


@app.on_message(filters.command(["gen"]) & ~BANNED_USERS)
async def gen_qr(client, message: Message):
    args = message.command
    if len(args) < 2:
        return await message.reply_text(
            "❌ <b>Usage:</b> <code>/gen {amount}</code>\n\n"
            "<i>Example: /gen 100 or /gen 49.99</i>\n"
            "<i>First set your UPI ID with /setupi</i>"
        )
    try:
        amount = float(args[1])
        if amount <= 0:
            raise ValueError
    except ValueError:
        return await message.reply_text("❌ <b>Invalid amount.</b> Please enter a valid positive number.")

    user_id = message.from_user.id
    data = await upi_db.find_one({"_id": user_id})
    if not data:
        return await message.reply_text(
            "❌ <b>No UPI ID found!</b>\n\n"
            "<i>Please set your UPI ID first using:</i>\n"
            "<code>/setupi yourupi@bank</code>"
        )

    upi_id = data["upi_id"]
    name = data.get("name", "Merchant")

    m = await message.reply_text("⚡️ <b>Generating QR Code...</b>")
    qr_buf = generate_upi_qr(upi_id, amount, name)

    sent = await message.reply_photo(
        photo=qr_buf,
        caption=(
            f"<b>💸 UPI Payment QR Code</b>\n\n"
            f"💳 <b>UPI ID :</b> <code>{upi_id}</code>\n"
            f"💰 <b>Amount :</b> <code>₹{amount:.2f}</code>\n"
            f"👤 <b>Name :</b> {name}\n\n"
            f"⏳ <b>This QR expires in 10 minutes!</b>\n"
            f"<i>Scan using any UPI app — PhonePe, GPay, Paytm, etc.</i>"
        ),
    )
    await m.delete()

    await asyncio.sleep(QR_EXPIRY_SECONDS)
    try:
        await sent.delete()
    except Exception:
        pass


@app.on_inline_query(filters.regex(r"^gen\s+\d+(\.\d+)?$"))
async def inline_gen_qr(client, inline_query: InlineQuery):
    try:
        amount_str = inline_query.query.split()[1]
        amount = float(amount_str)
    except (IndexError, ValueError):
        return

    user_id = inline_query.from_user.id
    data = await upi_db.find_one({"_id": user_id})
    if not data:
        return

    upi_id = data["upi_id"]
    name = data.get("name", "Merchant")
    qr_buf = generate_upi_qr(upi_id, amount, name)

    caption = (
        f"<b>💸 UPI Payment QR Code</b>\n\n"
        f"💳 <b>UPI ID :</b> <code>{upi_id}</code>\n"
        f"💰 <b>Amount :</b> <code>₹{amount:.2f}</code>\n"
        f"👤 <b>Name :</b> {name}\n\n"
        f"⏳ <b>QR expires in 10 minutes!</b>"
    )

    results = [
        InlineQueryResultPhoto(
            photo_url="https://files.catbox.moe/5go4t6.jpg",
            thumb_url="https://files.catbox.moe/5go4t6.jpg",
            title=f"Generate ₹{amount:.2f} Payment QR",
            description=f"UPI: {upi_id}",
            caption=caption,
        )
    ]
    await inline_query.answer(results, cache_time=0)
