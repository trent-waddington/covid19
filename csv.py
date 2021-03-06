import glob
import datetime
import calendar

previous_total = None

def process(timestamp, data):
	class_cases = data.find("class=\"cases\"")
	if class_cases == -1:
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
	else:
		dive = data.find(">", class_cases)	
		endspan = data.find("</span>", dive)
		cases = data[dive+1:endspan]
		cases = cases.replace("<span>", "")
		cases = cases.replace(",", "")
		total = cases

	th = data.find("table59454r1c2")
	total_samples_tested = data.find("Total samples tested")
	if th != -1:
		td = data.find("table59454r1c2", th + 1)
		etd = data.find(">", td)
		endtd = data.find("</td>", etd)
		testing = data[etd+1:endtd]
			
	elif total_samples_tested != -1:
		endp = data.find("</p>", total_samples_tested)
		testing = data[total_samples_tested + len("Total samples tested:"):endp]
	else:
		class_tested = data.find("class=\"tested\"")
		if class_tested == -1:
			testing = "no data"
		else:
			dive = data.find(">", class_tested)
			endspan = data.find("</span>", dive)
			tested = data[dive+1:endspan]
			tested = tested.replace("<span>", "")
			testing = tested

	testing = testing.replace("<b>","")
	testing = testing.replace("</b>","")
	testing = testing.replace("<strong>","")
	testing = testing.replace("</strong>","")
	testing = testing.replace(",","")
	testing = testing.strip()
	if testing.find("\\xe2") != -1:
		testing = testing[0:testing.find("\\xe2")]

	lost = "null"
	class_lost = data.find("class=\"lost\"")
	if class_lost != -1:
		dive = data.find(">", class_lost)
		endspan = data.find("</span>", dive)
		lost = data[dive+1:endspan]
		lost = lost.replace("<span>", "")

	month = calendar.month_name[int(timestamp[4:6])][:3]
	day = int(timestamp[6:8])
	print("\"" + month + " " + str(day) + "\", " + str(total) + ", " + str(testing) + ", " + str(lost))

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
