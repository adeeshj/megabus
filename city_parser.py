import csv

FILENAME = "city_codes.csv"

def city_to_code(cityName):
	with open(FILENAME, 'r') as csvFile:
		r = csv.reader(csvFile)
		for city, code in r:
			if city == cityName:
				return int(code)

		# city not found
		raise KeyError("{} not found.".format(cityName))


def code_to_city(cityCode):
	with open(FILENAME, 'r') as csvFile:
		r = csv.reader(csvFile)
		for city, code in r:
			if int(code) == cityCode:
				return city

		# code not found
		raise KeyError("{} not found.".format(cityCode))


if __name__ == '__main__':
	print city_to_code("Austin")
	print code_to_city(319)
