#!/usr/bin/python3

from bs4 import BeautifulSoup as bs
import requests
import getpass

subdomain = input("SchoolLoop subdomain (mvhs): ")
username = input("Username: ")
password = getpass.getpass()

args = []

args.append(subdomain)
args.append(username)
args.append(password)

r1 = requests.get(("https://" + args[0] + ".schoolloop.com/portal/guest_home?d=x"))
s1 = bs(r1.text, "html.parser")

form_data_id = s1.find("input", {"id": "form_data_id"})["value"]
cookies_sent = {"JSESSIONID": r1.cookies["JSESSIONID"], "slid": r1.cookies["slid"]}
payload = {"login_name": args[1], 'password': args[2], 'event_override': 'login', 'form_data_id': form_data_id}

r2 = requests.post(("https://" + args[0] + ".schoolloop.com/portal/guest_home?etarget=login_form"), cookies=cookies_sent, data=payload)
s2 = bs(r2.text, "html.parser")

grades = []

for row in s2.find_all("table", {"class": "student_row"}):

	class_name = str(row.find("td", {"class": "course"}).a.text)
	teacher_name = str(row.find("td", {"class": "teacher co-teacher"}).a.text).strip().split(", ")[1] + " " + str(row.find("td", {"class": "teacher co-teacher"}).a.text).strip().split(", ")[0]

	try:
		grade = float(row.find("div", {"class": "percent"}).text.replace("%", ""))
	except AttributeError:
		grade = "No Grades Published"

	grades.append([class_name, teacher_name, grade])

print(grades)
