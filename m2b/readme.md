# duplice satirlari kesfetmek icin:
SELECT mnemonics, count(*)
	FROM public.mnemonic2balance
	group by mnemonics
	HAVING count(*) > 1

# duz select sorgusu:
SELECT mnemonics, addressbtc, addressbsc, balancebtc, balancebsc
	FROM public.mnemonic2balance;

# eger internet giderse update sorgusu: