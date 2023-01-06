#!/usr/local/bin/ python3
# -*- coding: utf-8 -*-

# A command-line tool that derived addresses from a given mnemonic
# Run this script with python3 main.py mnemonic

# oguzhan.ince@protonmail.com
# github.com/cerebnismus
# 2022-11-11

import psycopg2
import sys, os, time

conn = psycopg2.connect(
		host="localhost",
		database="postgres",
		user="router",
		password="r0ut3r")

# connect to database
cur = conn.cursor()


# while True: clear and run every 5 seconds
while True:

	# clear screen
	os.system('clear')

	print("\n\t    Mnemonic Dashboard")
	print("\t  \---------------------/\n")

	totalbtc = 0
	totalbsc = 0
	cur.execute("SELECT balancebtc FROM public.mnemonic2balance")
	rows = cur.fetchall()
	for row in rows:
		# tuple to int converter
		totalbtc += float(row[0])


	cur.execute("SELECT balancebsc FROM public.mnemonic2balance")
	rows = cur.fetchall()
	for row in rows:
		totalbsc += float(row[0])

	# Print total btc balance and total bsc balance in one line
	print("\tTotal BTC: ", totalbtc, " Total BSC: ", totalbsc, "\n")

	cur.execute("SELECT count(*) FROM public.mnemonic2balance HAVING count(*) > 1")
	rows = cur.fetchall()
	for row in rows:
		print("\tMnemonic Counter: ", row[0])


	# run every 5 seconds
	time.sleep(3)

	# if user press ctrl+c then break the loop
	try:
		pass
	except KeyboardInterrupt:
		break

# close the communication with the PostgreSQL
cur.close()
conn.close()
# exit successfully
sys.exit(0)
