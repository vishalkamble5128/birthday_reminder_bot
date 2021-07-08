#https://api.telegram.org/bot1702120946:AAEy3tcM1jsC1XRYazpfDR1L554iDUMW_rM/getUpdates?timeout=1

from io import IncrementalNewlineDecoder
from telegram_bot import *
from time import sleep
from datetime import *
import pandas as pd
import time
import csv
import os
from dateutil.relativedelta import relativedelta
import pytz

admin_id = 803656239
bot = telegram_chatbot("token.cfg")

# getting today's date
def todays_date():
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    return datetime_ist.strftime("%d-%m-%Y")

def notify(user_id,user_name,birthday_of):
    print(user_id,birthday_of)
    bot.send_message(" 🅱🅸🆁🆃🅷🅳🅰🆈 🆁🅴🅼🅸🅽🅳🅴🆁 \n\nhey , {}\nBirthday of {} on {}".format(user_name,birthday_of,todays_date()),user_id)

#controller function
def controller(user_id,name,message):
    print(message)
    if(message == "/start"):
        bot.send_message("❖ welcome to birthday reminder bot ❖\n❖ created by νιѕнαℓ кαмвℓє ❖\n\nHow to use :\n-> send a message containing details about the birthday in the format\n---------------------------\nSyntax: add=DD-MM-YYYY,name of the person\nEx: add=20-09-2000,vishal kamble\n---------------------------",user_id)           
        controller(user_id,name,"/help")
    elif "add=" in message:
        message = message.replace("add=","")

        try:
            date_string,birthday_of = message.split(",")
        except:
            bot.send_message("please enter details and try again",user_id)
         
        try:
            IST = pytz.timezone('Asia/Kolkata')
            datetime_ist = datetime.now(IST)
            datetime.strptime(date_string, "%d-%m-%Y")
            date_format = True
        except ValueError:
            bot.send_message("format of date and month should be like --> DD-MM\nEx:\n1. 02-05-2000\n2. 22-11-2021",user_id)
            return

        d,m,y = str(date_string).split("-")


        if(date_format and birthday_of and check_for_invalid_birth_date(date_string)):     #checking for incorrect format or misplaced info
            with open("users_data.csv" , "a" , newline='') as csvfile:
                writer=csv.writer(csvfile)

                newdate1 = time.strptime(str(d+"-"+m), "%d-%m")
                newdate2 = time.strptime(current_date_and_month(), "%d-%m")

                if (newdate1<newdate2):
                    increment_year = 1
                else:
                    if int(y) > int(current_year()):
                        bot.send_message("invalid birth date \n try again",user_id)
                        return 0
                    increment_year = 0

                upc_birthday = datetime_ist.strftime("{}-{}".format(str(d+"-"+m),str(int(current_year())+increment_year)))
                bot.send_message("🅽🅴🆆 🅱🅸🆁🆃🅷🅳🅰🆈 🅰🅳🅳🅴🅳\n\nName: {}\nBirth_date: {}\nUpcoming birthday: {}\n\nFrom.\nuser id: {}\nuser name: {}".format(birthday_of,date_string,upc_birthday,user_id,name),admin_id)
                bot.send_message("🅽🅴🆆 🅱🅸🆁🆃🅷🅳🅰🆈 🅰🅳🅳🅴🅳\n\nName: {}\nBirth_date: {}\nUpcoming birthday: {}".format(birthday_of,date_string,upc_birthday),user_id)
                writer.writerow([user_id,name,date_string,birthday_of,upc_birthday]) 
                csvfile.close()
        else:
            bot.send_message("incorrect format or invalid birth date",user_id)
    elif "/help" == message:
        bot.send_message("User operations :\n----------\n1./get_my_data\n2./birthdays_this_month\n3./upcoming_birthday\n3./time\n4./report_bug\n----------",user_id)
    elif "/time" == message:
        IST = pytz.timezone('Asia/Kolkata')
        datetime_ist = datetime.now(IST)
        bot.send_message(datetime_ist.strftime("%d-%m-%Y   %I:%M %p"),user_id)
    elif "/get_my_data" == message:
        send_user_data(user_id)
    elif "/birthdays_this_month" == message:
        birthdays_this_month(user_id)
    elif "/upcoming_birthday" == message:
        upcoming_birthday(user_id)
    elif "/report_bug" == message:
        bot.send_message("Use following method:\n\nsyntax : bug=bug_discription\nEx : bug=there is a bug related to birth date",user_id)
    elif "bug=" in message:
        bot.send_message("bug recorded",user_id)
        bot.send_message("Thank you for your support",user_id)

        message = message.replace("bug=","")
        bot.send_message(f"Hey , vishal kamble \nI am {name} recently i found a bug in your system , bug description as below \n\nBug: {message}",admin_id)
    
    # admin control panel
    elif user_id == admin_id:
        if "/admin_help" in message:
            bot.send_message("welcome sir , \n\n1./get_all_file\n2./get_all_messages\n3./time",user_id)
        elif "/get_all_file" == message:
            bot.send_document(user_id,"users_data.csv")
        elif "/get_all_messages" == message:
            bot.send_document(user_id,"messages.csv")
            
    else:
        bot.send_message("sorry , i could'nt understand !",user_id)


def check_for_invalid_birth_date(date):
    newdate1 = time.strptime(date, "%d-%m-%Y")
    newdate2 = time.strptime(todays_date(), "%d-%m-%Y")

    if (newdate1<newdate2):
        return 1
    else:
        return 0


def birthdays_this_month(user_id):
    write_index = []
    data_status = False
    df = pd.read_csv('users_data.csv')

    for index,item in df.iterrows():
        if index==0 or index:
            if(item['user_id'] == user_id):
                d,m,y = str(item['upcoming_birthday']).split("-")
                
                if y==current_year() and m == current_month():
                    write_index.append(index)
                    data_status = True

    file_path = str(user_id)+" B_T_M"+".csv"
    with open(file_path , "a" , newline='') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(["Name","Birthday"])
            csvfile.close()
    
    if data_status:
        for i in write_index:
            with open(file_path , "a" , newline='') as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow([df.loc[i,'birthday_of'],df.loc[i,'upcoming_birthday']])
                csvfile.close()

        bot.send_message("Total {} birthdays in this month".format(len(write_index)),user_id)
        bot.send_document(user_id,file_path)
    else:
        bot.send_message("You don't have any birthdays in this month",user_id)
    
    try:
        os.remove(file_path)
    except:
        pass

def current_date_and_month():
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    return datetime_ist.strftime("%d-%m")

def current_year():
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    return datetime_ist.strftime("%Y")

def current_month():
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    return datetime_ist.strftime("%m")

def upcoming_birthday(user_id):
    data_status = False
    date = []
    df = pd.read_csv('users_data.csv')

    for index,item in df.iterrows():
        if index==0 or index:
            if(item['user_id'] == user_id):
                date.append(item['upcoming_birthday'])
                data_status = True
    if data_status:
        date.sort(key = lambda date: datetime.strptime(date, '%d-%m-%Y'))
        upcoming_birthday = date[0]

        bot.send_message("Upcoming birthdays are of",user_id)

        for index,item in df.iterrows():
            if index==0 or index:
                if(item['user_id'] == user_id):
                    if upcoming_birthday == item['upcoming_birthday']:
                        bot.send_message("Name : {} \nDate : {}".format(item['birthday_of'],item['upcoming_birthday']),user_id)
    else:
        bot.send_message("You don't have any data",user_id)

def insert_into_messages_file(user_id,user_name,message):
    with open("messages.csv" , "a" , newline='') as file:
        writer=csv.writer(file)
        writer.writerow([user_id,user_name,message])
        file.close()

def send_user_data(user_id):
    write_index = []
    data_status = False
    df = pd.read_csv('users_data.csv')

    for index,item in df.iterrows():
        if index==0 or index:
            if(item['user_id'] == user_id):
                write_index.append(index)
                data_status = True

    file_path = str(user_id)+".csv"
    with open(file_path , "a" , newline='') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(["birthday_of","birth_date","upcoming_birthday"])
            csvfile.close()
    
    if data_status:
        for i in write_index:
            with open(file_path , "a" , newline='') as csvfile:
                writer=csv.writer(csvfile)
                date,month,year = str(df.loc[i,'birthday_date']).split("-")
                writer.writerow([df.loc[i,'birthday_of'],df.loc[i,'birthday_date'],df.loc[i,'upcoming_birthday']])
                csvfile.close()

        bot.send_document(user_id,file_path)
        os.remove(file_path)
    else:
        bot.send_message("You don't have any data",user_id)

# reading csv file
def read_csv():
    write_index = []
    df = pd.read_csv('users_data.csv')

    for index,item in df.iterrows():
        if(item['upcoming_birthday'] == todays_date()):
            notify(item['user_id'],item['user_name'],item['birthday_of'])
            write_index.append(index)

    for i in write_index:
        date,month,year = str(item['upcoming_birthday']).split("-")

        df.loc[i,'upcoming_birthday'] = date+"-"+month+"-"+str(int(year)+1)
        # print(df)
        df.to_csv('users_data.csv',index=False)

while True:
    sleep(2)
    update_id = None
    i=0
    while True:
        read_csv()
        i+=1
        print(i)
        try:
            updates = bot.get_updates(offset=update_id)
            updates = updates["result"]
            if updates:
                for item in updates:
                    update_id = item["update_id"]                
                    message = item["message"]['text']
                    user_id = int(item["message"]["from"]["id"])
                    name = item["message"]["from"]["first_name"]+" "+ item["message"]["from"]["last_name"]
                    print("_______________________________ \n ")
                    print("update id : ",update_id)
                    print("user_id:",user_id)
                    print("user_name:",name)
                    print("message:",message)
                    print("_______________________________")

                    insert_into_messages_file(user_id,name,message)
                    controller(user_id,name,message)                   

        except Exception as e:
            print("!! ERROR !! : ",e)