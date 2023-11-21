import mysql.connector as con
import datetime as dt

mydb=con.connect(host="localhost",user="root",password="msrit",database="Telegram")

def gettime():
    text=dt.datetime.today()
    temp=str(text)
    return temp[0:19]

def getdetails(chatid):
    mycursor=mydb.cursor()
    mycursor.execute("select *from user_details where chatid="+str(chatid))
    for x in mycursor:
        return x

def insertdetails(chatid,name,usn,dob):
    mycursor=mydb.cursor()
    sqlform="insert into user_details(chatid,name,usn,dob) values(%s,%s,%s,%s)"
    mycursor.execute(sqlform,(chatid,name,usn,dob))
    mydb.commit()

def updatedetails(chatid,usn,dob):
    mycursor=mydb.cursor()
    sqlform="update user_details set usn='"+str(usn)+"', dob='"+str(dob)+"' where chatid="+str(chatid)+";"
    mycursor.execute(sqlform)
    mydb.commit()

def insertmessage(chatid,name,message):
    mycursor=mydb.cursor()
    try:
        sqlform="insert into "+str(name)+"_"+str(chatid)+"(date_time,Message) values(%s,%s)"
        mycursor.execute(sqlform,(gettime(),message))
        mydb.commit()
    except:
        print("Exception occurred")
        mycursor.execute("create table "+str(name)+"_"+str(chatid)+" (date_time varchar(25),Message varchar(50));")
        insertmessage(chatid,name,message)
