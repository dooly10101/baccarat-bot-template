import os, sqlite3, random, logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from keep_alive import keep_alive

ADMIN_IDS = [5783625431]  # 본인의 Telegram user_id 입력

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, balance INTEGER)")
conn.commit()

keep_alive()

async def 시작(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if not c.fetchone():
        c.execute("INSERT INTO users VALUES (?, ?)", (user_id, 10000))
        conn.commit()
        await update.message.reply_text("🎉 가입 완료! 둘리코인 10,000 지급!")
    else:
        await update.message.reply_text("이미 가입되어 있습니다.")

async def 잔액(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    c.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    res = c.fetchone()
    if res:
        await update.message.reply_text(f"💰 현재 잔액: {res[0]} 둘리코인")
    else:
        await update.message.reply_text("❗ /시작 으로 가입해주세요.")

async def 배팅(update: Update, context: ContextTypes.DEFAULT_TYPE, bet_on: str):
    user_id = update.effective_user.id
    args = context.args
    if len(args) != 1 or not args[0].isdigit():
        await update.message.reply_text("💡 예시: /뱅 1000 또는 /플 500")
        return

    amount = int(args[0])
    c.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    res = c.fetchone()
    if not res:
        await update.message.reply_text("❗ /시작 으로 먼저 가입해주세요.")
        return

    balance = res[0]
    if balance < amount:
        await update.message.reply_text("❗ 잔액 부족!")
        return

    player_total = random.randint(0, 9)
    banker_total = random.randint(0, 9)
    win = "플" if player_total > banker_total else "뱅"

    if win == bet_on:
        balance += amount
        msg = f"🎉 {bet_on} 승리! +{amount} 둘리코인"
    else:
        balance -= amount
        msg = f"😢 {bet_on} 패배... -{amount} 둘리코인"

    c.execute("UPDATE users SET balance=?", (balance, user_id))
    conn.commit()
    await update.message.reply_text(
        f"{msg}\n🎯 결과: 플레이어 {player_total}, 뱅커 {banker_total}\n💰 현재 잔액: {balance}"
    )

async def 뱅(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await 배팅(update, context, "뱅")

async def 플(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await 배팅(update, context, "플")

async def 충전(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ 관리자만 사용할 수 있습니다.")
        return
    try:
        target_id = int(context.args[0])
        amount = int(context.args[1])
        c.execute("INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, 0)", (target_id,))
        c.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, target_id))
        conn.commit()
        await update.message.reply_text(f"✅ {target_id}님에게 {amount} 둘리코인 충전 완료.")
    except:
        await update.message.reply_text("💡 예시: /충전 123456789 5000")

import asyncio
async def main():
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("시작", 시작))
    app.add_handler(CommandHandler("잔액", 잔액))
    app.add_handler(CommandHandler("뱅", 뱅))
    app.add_handler(CommandHandler("플", 플))
    app.add_handler(CommandHandler("충전", 충전))

    print("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
