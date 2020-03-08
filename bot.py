#!/usr/bin/env python3
# Jus de Patate_ - Telegram Monitoring Bot (github:jusdepatate/telegram-monitoring-bot) - 2020
# Telegram bot that gives informations on server

import telebot
import psutil
import time

TOKEN = ""

bot = telebot.TeleBot(TOKEN)
# login


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "If you don't know what this bot does, it's maybe not made for you")
	# eheh


@bot.message_handler(commands=['status'])
def send_welcome(message):
	ram = str(round(getattr(psutil.virtual_memory(), 'used') / getattr(psutil.virtual_memory(), 'total') * 100))
	cpu = str(round(psutil.cpu_percent(interval=None, percpu=False) * 10))
	disk = str(round(psutil.disk_usage(psutil.disk_partitions()[0].mountpoint).percent))

	sent = time.monotonic()
	msg = bot.reply_to(message, "Ping-pong!")
	ping = (time.monotonic() - sent) * 1000
	ping = int(ping)

	bot.edit_message_text(
		"Ping: " + str(ping) + "ms\n"
		"RAM: " + ram + "%\n"
		"CPU: " + cpu + "% (/cpu for more)\n"
		"Disk: " + disk + "% (/disk for more)",
		message_id=msg.message_id, chat_id=msg.chat.id)
	# here we send a message, then edit it to get """"ping""""
	# we also give RAM/CPU/Disk (first partition) usage from psutil


@bot.message_handler(commands=['cpu'])
def cpu_usage(message):
	i = 0
	msg = ""
	while True:
		try:
			cpup = psutil.cpu_percent(percpu=True)

			msg += "CPU "+str(i+1)+": "+str(cpup[i] * 10)+"\n"
			i += 1
		except IndexError:
			break
	bot.reply_to(message, msg)
	# Gives CPU usage per cores


@bot.message_handler(commands=['disk'])
def disk_usage(message):
	partitions = psutil.disk_partitions()
	fmt = "{}\t{}\t{}\t{}%\n"
	msg = fmt.format("Disk", "Fs", "Mountpoint", "Av.Space in ")
	# Only show a couple of different types of devices, for brevity.
	i = 0
	while True:
		try:
			partition = partitions[i]
			if partition.fstype == "squashfs":
				i += 1
				# ignore squashfs
			else:
				msg += fmt.format(partition.device, partition.fstype, partition.mountpoint, psutil.disk_usage(partition.mountpoint).percent)
				# add drive (usually starts by '/dev/'), filesystem, mountpoint and disk usage in %
				i += 1
		except IndexError:
			break
	# i know you hate that way to do <3
	bot.reply_to(message, msg)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, "Unknown command")


bot.polling()
