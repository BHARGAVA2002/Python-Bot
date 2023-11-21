import requests as rq
import re


def split_dob(dob):
    temp=dob.split('-')
    return temp

def scrap_cie(usn,dob):
    temp=split_dob(dob)
    dd=temp[0]
    mm=temp[1]
    yyyy=temp[2]
    payload={
        "username": usn,
        "dd": dd ,
        "mm": mm,
        "yyyy": yyyy,
        "passwd": yyyy+"-"+mm+"-"+dd,
        "remember": "No",
        "option": "com_user",
        "task": "login"
    }
    loginurl="https://parents.msrit.edu/index.php"
    dashboardurl="https://parents.msrit.edu/index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard"

    with rq.session() as s:
        r=s.post(loginurl,payload)
        r2=s.get(dashboardurl)
    text=r2.text
    temp=re.search("columns:",text)
    temp2=re.search('type: "bar"',text)
    arr=text[temp.span()[1]+2:temp2.span()[0]-9]
    regex='"[A-Z]{2}\d{2}",\d{2}||"[A-Z]{2}\d{2}",\d{1}||"[A-Z]{3}\d{2}",\d{2}||"[A-Z]{3}\d{2}",\d{1}||"[A-Z]{3}\d{3}",\d{2}||"[A-Z]{3}\d{3}",\d{1}||"[A-Z]{4}\d{2}",\d{2}||"[A-Z]{4}\d{2}",\d{1}||"[A-Z]{4}",\d{2}||"[A-Z]{4}",\d{1}'
    res=re.findall(regex,arr)
    temp=""
    for x in res:
        if x!="":
          temp+=x+"\n"
    return temp

def scrap_attendence(usn,dob):
    temp=split_dob(dob)
    dd=temp[0]
    mm=temp[1]
    yyyy=temp[2]
    payload={
        "username": usn,
        "dd": dd ,
        "mm": mm,
        "yyyy": yyyy,
        "passwd": yyyy+"-"+mm+"-"+dd,
        "remember": "No",
        "option": "com_user",
        "task": "login"
    }
    loginurl="https://parents.msrit.edu/index.php"
    dashboardurl="https://parents.msrit.edu/index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard"

    with rq.session() as s:
        r=s.post(loginurl,payload)
        r2=s.get(dashboardurl)
    temptext=r2.text
    temps=re.search('type: "bar"',temptext)
    text=temptext[temps.span()[0]:]
    temp=re.search("columns:",text)
    temp2=re.search('type: "gauge"',text)
    arr=text[temp.span()[1]+2:temp2.span()[0]-36]
    regex='"[A-Z]{2}\d{2}",\d{3}||"[A-Z]{2}\d{2}",\d{2}||"[A-Z]{3}\d{2}",\d{3}||"[A-Z]{3}\d{2}",\d{2}||"[A-Z]{3}\d{3}",\d{3}||"[A-Z]{3}\d{3}",\d{2}||"[A-Z]{4}\d{2}",\d{2}||"[A-Z]{4}\d{2}",\d{3}||"[A-Z]{4}",\d{2}||"[A-Z]{4}",\d{3}||"[A-Z]{4}",\d{1}'
    res=re.findall(regex,arr)
    temp=""
    for x in res:
        if x!="":
          temp+=x+"\n"
    return temp

