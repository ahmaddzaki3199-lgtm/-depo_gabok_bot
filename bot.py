import telebot
from datetime import datetime

TOKEN = "TOKEN_BOT_KAMU"

bot = telebot.TeleBot(TOKEN)

total_pemasukan = 0
total_pengeluaran = 0
transaksi = []
aktif = False


def rupiah(angka):
    return "Rp{:,.0f}".format(angka).replace(",", ".")


@bot.message_handler(commands=['mulai'])
def mulai(message):
    global aktif, total_pemasukan, total_pengeluaran, transaksi

    if message.chat.type not in ['group', 'supergroup']:
        return

    aktif = True
    total_pemasukan = 0
    total_pengeluaran = 0
    transaksi = []

    tanggal = datetime.now().strftime("%d %B %Y")

    bot.reply_to(message,
f"""{tanggal}
Pencatatan transaksi hari ini dimulai.

Semangat mengejar omset hari ini 💪

Format transaksi:
+500000 = pemasukan
-200000 = pengeluaran

Perintah:
/saldo
/riwayat
/tutup
""")


@bot.message_handler(commands=['saldo'])
def saldo(message):
    saldo = total_pemasukan - total_pengeluaran

    bot.reply_to(message,
f"""📊 Saldo Sementara

💰 Total pemasukan : {rupiah(total_pemasukan)}
💸 Total pengeluaran : {rupiah(total_pengeluaran)}

🏦 Saldo : {rupiah(saldo)}
""")


@bot.message_handler(commands=['riwayat'])
def riwayat(message):
    if not transaksi:
        bot.reply_to(message, "Belum ada transaksi hari ini.")
        return

    teks = "🧾 Transaksi Hari Ini\n\n"

    for i, t in enumerate(transaksi, start=1):
        teks += f"{i}. {t}\n"

    bot.reply_to(message, teks)


@bot.message_handler(commands=['tutup'])
def tutup(message):
    global aktif

    if not aktif:
        return

    saldo = total_pemasukan - total_pengeluaran
    tanggal = datetime.now().strftime("%d %B %Y")

    teks = f"""📊 Laporan Kas Harian
📅 {tanggal}

🧾 Transaksi Hari Ini

"""

    for i, t in enumerate(transaksi, start=1):
        teks += f"{i}. {t}\n"

    teks += f"""
━━━━━━━━━━━━

💰 Total pemasukan : {rupiah(total_pemasukan)}
💸 Total pengeluaran : {rupiah(total_pengeluaran)}
🏦 Saldo akhir : {rupiah(saldo)}

✅ Pencatatan hari ini ditutup
"""

    bot.reply_to(message, teks)

    aktif = False


@bot.message_handler(func=lambda message: True)
def transaksi_handler(message):
    global total_pemasukan, total_pengeluaran

    if not aktif:
        return

    text = message.text.replace(".", "").replace("Rp", "")

    if text.startswith("+"):
        jumlah = int(text[1:])
        total_pemasukan += jumlah
        transaksi.append(f"+{rupiah(jumlah)[2:]}")

        saldo = total_pemasukan - total_pengeluaran

        bot.reply_to(message,
f"""✅ Pemasukan dicatat
{rupiah(jumlah)}

💰 Total pemasukan saat ini
{rupiah(saldo)}
""")


    elif text.startswith("-"):
        jumlah = int(text[1:])
        total_pengeluaran += jumlah
        transaksi.append(f"-{rupiah(jumlah)[2:]}")

        saldo = total_pemasukan - total_pengeluaran

        bot.reply_to(message,
f"""💸 Pengeluaran dicatat
{rupiah(jumlah)}

💰 Total pemasukan saat ini
{rupiah(saldo)}
""")


print("Bot berjalan...")
bot.infinity_polling()
