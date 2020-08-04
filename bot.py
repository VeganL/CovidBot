import discord, json, re
import requests as req
from random import randint
from discord.ext import commands
from googleapiclient.discovery import build

client = commands.Bot(command_prefix = 'covid!')
runFile = open("info.json", "r")
runInfo = json.loads(runFile.read().rstrip())

# Bot Globals
token = runInfo["token"]
stateCodes = runInfo["stateCodes"]

# YouTube API Globals
DEVELOPER_KEY = runInfo['youtubeApi']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

@client.command()
async def news(ctx):
	youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

	search_response = youtube.search().list(
		q='covid news',
		part='id',
		maxResults=10
	).execute()

	videos = []

	for search_result in search_response.get('items', []):
		if search_result['id']['kind'] == 'youtube#video':
			videos.append(search_result['id']['videoId'])

	pick = randint(0,len(videos) - 1)

	await ctx.send('https://www.youtube.com/watch?v=' + videos[pick])

@client.event
async def on_ready():
	print('Bot is ready')

@client.command()
async def state(ctx,*,inpState):
	rV = ''

	if inpState.upper() in stateCodes:
		toFind = stateCodes[inpState.upper()].replace(' ','%20')
	else:
		toFind = inpState.replace(' ','%20')
	
	try:
		data = json.loads(req.get('https://disease.sh/v3/covid-19/states/' + toFind + '?yesterday=false').text)
		rV += 'Covid-19 in ' + data["state"] + '\n======================\n'
		rV += 'Total Cases: ' + str(data["cases"]) + '\n'
		rV += "Today's New Cases: " + str(data["todayCases"]) + '\n'
		rV += 'Total Deaths: ' + str(data["deaths"]) + '\n'
		rV += "Today's New Deaths: " + str(data["todayDeaths"]) + '\n'
		rV += 'Tests Issued: ' + str(data["tests"]) + '\n'
		rV += 'Active Cases: ' + str(data["active"])
		await ctx.send(rV)
	except:
		await ctx.send('Could not find state data for ' + inpState)

@client.command()
async def statetop(ctx,*,sortByInp='cases'):
	rV = ''

	sortByDict = {
		'case': 'cases',
		'deaths': 'deaths',
		'death': 'deaths',
		'tests': 'tests',
		'test': 'tests',
		'active': 'active',
		'todaycases': 'todayCases',
		'todaycase': 'todayCases',
		'casestoday': 'todayCases',
		'casetoday': 'todayCases',
		'todaydeaths': 'todayDeaths',
		'todaydeath': 'todayDeaths',
		'deathstoday': 'todayDeaths',
		'deathtoday': 'todayDeaths'
		}
	
	if sortByInp != 'cases' and sortByInp.replace(' ','').lower() in sortByDict:
		sortBy = sortByDict[sortByInp.replace(' ','').lower()]
	elif sortByInp.lower() == 'cases':
		sortBy = sortByInp.lower()
	else:
		await ctx.send('Cannot sort by parameter "' + sortByInp + '"')

	data = json.loads(req.get('https://disease.sh/v3/covid-19/states?sort=' + sortBy + '&yesterday=false').text)
	rV += 'Covid-19 Top 5 States\n======================\n'
	for i in range(5):
		rV += '#' + str(i + 1) + ': ' + data[i]["state"] + '\n'
		rV += '    Total Cases: ' + str(data[i]["cases"]) + '\n'
		rV += "    Today's New Cases: " + str(data[i]["todayCases"]) + '\n'
		rV += '    Total Deaths: ' + str(data[i]["deaths"]) + '\n'
		rV += "    Today's New Deaths: " + str(data[i]["todayDeaths"]) + '\n'
		rV += '    Tests Issued: ' + str(data[i]["tests"]) + '\n'
		rV += '    Active Cases: ' + str(data[i]["active"])
		
		if i != 4:
			rV += '\n\n'

	await ctx.send(rV)

@client.command()
async def total(ctx):
	rV = 'Current Covid-19 Global Stats\n======================\n'
	data = json.loads(req.get('https://disease.sh/v3/covid-19/all?yesterday=false&allowNull=false').text)
	rV += 'Total Cases: ' + str(data["cases"]) + '\n'
	rV += 'Total Deaths: ' + str(data["deaths"]) + '\n'
	rV += 'Total Recoveries: ' + str(data["recovered"]) + '\n'
	rV += 'Active Cases: ' + str(data['active']) + '\n'
	rV += 'Critical Cases: ' + str(data['critical']) + '\n'
	rV += 'Tests Issued: ' + str(data['tests']) + '\n'
	rV += 'Countries Affected: ' + str(data['affectedCountries'])
	await ctx.send(rV)

@client.command()
async def country(ctx,*,inpNation):
	rV = ''
	inpNationOrig = inpNation
	inpNation = inpNation.replace(' ','%20')

	try:
		data = json.loads(req.get('https://disease.sh/v3/covid-19/countries/' + inpNation + '?yesterday=false&allowNull=false').text)
		rV += 'Covid-19 in ' + data["country"] + '\n======================\n'
		rV += 'Total Cases: ' + str(data["cases"]) + '\n'
		rV += "Today's New Cases: " + str(data["todayCases"]) + '\n'
		rV += 'Total Deaths: ' + str(data["deaths"]) + '\n'
		rV += "Today's New Deaths: " + str(data["todayDeaths"]) + '\n'
		rV += 'Total Recoveries: ' + str(data["recovered"]) + '\n'
		rV += 'Active Cases: ' + str(data["active"]) + '\n'
		rV += 'Critical Cases: ' + str(data["critical"]) + '\n'
		rV += 'Cases per Million: ' + str(data["casesPerOneMillion"]) + '\n'
		rV += 'Deaths per Million: ' + str(data["deathsPerOneMillion"]) + '\n'
		rV += 'Tests Issued: ' + str(data['tests'])
		await ctx.send(rV)
	except:
		await ctx.send('Could not find country data for ' + inpNationOrig)

@client.command()
async def countrytop(ctx,*,sortByInp='cases'):
	rV = ''
	
	sortByDict = {
		'case': 'cases',
		'deaths': 'deaths',
		'death': 'deaths',
		'tests': 'tests',
		'test': 'tests',
		'active': 'active',
		'todaycases': 'todayCases',
		'todaycase': 'todayCases',
		'casestoday': 'todayCases',
		'casetoday': 'todayCases',
		'todaydeaths': 'todayDeaths',
		'todaydeath': 'todayDeaths',
		'deathstoday': 'todayDeaths',
		'deathtoday': 'todayDeaths'
		}
	
	if sortByInp != 'cases' and sortByInp.replace(' ','').lower() in sortByDict:
		sortBy = sortByDict[sortByInp.replace(' ','').lower()]
	elif sortByInp.lower() == 'cases':
		sortBy = sortByInp.lower()
	else:
		await ctx.send('Cannot sort by parameter "' + sortByInp + '"')

	data = json.loads(req.get('https://disease.sh/v3/covid-19/countries?yesterday=false&sort=' + sortBy + '&allowNull=false').text)
	rV += 'Covid-19 Top 5 Countries\n======================\n'
	for i in range(5):
		rV += '#' + str(i + 1) + ': ' + data[i]["country"] + '\n'
		rV += '    Total Cases: ' + str(data[i]["cases"]) + '\n'
		rV += "    Today's New Cases: " + str(data[i]["todayCases"]) + '\n'
		rV += '    Total Deaths: ' + str(data[i]["deaths"]) + '\n'
		rV += "    Today's New Deaths: " + str(data[i]["todayDeaths"]) + '\n'
		rV += '    Tests Issued: ' + str(data[i]["tests"]) + '\n'
		rV += '    Active Cases: ' + str(data[i]["active"])
		
		if i != 4:
			rV += '\n\n'

	await ctx.send(rV)

@client.command()
async def time(ctx):
	await ctx.send("*It's Corona Time!* :sunglasses::partying_face::skull::ghost:")

client.run(token)
