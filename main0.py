# SchoolLoop Parser
# To become a module (schoolloop-python)

from bs4 import BeautifulSoup as bs
import requests
import getpass
import datetime
import time

args = []
dtd = False
dtt = False
duedate = ""

hw_list = []
grades = []

def get_data(subdomain, username, password):
  global args

  print("")

  args.append(subdomain)
  args.append(username)
  args.append(password)

  r1 = requests.get(("https://" + args[0] + ".schoolloop.com/portal/guest_home?d=x"))
  s1 = bs(r1.text, "html.parser")

  form_data_id = s1.find("input", {"id": "form_data_id"})["value"]
  cookies_sent = {"JSESSIONID": r1.cookies["JSESSIONID"], "slid": r1.cookies["slid"]}
  payload = {"login_name": args[1], 'password': args[2], 'event_override': 'login', 'form_data_id': form_data_id}

  r2 = requests.post(("https://" + args[0] + ".schoolloop.com/portal/guest_home?etarget=login_form"), cookies=cookies_sent, data=payload)
  #s2 = bs(r2.text, "html.parser")
  return bs(r2.text, "html.parser")

def get_grades():
  global grades, s2
  for row in s2.find_all("table", {"class": "student_row"}):
    period = int(row.find("td", {"class":"period"}).string)
    class_name = str(row.find("td", {"class": "course"}).a.text)
    
    # Gets teachers
    teacher_name = str(row.find("td", {"class": "teacher co-teacher"}).a.text).strip().split(", ")[1] + " " + str(row.find("td", {"class": "teacher co-teacher"}).a.text).strip().split(", ")[0]

    try:
      grade = float(row.find("div", {"class": "percent"}).text.replace("%", ""))
    except AttributeError:
      grade = "No grades published by teacher"

    grades.append([period, class_name, teacher_name, grade])

def get_homework():
  global hw_list, s2
  for hw in s2.find_all("table", {"class":"table_basic"}):
    hw_assignment = str(hw.find("td", {"class":"column padding_5 item_title"}).span.string).strip()
    hw_class = str(hw.find("td", {"class":"column padding_5"}).string).strip()

    hw_duedate = str(hw.find_all("td", {"class":"column padding_5 no_wrap"})[int(len(hw.find_all("td", {"class":"column padding_5 no_wrap"})))-1].string).strip()[5:]
    hw_dd = datetime.date(int(datetime.datetime.now().year), int(hw_duedate.split("/")[0]), int(hw_duedate.split("/")[1]))

    #print(hw_dd)

    #print(hw_assignment + "::" + hw_class + "::" + str(hw_dd))
    #hw_list = [hw_assignment, hw_class]
    #hw.append(hw_list)
    hw_list.append([hw_assignment, hw_class, hw_dd])
 
def output_hw(duedate, h):
    global current_day, next_day, dtd, dtt
    
    if duedate == current_day:
      dtd = True
    elif duedate == next_day:
      dtt = True

    if dtd:
      print(str(h[0]) + " in " + str(h[1]) + " due " + "TODAY!")
      dtd = False
    elif dtt:
      print(str(h[0]) + " in " + str(h[1]) + " due " + "TOMORROW!")
      dtt = False
    elif not dtt:
      print(str(h[0]) + " in " + str(h[1]) + " due " + duedate)
      dtt = False
    elif not dtd:
      print(str(h[0]) + " in " + str(h[1]) + " due " + duedate)
      dtd = False

day = ""
if int(time.strftime("%d")) < 10: 
  day = "0" + str(int(time.strftime("%d")))

current_day = time.strftime("%m") + "/" + str(day) + "/" + time.strftime("%Y")
next_day = time.strftime("%m") + "/" + str(int(day)+1) + "/" + time.strftime("%Y")
  
print("Today is: " + current_day)

subdomain = "sms-lafsd-ca" # SchoolLoop subdomain, hardcoded right now
username = input("Username: ")
password = getpass.getpass()
s2 = get_data(subdomain, username, password)

get_grades()

get_homework()
  
print("")  

for g in grades:
   print(str(g[0]) + "°: " + str(g[1]) + " (" + str(g[2]) + "): " + str(g[3]))
    
print("")

for h in hw_list:
   h2 = str(h[2]).split("-")
   duedate = h2[1] + "/" + h2[2] + "/" + h2[0]
   
   output_hw(duedate, h)
