import glob
import datetime
import calendar

def get_last_updated(data):
	p_last_updated = data.find("<p>Last updated: ")
	if p_last_updated != -1:
		end_p = data.find("</p>", p_last_updated)
		last_updated = data[p_last_updated + len("<p>Last updated: "):end_p]
		last_updated = last_updated.replace("Midday ", "")
		return last_updated
	return "null"

def pull_from_td(data, start):
	td = data.find("<td>", start)
	end_td = data.find("</td>", td)
	return data[td+len("<td>"):end_td]

def pull_field(data, header):
	th = data.find("<th>" + header + "</th>")
	if th != -1:
		return pull_from_td(data, th)
	return "null"

def process(timestamp, data):
	last_updated = get_last_updated(data)
	active_cases = pull_field(data, "Active cases")
	current_hospitalisations = pull_field(data, "Current hospitalisations")
	in_icu = pull_field(data, "Patients currently in ICU")
	deaths = pull_field(data, "Deaths")
	print(last_updated + ", " + active_cases + ", " + current_hospitalisations + ", " + in_icu + ", " + deaths)

def main():
	all_timestamps = []
	for filename in glob.glob("stats/*"):
		timestamp = filename[filename.find("\\") + 1:]
		all_timestamps.append(timestamp)

	timestamps = []
	for i in range(0, len(all_timestamps)):
		timestamp = all_timestamps[i]
		if i == len(all_timestamps) - 1:
			timestamps.append(timestamp)
		elif timestamp[:8] != all_timestamps[i+1][:8]:
			timestamps.append(timestamp)

	for timestamp in timestamps:
		f = open("stats/" + timestamp, "r")	
		data = str(f.read());
		f.close()

		process(timestamp, data)

main()
