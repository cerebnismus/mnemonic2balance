#!/usr/local/bin/ python3
# -*- coding: utf-8 -*-

# oguzhan.ince@protonmail.com
# github.com/cerebnismus
# 2022-11-11

# database
import psycopg2
import sys, os, time

conn = psycopg2.connect(
		host="localhost",
		database="postgres",
		user="postgres")

# connect to database
cur = conn.cursor()


def check_btc():

  # Read data from file
  datafile = open('databtc.txt', 'r')

  # compare lines in datafile for btc
  for line in datafile:
    line = line.strip()
    query = "SELECT mnemonics, addressbtc FROM public.mnemonic2balance WHERE addressbtc like '%" + line + "%'"
    cur.execute(query)
    rows = cur.fetchall()
    print(rows)
    for row in rows: 
      if row[0] not in open('databtc_found.txt').read():
        with open('databtc_found.txt', 'a') as f:
          f.write(row[0] + ' ' + row[1])
          f.close()

def check_bsc():
  
  # Read data from file
  datafile2 = open('databsc.txt', 'r')

  # compare lines in datafile for bsc
  for line in datafile2:
    line = line.strip()
    query = "SELECT mnemonics, addressbsc FROM public.mnemonic2balance WHERE addressbsc like '%" + line + "%'"
    cur.execute(query)
    rows = cur.fetchall()
    print(rows)
    for row in rows:
      if row[0] not in open('databsc_found.txt').read():
        with open('databsc_found.txt', 'a') as f:
          f.write(row[0] + ' ' + row[1])
          f.close()
  
  
#define a main function
def main():
  check_btc()
  check_bsc()
  
  # print databtc_found.txt and databsc_found.txt
  print(open('databtc_found.txt').read())
  print(open('databsc_found.txt').read())

  
  
#run the main function
if __name__ == "__main__":
  main()
