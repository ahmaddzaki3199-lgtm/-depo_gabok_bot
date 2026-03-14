from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime

active = False
transactions = []

def format_rupiah(n):
    return "Rp{:,.0f}".format(n).replace(",", ".")

async def mulai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active, transactions
    active = True
    transactions = []

    today = datetime.now().strftime("%d %B %Y")

    text = f"""
📅 {today}

📊 Pencatatan transaksi hari ini dimulai.
Semangat mengejar omset hari ini! 💪

━━━━━━━━━━━━

💰 Transaksi
+nominal → pemasukan
-nominal → pengeluaran

📊 Menu
/saldo → cek saldo
/riwayat → riwayat transaksi
/tutup → laporan harian
"""
    await update.message.reply_text(text)

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    income = sum(t for t in transactions if t > 0)
    expense = abs(sum(t for t in transactions if t < 0))
    balance = income - expense

    text = f"""
📊 Saldo Sementara

💰 Total pemasukan : {format_rupiah(income)}
💸 Total pengeluaran : {format_rupiah(expense)}

🏦 Saldo : {format_rupiah(balance)}
"""
    await update.message.reply_text(text)

async def riwayat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not transactions:
        await update.message.reply_text("Belum ada transaksi hari ini.")
        return

    msg = "📜 Riwayat Transaksi\n\n"

    for i,t in enumerate(transactions,1):
        if t > 0:
            msg += f"{i}. +{t}\n"
        else:
            msg += f"{i}. {t}\n"

    await update.message.reply_text(msg)

async def hapus(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not transactions:
        await update.message.reply_text("⚠️ Tidak ada transaksi yang bisa dihapus.")
        return

    last = transactions.pop()

    await update.message.reply_text(f"""
🗑 Transaksi terakhir dihapus

Transaksi:
{last}

Saldo diperbarui.
""")

async def tutup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active

    income = sum(t for t in transactions if t > 0)
    expense = abs(sum(t for t in transactions if t < 0))
    balance = income - expense

    msg = "📊 Laporan Kas Harian\n"
    msg += datetime.now().strftime("📅 %d %B %Y\n\n")

    msg += "🧾 Transaksi Hari Ini\n\n"

    for i,t in enumerate(transactions,1):
        if t > 0:
            msg += f"{i}. +{t}\n"
        else:
            msg += f"{i}. {t}\n"

    msg += "\n━━━━━━━━━━━━\n\n"

    msg += f"💰 Total pemasukan : {format_rupiah(income)}\n"
    msg += f"💸 Total pengeluaran : {format_rupiah(expense)}\n"
    msg += f"🏦 Saldo akhir : {format_rupiah(balance)}\n\n"

    msg += "✅ Pencatatan hari ini ditutup"

    active = False

    await update.message.reply_text(msg)

async def transaksi(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not active:
        return

    text = update.message.text

    try:

        if text.startswith("+"):
            value = int(text[1:])
            transactions.append(value)

            await update.message.reply_text(f"""
✅ Pemasukan dicatat
{format_rupiah(value)}
""")

        elif text.startswith("-"):
            value = int(text[1:])
            transactions.append(-value)

            await update.message.reply_text(f"""
💸 Pengeluaran dicatat
{format_rupiah(value)}
""")

        else:

            await update.message.reply_text("""
⚠️ Format transaksi tidak dikenali.

Gunakan format:
+nominal → pemasukan
-nominal → pengeluaran

Contoh:
+500000
-100000
""")

    except:
        pass

app = ApplicationBuilder().token("8765242023:AAFjnoUrJZIba-IioG9neG5HpuD7PF6Uk84").build()

app.add_handler(CommandHandler("mulai", mulai))
app.add_handler(CommandHandler("saldo", saldo))
app.add_handler(CommandHandler("riwayat", riwayat))
app.add_handler(CommandHandler("hapus", hapus))
app.add_handler(CommandHandler("tutup", tutup))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), transaksi))

app.run_polling()
