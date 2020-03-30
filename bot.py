import discord, json, re
import requests as req
from discord.ext import commands

client = commands.Bot(command_prefix = 'covid!')
runFile = open("info.json", "r")
runInfo = json.loads(runFile.read().rstrip())

token = runInfo["token"]
stateCodes = runInfo["stateCodes"]

@client.event
async def on_ready():
	print('Bot is ready')

@client.command()
async def state(ctx,*,inpState):
	rV = ''
	stateData = {}

	if inpState.upper() in stateCodes:
		toFind = stateCodes[inpState.upper()]
	else:
		toFind = inpState
	
	data = json.loads(req.get('https://corona.lmao.ninja/states').text)
	for state in data:
		if state["state"].lower() == toFind.lower():
			stateData = state
	
	if stateData == {}:
		await ctx.send('Could not find state data for ' + inpState)
	else:
		rV += 'Covid-19 in ' + stateData["state"] + '\n======================\n'
		rV += 'Total Cases: ' + str(stateData["cases"]) + '\n'
		rV += "Today's New Cases: " + str(stateData["todayCases"]) + '\n'
		rV += 'Total Deaths: ' + str(stateData["deaths"]) + '\n'
		rV += "Today's New Deaths: " + str(stateData["todayDeaths"]) + '\n'
		rV += 'Active Cases: ' + str(stateData["active"])
		await ctx.send(rV)

@client.command()
async def total(ctx):
	rV = 'Current Covid-19 Global Stats\n======================\n'
	data = json.loads(req.get('https://corona.lmao.ninja/all').text)
	rV += 'Total Cases: ' + str(data["cases"]) + '\n'
	rV += 'Total Deaths: ' + str(data["deaths"]) + '\n'
	rV += 'Total Recoveries: ' + str(data["recovered"])
	await ctx.send(rV)

@client.command()
async def country(ctx,*,inpNation):
	rV = ''
	inpNationOrig = inpNation
	inpNation = inpNation.replace(' ','%20')

	try:
		data = json.loads(req.get('https://corona.lmao.ninja/countries/' + inpNation).text)
		rV += 'Covid-19 in ' + data["country"] + '\n======================\n'
		rV += 'Total Cases: ' + str(data["cases"]) + '\n'
		rV += "Today's New Cases: " + str(data["todayCases"]) + '\n'
		rV += 'Total Deaths: ' + str(data["deaths"]) + '\n'
		rV += "Today's New Deaths: " + str(data["todayDeaths"]) + '\n'
		rV += 'Total Recoveries: ' + str(data["recovered"]) + '\n'
		rV += 'Active Cases: ' + str(data["active"]) + '\n'
		rV += 'Critical Cases: ' + str(data["critical"]) + '\n'
		rV += 'Cases per Million: ' + str(data["casesPerOneMillion"]) + '\n'
		rV += 'Deaths per Million: ' + str(data["deathsPerOneMillion"])
		await ctx.send(rV)
	except:
		await ctx.send('Could not find country data for ' + inpNationOrig)

@client.command()
async def time(ctx):
	await ctx.send("*It's Corona Time!* :sunglasses::partying_face::skull::ghost:")

client.run(token)
