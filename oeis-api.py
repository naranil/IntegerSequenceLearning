import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

sequence = "1,3,13,87,1053,28576,2141733,508147108,402135275365,1073376057490373,9700385489355970183,298434346895322960005291,31479360095907908092817694945"

def find_oeis_number(sequence):
	sequence_array = sequence.split(',')

	oeis_url = "https://oeis.org/"
	request_url = oeis_url + 'search?q=' + '%2C'.join(sequence.split(','))

	response = requests.get(request_url)

	if response.status_code != 200:
		raise Exception("Can't access the website")

	soup = BeautifulSoup(response.text, 'html.parser')
	new_sequence = soup.find('tt').text
	new_sequence_array = new_sequence.split(", ")
	remainings = [integer for integer in new_sequence_array if integer not in sequence_array]
	result = remainings[0]

	return result

train = pd.read_csv("./data/train.csv")
small_train = train.sample(1000, random_state=0)

for i in range(small_train.shape[0]):
	full_sequence = small_train['Sequence'].iloc[i]
	sequence_array = full_sequence.split(',')
	sequence = ",".join(sequence_array[:-1])
	last_number = sequence_array[-1]
	try:
		oeis_number = find_oeis_number(sequence)
	except Exception:
		print "Didn't find OEIS for id: {0}".format(small_train['Id'].iloc[i])
		pass

	if oeis_number != last_number:
		print "Wrong OEIS for id: {0}".format(small_train['Id'].iloc[i])
	time.sleep(2)