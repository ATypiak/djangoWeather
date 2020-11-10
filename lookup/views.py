from django.shortcuts import render

def home(request):
	import json
	import requests

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
			category_loop.append(key.rstrip('IndexLevel')+': '+api[key]['indexLevelName'])
			# print(category_loop)
			# return render(request, 'home.html',{'category_loop':category_loop})
	return render(request, 'home.html',{'api':api,
		'category_loop':category_loop})

def about(request):
	return render(request, 'about.html',{})	
