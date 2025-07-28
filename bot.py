import logging
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 로깅
logging.basicConfig(level=logging.INFO)

# 데이터베이스 연결
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    name TEXT,
    balance INTEGER DEFAULT 100000
)
''')
conn.commit()

# 봇 시작 핸들러
async def 시작(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    cursor.execute('SELECT * FROM users WHERE user_id=?', (user.id,))
    if cursor.fetchone() is None:
        cursor.execute(
            'INSERT INTO users (user_id, username, name) VALUES (?, ?, ?)',
            (user.id, user.username, user.first_name)
        )
        conn.commit()
        await update.message.reply_text(f"환영합니다, {user.first_name}님! 초기 잔액 100,000원이 지급되었습니다.")
    else:
        await update.message.reply_text(f"{user.first_name}님, 이미 가입되어 있습니다!")

# 내 정보 핸들러
async def 내정보(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    cursor.execute('SELECT * FROM users WHERE user_id=?', (user.id,))
    row = cursor.fetchone()
    if row:
        _, username, name, balance = row
        await update.message.reply_text(
            f"👤 내 정보\n\n"
            f"🆔 아이디: @{username} [ {user.id} ]\n"
            f"📝 이름: {name}\n"
            f"💰 잔액: {balance:,}원"
        )
    else:
        await update.message.reply_text("가입 정보가 없습니다. /시작 으로 가입해주세요!")

# 메인 함수
def main():
    BOT_TOKEN = "여기에_당신의_BOT_TOKEN"
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("시작", 시작))
    app.add_handler(CommandHandler("내정보", 내정보))
    app.run_polling()

if __name__ == "__main__":
    main()
