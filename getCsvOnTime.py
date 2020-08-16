import time, schedule, subprocess

def getCsv():
	subprocess.call('wget https://d14wlfuexuxgcm.cloudfront.net/covid/rt.csv', shell=True)
	subprocess.call('rm rt.csv && mv rt.csv.1 rt.csv', shell=True)

schedule.every().hour.do(getCsv)

while True:
	schedule.run_pending()
	time.sleep(1)
