import glob
import datetime
import calendar

previous_total = None

def process(timestamp, data):
	confirmed_cases = data.find("confirmed cases")
	if confirmed_cases == -1:
		print(timestamp + " no data");
		return
	p = data.rfind("<p", 0, confirmed_cases)
	pe = data.find(">", p)
	endp = data.find("</p>", pe)
	summary = data[pe+1:endp]

	words = summary.split()

	global previous_total
	nums = []
	for word in words:
		if word[-1] == '.' or word[-1] == ",":
			word = word[0:-1]
		if word.isnumeric():
			nums.append(word)
	if len(nums) == 0:
		if "no new confirmed cases" in summary:
			total = previous_total
		else:
			total = summary
	else:
		total = nums[-1]
	previous_total = total

	th = data.find("table59454r1c2")
	if th == -1:
		total_samples_tested = data.find("Total samples tested")
		if total_samples_tested == -1:
			testing = "null"
		else:
			endp = data.find("</p>", total_samples_tested)
			testing = data[total_samples_tested + len("Total samples tested:"):endp]
	else:
		td = data.find("table59454r1c2", th + 1)
		etd = data.find(">", td)
		endtd = data.find("</td>", etd)
		testing = data[etd+1:endtd]
		
	testing = testing.replace("<b>","")
	testing = testing.replace("</b>","")
	testing = testing.replace("<strong>","")
	testing = testing.replace("</strong>","")
	testing = testing.replace(",","")
	testing = testing.strip()
	if testing.find("\\xe2") != -1:
		testing = testing[0:testing.find("\\xe2")]

	month = calendar.month_name[int(timestamp[4:6])][:3]
	day = int(timestamp[6:8])
	print("\"" + month + " " + str(day) + "\", " + str(total) + ", " + str(testing))

def main():
	all_timestamps = []
	for filename in glob.glob("mementos/*"):
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
		f = open("mementos/" + timestamp, "r")	
		data = str(f.read());
		f.close()

		process(timestamp, data)

main()
