import requests
import json
import os
import time

btcRefundAddress = input("Enter a refund address for your Bitcoin: ")
xmrPayoutAddress = input("Enter your XMR Payout Address: ")
swapAmt = float(input("Enter the amount of BTC you want to swap "))



#("Creating data file...")
with open("data.json", 'r+') as f:
    f.truncate(0)
#("Cleared old data.")


#("Requesting data...")
data = requests.get('https://api.unstoppableswap.net/api/list').json()


#("Successfully fetched data.")
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
#("Data written to file successfully.")


pyList = json.loads(json.dumps(data))
pyList.sort(key=lambda x: x["price"], reverse=False)
#("Sorted data successfully.")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(pyList, f, ensure_ascii=False, indent=4)
#("New data written to file successfully.")


bestPrice = "Undefined"
ii = 0
for il in pyList:
	if pyList[ii]["testnet"] != False:
		ii=ii+1
		continue
	else:
		bestPrice = str(pyList[ii]["multiAddr"]) + "/p2p/" + str(pyList[ii]["peerId"])

clearConsole = lambda: print('\n' * 150)
clearConsole()

print("----------- CHOOSE A SWAPPER -----------")
class roman: # No longer needed as unstoppableswap doesnt use roman numerals anymore
    def int_to_Roman(self, num):
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
            ]
        syb = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
            ]
        roman_num = ''
        i = 0
        while  num > 0:
            for _ in range(num // val[i]):
                roman_num += syb[i]
                num -= val[i]
            i += 1
        return roman_num

for g in range(len(pyList)):
	#romanN = (roman().int_to_Roman(g)).lower()
	g1 = g+1
	mA = str(pyList[g]["multiAddr"])
	pr = str(pyList[g]["price"])
	minSA = str(pyList[g]["minSwapAmount"])
	maxSA = str(pyList[g]["maxSwapAmount"])
	print(f"[{g1}] peerId: {mA}  Price:{pr}  Min/Max swap amount:{minSA}/{maxSA}")

#("Swap provider input generated.")
print("The best price available is from ",bestPrice)
swapperSelection = int(input("Select a swapper by number.       [0] for best"))
if swapperSelection == 0:
	swapperSelection = bestPrice
else:
	romanN = (roman().int_to_Roman(swapperSelection)).lower()
	swapperSelection = pyList[romanN]["multiAddr"]

# buyCommand = "./swap  buy-xmr --receive-address "+xmrPayoutAddress+" --seller "+swapperSelection+" --change-address "+btcRefundAddress

cmd = """mkdir -f ~/swaptool; cd ~/swaptool;
If(!(test-path .\\swap.exe) -or !((Get-FileHash .\\swap.exe).Hash -eq "0e5d81416626cdedc0965e65bf4a3d43119ebeab5ee19776fdcf1ab03aa9efc3")) {
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls, [Net.SecurityProtocolType]::Tls11, [Net.SecurityProtocolType]::Tls12, [Net.SecurityProtocolType]::Ssl3
  [Net.ServicePointManager]::SecurityProtocol = "Tls, Tls11, Tls12, Ssl3"
  Write-Host "Downloading the latest version of the swap tool...";
  Invoke-WebRequest -Uri https://github.com/comit-network/xmr-btc-swap/releases/download/0.10.2/swap_0.10.2_Windows_x86_64.zip -OutFile ./swap.zip;
  Expand-Archive ./swap.zip -DestinationPath ./ -Force;
}
clear; Write-Host "Starting swap. This can take some time...";

""" + "./swap  buy-xmr --receive-address "+xmrPayoutAddress+" --seller "+swapperSelection+" --change-address "+btcRefundAddress

f = open("AtomicSwap.ps1", "a")
f.write(cmd)
f.close()
time.sleep(2)
os.startfile('AtomicSwap.ps1')