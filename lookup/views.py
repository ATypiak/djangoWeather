from django.shortcuts import render

QUEALITY_DICT={
'Bardzo dobry':'verygood',
'Dobry':'good',
'Umiarkowany':'moderate',
'Dostateczny':'usg',
'Zły':'bad',
'Bardzo zły':'terrible',
}
CITIES={}
stations={}

def home(request):
	import json
	import requests

	global CITIES,stations
	# CITIES={}
	# stations={}

	if len(CITIES)==0:
		all_stations=requests.get("http://api.gios.gov.pl/pjp-api/rest/station/findAll")
		# try:
		api_all_stations = json.loads(all_stations.content)
		
		for i in api_all_stations:
			id=i['id']
			stationName=i['stationName']
			city=i['city']['name']
			address=i['addressStreet']
			lat=i['gegrLat']
			lon=i['gegrLon']
			if city not in stations:
				stations[city]=[]
			stations[city].append((city,id,stationName,address))	
		CITIES=list(stations.keys())
		CITIES.sort()
	# print(CITIES)
	# except Exception as e:
		# api_all_stations = "Error.."

	if request.method == "POST":
		city = request.POST['city']
		city_stations=stations[city]
		return render(request, 'home.html',{'city':city_stations,
											'cities_names':CITIES})
	else:
		

		# api_requests=requests.get("http://api.gios.gov.pl/pjp-api/rest/station/findAll")
		api_requests=requests.get("http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/10955")
		
		#http://api.gios.gov.pl/pjp-api/rest/station/findAll
		try:
			api = json.loads(api_requests.content)
		except Exception as e:
			api = "Error.."
	
		category_loop=[]
		for key in api:
			if type(api[key])==dict:
				if key=='stIndexLevel':
					category_color=QUEALITY_DICT[api[key]['indexLevelName']]
				category_loop.append(key.rstrip('IndexLevel')+': '+api[key]['indexLevelName'])
				# print(category_loop)
				# return render(request, 'home.html',{'category_loop':category_loop})
		return render(request, 'home.html',{'api':api,
			'category_loop':category_loop, 
			'category_color':category_color,
			'stations':stations,
			'cities_names':CITIES})

def about(request):
	return render(request, 'about.html',{'cities_names':CITIES})	
