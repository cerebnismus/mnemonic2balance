# A command-line tool that derived addresses from a given mnemonic
# Run this script with python3 main.py mnemonic

# oguzhan.ince@protonmail.com
# github.com/cerebnismus
# 2022-11-09
# 
# adding multithreading to the script to speed up the process
# 2021-11-14

import subprocess, threading
from time import sleep
from datetime import datetime
from hdwallet.utils import generate_mnemonic

def generate_main():

    mnemon = generate_mnemonic()
    try:
        subprocess.check_output(["python", "main.py", mnemon]) #, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(e.output)

def threadz():
    th=threading.Thread(target=generate_main,args=())
    th.start()

if __name__ == "__main__":
    
    print("\n\t  m2b is running...\n")
    print("    ", datetime.now())
    
    for j in range(1000000):
        for i in range(3):
            threadz()
            sleep(1)
    
    # wait for threads to finish
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()