import requests
import os
import json
import sys

from code import *

law_us = []
out_us = []
ren_us = []
win = ""
alive_us = []

data = load_raw()
data = data["players"]

count = 1
print("\n\nAvailable Players\n-1 No one")
for user in data:
	print(str(count) + " " + user["name"])
	count += 1
print("\n")

law = input('Who were the law enforcers?\n')
law = law.split(" ")
for i in law:
	if i != '' and int(i) > 0 and int(i) < len(data):
		law_us.append(data[int(i)-1]["name"])

out = input('Who were the outlaws?\n')
out = out.split(" ")

for i in out:
	if i != '' and int(i) > 0 and int(i) < len(data):
		out_us.append(data[int(i)-1]["name"])


ren = input('Who was the rendegade?\n')
ren = ren.split(" ")
if ren[0] != '-1':
	for i in ren:
		if i != '' and int(i) > 0 and int(i) < len(data):
			ren_us.append(data[int(i)-1]["name"])

victory = input('Who won the game?\n(law=1 - outlaw=2 - rendegade=3)\n')
if int(victory) ==1:
	victory="law"
elif int(victory) ==2:
	victory="out"
elif int(victory) ==3:
	victory="ren"
else:
	print("Error. Aborting.")
	sys.exit()

alive = input('Who was still alive at the end of the match?\n')
alive = alive.split(" ")
for i in alive:
	if i != '' and int(i) > 0 and int(i) < len(data):
		alive_us.append(data[int(i)-1]["name"])

print("Updating values with:")
print("\nLaw enforcers:")
print(law_us)
print("Outlaws:")
print(law_us)
print("Renegade:")
print(law_us)
print("\nVictory:")
print(victory)
print("Still alive:")
print(alive_us)

confirm = input("\nConfirm? [y/N]")
if confirm != 'y' or confirm != 'Y':
	access_token = str(os.environ.get('ACCESS_TOKEN'))
	params = {
		"code":access_token, 
		"match": {
			"law": law_us,
			"out": out_us,
			"ren": ren_us,
			"win": victory,
			"alive": alive_us
		}
	}

	r = requests.post('https://vrselo.herokuapp.com/update/', json=params)
	print(r)