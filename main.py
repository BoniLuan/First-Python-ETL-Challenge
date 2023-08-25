import requests

# Load Brazil states list 
def get_states():
	url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
	return requests.get(url).json()

# Load cities of state
def get_cities(uf):
	url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
	return requests.get(url).json()

# Load population of city
def get_population(city):
	url = f"https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2021/variaveis/9324?localidades=N1[all]|N6[{city}]"
	return requests.get(url).json()[0]

# Seach uf in tuple of states
def search_uf(list_states, uf):
	for tuple in list_states:
		if tuple['sigla'] == uf:
			return tuple
	return {}

# Seach city name in tuple of cities
def search_city(list_cities, city_name):
	for tuple in list_cities:
		if tuple['nome'].upper() == city_name.upper():
			return tuple
	return {}

# -------------> START <------------- #
print("\n"+10*"-"+"> START <"+10*"-")

list_states = get_states()
	
FILE_NAME = "IBGE.txt"

stop = "C"
while stop != "S":
	tuple_uf = {}
	while True:
		uf = input(f"\nDigite a sigla de um estado brasileiro:\n").upper()
		tuple_uf = search_uf(list_states, uf)
		if tuple_uf:
			break

	list_cities = get_cities(tuple_uf['id'])
	tuple_city = {}
	while True:
		city_name = input(f"Digite uma cidade pertencente ao estado {uf}:\n")
		tuple_city = search_city(list_cities, city_name)
		if tuple_city:
			break

	tuple_population = get_population(tuple_city['id'])

	population_number = f"{int(tuple_population['resultados'][0]['series'][1]['serie']['2021']):,}".replace(",", ".")
	city_name = tuple_population['resultados'][0]['series'][1]['localidade']['nome']

	str_ibge = f"\n\tMunicípio: {city_name}\n\tPopulação: {population_number}\n"

	with open(FILE_NAME, "a", encoding="utf-8") as file:
		file.write(str_ibge)

	stop = input(f"\nC - Continuar\nS - Sair\n\n").upper()

print(f"\n{FILE_NAME} successfully exported!\n")
