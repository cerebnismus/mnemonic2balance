#!/usr/local/bin/ python3
# -*- coding: utf-8 -*-

# A command-line tool that derived addresses from a given mnemonic
# Run this script with python3 webSrapping_01.py mnemonic

# oguzhan.ince@protonmail.com
# github.com/cerebnismus
# 2022-11-09

from bs4 import BeautifulSoup
from mnemonic import Mnemonic
import bip32utils
import requests
import web3

from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
# from hdwallet.utils import generate_mnemonic
from hdwallet.utils import is_mnemonic
from typing import Optional

import unicodedata
import sys

print("\n\t  Mnemonic Code Converter")
print("\t\-------------------------/\n")

mnemon = " ".join(sys.argv[1:])
# print ("mnemonic: ", mnemon) # for debugging

# use bydefault mnemonic for testing
# mnemon = "draft test oppose often any away luxury federal vast captain leg sustain"

# generate english mnemonic words for testing
# MNEMONIC: str = generate_mnemonic(language="english", strength=128)

MNEMONIC: str = mnemon
language = "english"

# Secret passphrase/password for mnemonic
PASSPHRASE: Optional[str] = None  # "meherett"

# Initialize Ethereum mainnet BIP44HDWallet
bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
# Get Ethereum BIP44HDWallet from mnemonic
bip44_hdwallet.from_mnemonic(
		mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
)

if not is_mnemonic(mnemonic=mnemon, language=language):
	print("\tInvalid mnemonic words...\n")
else:
	print("\tMnemonic Validation passed !\n")
	mnemonic = mnemon
	print("\tMnemonic: ", mnemonic)
	seed = Mnemonic("english").to_seed(mnemonic)
	print("\tBIP39 Seed : " + seed.hex() + "\n")

	# new code 
	#mnemon = Mnemonic('english')
	#seed = mnemon.to_seed(b'draft test oppose often any away luxury federal vast captain leg sustain')
	#print(f'\tBIP39 Seed Method 2: {seed.hex()}\n')

	root_key = bip32utils.BIP32Key.fromEntropy(seed)

	root_fingerprint = root_key.Fingerprint()
	root_identifier = root_key.Identifier()
	root_chaincode = root_key.ChainCode()
	print(f'\tMain Fingerprint : {root_fingerprint.hex()}')
	print(f'\tMain Identifier  : {root_identifier.hex()}')
	print(f'\tMain Chaincode   : {root_chaincode.hex()}')

	root_address = root_key.Address()
	root_public_hex = root_key.PublicKey().hex()
	root_private_wif = root_key.WalletImportFormat()
	root_private_key = root_key.PrivateKey().hex()
	print(f'\tMain Address     : {root_address}')
	print(f'\tMain Public      : {root_public_hex}')
	print(f'\tMain Private wif : {root_private_wif}')
	print(f'\tMain Private key : {root_private_key}\n')

	extended_private_key = root_key.ExtendedKey()
	root_extended_priv_true = root_key.ExtendedKey(private=True, encoded=True)
	root_extended_priv_false = root_key.ExtendedKey(private=False, encoded=True)

	print(f'\tRoot Private Key : {root_key.ExtendedKey()}')
	print(f'\tRoot Extended Private Key : {root_extended_priv_true}')
	print(f'\tRoot Extended Public Key : {root_extended_priv_false}\n')

	# COIN_TYPE = 0 for Bitcoin
	account_key_btc = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN)
	print(f'\tBTC Account Extended Private Key : {account_key_btc.ExtendedKey()}')
	print(f'\tBTC Account Extended Public Key : {account_key_btc.ExtendedKey(private=False)}\n')

	bip32_key_btc = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0)
	print(f'\tBTC BIP32 Extended Private Key : {bip32_key_btc.ExtendedKey()}')
	print(f'\tBTC BIP32 Extended Public Key  : {bip32_key_btc.ExtendedKey(private=False)}\n')

	i = 0
	while True: # BTC
		# Derived Addresses from bip32_derivation_path
		bip32_path = "m/44'/0'/0'/0/" + str(i)
		bip32_address = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(i).Address()
		bip32_public_hex = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(i).PublicKey().hex()
		bip32_private_wif = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(i).WalletImportFormat()
		bip32_private_key = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(i).PrivateKey().hex()
		print(f'\tBTC BIP32 Derivation Path : {bip32_path}')
		print(f'\tBTC BIP32 Address         : {bip32_address}')
		print(f'\tBTC BIP32 Public          : {bip32_public_hex}')
		print(f'\tBTC BIP32 Private wif     : {bip32_private_wif}')
		print(f'\tBTC BIP32 Private key     : {bip32_private_key}')
		i += 1

		if i == 1:
			break

	url = "https://blockchain.info/q/addressbalance/" + bip32_address
	response = requests.get(url)
	html_index = response.content
	soup = BeautifulSoup(html_index, "html.parser")
	# print(soup.prettify())

	print("\tBTC Balance: " + soup.get_text())
	print("\n")

	# COIN_TYPE = 60 for ETH
	account_key_bsc = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(60 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN)
	print(f'\tBSC Account Extended Private Key : {account_key_bsc.ExtendedKey()}')
	print(f'\tBSC Account Extended Public Key : {account_key_bsc.ExtendedKey(private=False)}\n')

	bip32_key_bsc = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(60 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0)
	print(f'\tBSC BIP32 Extended Private Key : {bip32_key_bsc.ExtendedKey()}')
	print(f'\tBSC BIP32 Extended Public Key  : {bip32_key_bsc.ExtendedKey(private=False)}\n')

	i = 0
	while True: # ETH
		
		# get derived addresses for ETH
		bip32_path_eth = "m/44'/60'/0'/0/" + str(i)
		bip32_address_eth = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(60 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(i).Address()
		bip32_public_hex_eth = "0x" + root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(60 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(i).PublicKey().hex()
		bip32_private_wif_eth = "0x" + root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(60 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(i).WalletImportFormat()
		bip32_private_key_eth = "0x" + root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(60 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(i).PrivateKey().hex()
		print(f'\tBSC BIP32 Derivation Path : {bip32_path_eth}')
		print(f'\tBSC BIP32 Address         : {bip32_address_eth}')
		print(f'\tBSC BIP32 Public          : {bip32_public_hex_eth}')
		print(f'\tBSC BIP32 Private wif     : {bip32_private_wif_eth}')
		print(f'\tBSC BIP32 Private key     : {bip32_private_key_eth}\n')
		i += 1

		if i == 1:
			break

	# Clean default BIP44 derivation indexes/paths
	bip44_hdwallet.clean_derivation()

	# print("Mnemonic:", bip44_hdwallet.mnemonic())
	# print("Base HD Path:  m/44'/60'/0'/0/{address_index}", "\n")

	# Get Ethereum bip44_hdwallet information's from address index
	for address_index in range(1):
			# Derivation from Ethereum BIP44 derivation path
			bip44_derivation: BIP44Derivation = BIP44Derivation(
					cryptocurrency=EthereumMainnet, account=0, change=False, address=address_index
			)
			# Drive Ethereum bip44_hdwallet
			bip44_hdwallet.from_path(path=bip44_derivation)
			# Print address_index, path, address and private_key
			# print(f"({address_index}) {bip44_hdwallet.path()} {bip44_hdwallet.address()} 0x{bip44_hdwallet.private_key()}")
			print(f"\tBSC BIP32 Wallet Address  : {bip44_hdwallet.address()}")
			
			# Clean derivation indexes/paths
			bip44_hdwallet.clean_derivation()

	url = "https://api.bscscan.com/api?module=account&action=balance&address=" + bip44_hdwallet.address() + "&apikey=5PP7JJGQZHHRZUXC6NDCQ8QTAMH795WYQC"
	response = requests.get(url)
	html_index = response.content
	soup = BeautifulSoup(html_index, "html.parser")

	import json

	# get result value from json
	result = json.loads(soup.get_text())
	print("\tBSC Balance: " + result['result'])

	# print("\tBSC Balance: " + soup.get_text())
	print("\n")
