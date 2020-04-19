
import os.path
import urllib.request

def processMemento(timestamp, url):
	if not os.path.exists("mementos/" + timestamp):
		print("Pulling " + timestamp, flush=True)
		f = urllib.request.urlopen(url)
		o = open("mementos/" + timestamp, "w")
		o.write(str(f.read()))
		o.close()

def main():
	print("Pulling index", flush=True)
	f = urllib.request.urlopen("http://web.archive.org/web/timemap/link/www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/current-status/current-status-and-contact-tracing-alerts")
	mementos_str = str(f.read())

	firstMemento = mementos_str.find("=\"first memento\"");
	if firstMemento == -1:
		print("Couldn't find any pages.")
		return
	
	memento = mementos_str.rfind("<", 0, firstMemento)
	while memento != -1:
		right = mementos_str.find(">", memento)
		if right == -1:
			print("Expected a >")
			return
		url = mementos_str[memento + 1:right]
		webslash = url.find("web/")
		if webslash == -1:
			print("Expected web/")
		nextslash = url.find("/", webslash + 4)
		timestamp = url[webslash + 4:nextslash]
		processMemento(timestamp, url)
		memento = mementos_str.find("<", right)

main()
