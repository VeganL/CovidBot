import time, schedule, subprocess

def getCsv():
	subprocess.call('rm rt.csv', shell=True)
	subprocess.call('wget https://d14wlfuexuxgcm.cloudfront.net/covid/rt.csv', shell=True)

schedule.every().hour.do(getCsv)

while True:
	schedule.run_pending()
	time.sleep(1)
