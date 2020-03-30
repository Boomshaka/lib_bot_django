import threading
from multiprocessing import Queue
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import selenium.common.exceptions as SeleniumException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import imaplib
from email.message import EmailMessage
from email.parser import BytesParser, Parser
import random
from html.parser import HTMLParser
import csv
import datetime
from datetime import date
import logging

from .student import Student
from .dateconfig import Dates
from .database import Database
# import configure as cfg
from .configure import getStartID, getWebDriverPath


global linkList


#degbug: Detailed information, typically of interest only when diagnosing problems
#info: Confirmation that things are working as expected
#warning: Indication that something unexpected happened
#error: Due to a more serious issue, software has not been able to perform something
#critical: Serious error, indicating that the program itself may be unable to continue running
#DEFAULT = Warning
#logging.debug()

# logging.basicConfig(filename = "libbot.log", level = logging.DEBUG, 
#                     format = '%(created)f:%(funcName)s:%(message)s:%(thread)d')





def sleep():
    time.sleep(random.randint(1,2))

def setup_browser():
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # browser = webdriver.Chrome(cfg.webdriver['path'], chrome_options=chrome_options)
    path = getWebDriverPath()
    
    browser = webdriver.Chrome(path)
    return browser

def collect_student_list(diffday):
    students = []
    if diffday.day%3 == 0:
        with open("script/credentials.csv", newline='') as credentials_csv:
            reader = csv.DictReader(credentials_csv)
            for index, row in enumerate(reader):
                students.append(Student(row['username'],row['password']))
                students[index].log.info("\n\n\n")
    elif diffday.day%3 == 1:
        with open("script/credentialstwo.csv", newline='') as credentials_csv:
            reader = csv.DictReader(credentials_csv)
            for index, row in enumerate(reader):
                students.append(Student(row['username'],row['password']))
                students[index].log.info("\n\n\n")
    else:
        with open("script/credentialsthree.csv", newline='') as credentials_csv:
            reader = csv.DictReader(credentials_csv)
            for index, row in enumerate(reader):
                students.append(Student(row['username'],row['password']))
                students[index].log.info("\n\n\n")
    return students

def collect_id_list(targetRoom,dates,len_gmail):
    some_reason_for_num = 816     
    id = str(targetRoom)
    id_list = []
    twelve_AM_id = dates.start_id[id] + some_reason_for_num * dates.diff_day
    next_room_id = twelve_AM_id + 48
    id_list.append(twelve_AM_id)
    #print(twelveAM)

    #uncomment pls

    # logger.info("TwelveAM ID {}".format(twelve_AM_id))
    new_id = dates.start_id[id] + some_reason_for_num * dates.diff_day
    
    for x in range(len_gmail - 1):
        if new_id < next_room_id:
            id_list.append(new_id)
        new_id += 4
    id_list = list(reversed(id_list))
    return id_list, twelve_AM_id

def search_mail(key,value,M):
    result, data = M.search(None, key, '"{}"'.format(value))
    return data

def collect_emails(result_bytes,M):
    msgs = []
    for num in result_bytes[0].split():
        typ, data = M.fetch(num, '(RFC8222)')
        msgs.append(data)
    return msgs

def room_reserve(student,ID,date_to_reserve,target_time,twelve_AM_id):
    #Open libcal website and go to correct month
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # print('ROOM _RESERVE CALLED')

    browser = setup_browser()
    browser.get('https://libcal.library.ucsb.edu/rooms.php?i=12405')
    select = Select(browser.find_element_by_class_name('ui-datepicker-month'))
    select.select_by_value(str(date_to_reserve.month - 1))
    time.sleep(.25)
    browser.find_element_by_link_text(date.strftime(date_to_reserve,"%d").lstrip('0')).click()
    time.sleep(6)
    ID = target_time*2 + ID
    # print("ID for ", username, " is ", ID)
    

    sleep()
    timeslots = []
    #click 4 time slots, total 2 hours
    for x in range(4):
        timeslots.append((ID - twelve_AM_id) * 50)
        ID = int(ID)
        ID = str(ID)
        try:
            browser.find_element_by_id(ID).click()
        # except ElementNotInteractableException as Exception:

        except (NoSuchElementException, ElementNotInteractableException) as Exception: 
            student.log.error("Room not found or already reserved: {}".format(timeslots[x]))
            pass
        ID = int(ID)
        ID += 1
        time.sleep(0.25)
    student.log.info("Timeslot for {} is {}-{}".format(student.username, timeslots[0], timeslots[-1]))

    #get to the next screen
    browser.find_element_by_name('Continue').click()
    browser.find_element_by_id('s-lc-rm-sub').click()

    time.sleep(3)

    #loginUCSB
    browser.find_element_by_id('username').send_keys(student.username)
    browser.find_element_by_id('password').send_keys(student.password)
    sleep()
    browser.find_element_by_name('submit').click()

    time.sleep(5)

    #send Group Name

    try:
        browser.find_element_by_id("nick").send_keys('Nintendo Co. Customer Support')
        browser.find_element_by_name('Submit').click()
        # print ('Successful confirmation for:', students[k].username)
    except NoSuchElementException as Exception:
        student.log.error("Slot to submit roomname not found for {} at {}-{}, either username/password didn't work or browser too slow".format(student.username, timeslots[0],timeslots[-1]))
        # pass

    
    print (datetime.datetime.now())
    sleep()
    browser.close()
    browser.quit()


def gmail_login(student):
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    time.sleep(2) #new
    #Log into ucsb gmail and find latest email ID
    print(student.email)

    try:
        M.login(student.email, student.password)
        #print ('Successful confirmation for:', students[k].username)
    except Exception:
        student.log.error('Email login failed with {}, wrong username/password'.format(student.username))
        # pass

    return M



def cancel_booking(student):
    print("canceling booking for", student.username)
    M = gmail_login(student)
    M.select('inbox')
    rv, data = M.search(None,'FROM', '"LibCal"')
    mail_ids = data[0]
    id_list = mail_ids.split()
    latest_email_id =id_list[-1]
    print("EMAIL ID IS: ",latest_email_id)
    
    #Access latest email
    sleep()
    # msg_data = collect_emails(search_mail('FROM','alerts@mail.libcal.com', M), M)
    # target_msg=msg_data[0]
    typ, msg_data = M.fetch(latest_email_id, '(RFC822)')
    msg = Parser().parsestr(str(msg_data[0][1]))
    msg=str(msg)

    #Set msg equal to the confirmation link
    index1 = msg.index('https://libcal.library.ucsb.edu/cancel_booking')
    msg = msg[index1:index1+145]
    print(msg)
    M.close()
    M.logout()

    browser = setup_browser()
    browser.get(msg)
    sleep()
    browser.find_element_by_id('rm_confirm_link').click()
    browser.close()




#Input: instance of Student class
# class Student:
#     def _init__(self, username, password):
#         self.username = username + '@ucsb.edu'
#         self.password = password
def confirm_room(student):
    M = gmail_login(student)
    M.select('inbox')
    rv, data = M.search(None,'FROM', '"LibCal"')
    mail_ids = data[0]
    id_list = mail_ids.split()
    latest_email_id =id_list[-1]
    print("EMAIL ID IS: ",latest_email_id)

    #Access latest email
    sleep()
    # msg_data = collect_emails(search_mail('FROM','alerts@mail.libcal.com', M), M)
    # target_msg=msg_data[0]
    typ, msg_data = M.fetch(latest_email_id, '(RFC822)')
    msg = Parser().parsestr(str(msg_data[0][1]))
    msg=str(msg)

    #Set msg equal to the confirmation link
    index1 = msg.index('https://libcal.library.ucsb.edu/confirm')
    msg = msg[index1:index1+98]
    print(msg)
    M.close()
    M.logout()

    #Open up confirmation link and confirm rooms
    
    browser = setup_browser()
    browser.get(msg)
    sleep()
    browser.find_element_by_id('rm_confirm_link').click()
    browser.close()

    # cancel_booking(student)

def main(target_time, target_room):

    formatter = logging.Formatter('{:<28}   :   {:<35}   :   {:<70}'.format('Time logged = %(asctime)s','Function name = %(funcName)s','message= %(message)s'))
    file_handler = logging.FileHandler('libbot.log')
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    #uncomment pls
    logger.info("main called with target time={} and target room={}".format(target_time,target_room))
    start_id = getStartID()

    dates = Dates(start_id, target_time)
    dates.configure()
    diffday = dates.date_to_reserve
    
    students = collect_student_list(diffday)
    len_gmail = len(students)

    id_list,twelve_AM_id = collect_id_list(target_room,dates, len_gmail)

    thread_list = []
    start = time.time()
    # print("Length of gmail, ", len_gmail)

    #uncomment pls
    logger.info("List of Students: {}".format(*students))
    for i in range(len_gmail):
        thread = threading.Thread(target = room_reserve, args = (students[i],id_list[i],dates.date_to_reserve,target_time,twelve_AM_id))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    # print ('total time taken:' , time.time()-start)

    #uncomment pls
    logger.info("total time taken: {}".format(time.time()-start))

    db = Database()
    db.create_connection()

    for k in range(len_gmail):
        linkList = []  
        id = db.get_student_id(students[k].username)
        try:
            confirm_room(students[k])
            # print ('Successful confirmation for:', students[k].username)

            #uncomment pls
            logger.info("Successful confirmation for: {}".format(students[k].username))
            db.update_stats(id,True)
        except Exception:
            # print('unsuccessful, trying next person')
            #uncomment pls
            logger.error('an error has occured with the following username, trying next username: {}'.format(students[k].username))
            db.update_stats(id,False)
            pass

    db.close_connection()

if __name__ == "__main__":
    # formatter = logging.Formatter('{:<28}   :   {:<35}   :   {:<70}'.format('Time logged = %(asctime)s','Function name = %(funcName)s','message= %(message)s'))
    # file_handler = logging.FileHandler('libbot.log')
    # file_handler.setFormatter(formatter)

    #uncomment pls

    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)
    # logger.addHandler(file_handler)
    while True:
        #wait for midnight
        while datetime.datetime.now().hour == 0:
            print ('sleeping ... ' , datetime.datetime.now())
            time.sleep(1)
            #start booking at 12pm
        main(5, 2334)

        #uncomment pls
        # logger.info("\n\n\n")
        print ('sleeping for one hour...')
        time.sleep(3600)
        # print 'sleeping for one hour...'
        # time.sleep(3600)


