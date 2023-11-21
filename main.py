import telegram as t
import telegram.ext as te
import sis_scrap
import sqldb

USN,DOB=range(2)
usn=""
dob=""

#Conversation Handlers
#/setup
def setup(update,context):
    chatid=update.message.chat_id
    text=update.message.text
    fname=update.message.chat.first_name
    sqldb.insertmessage(chatid,fname,text)
    bot.send_message(chatid,"Enter your USN")
    return USN

def getusn(update,context):
    global usn
    chatid=update.message.chat_id
    text=update.message.text
    fname=update.message.chat.first_name
    sqldb.insertmessage(chatid,fname,text)
    usn=str(text)
    bot.send_message(chatid,"Enter your DOB in dd-mm-yyyy format")
    return DOB

def getdob(update,context):
    global dob
    chatid=update.message.chat_id
    text=update.message.text
    fname=update.message.chat.first_name
    sqldb.insertmessage(chatid,fname,text)
    dob=str(text)
    bot.send_message(chatid,"Setup successful")
    sqldb.insertdetails(chatid,str(update.message.chat.first_name),usn,dob)
    return te.ConversationHandler.END

def end(update,context):
    chatid=update.message.chat_id
    text=update.message.text
    fname=update.message.chat.first_name
    sqldb.insertmessage(chatid,fname,text)
    bot.send_message(chatid,"Setup successful")
    return te.ConversationHandler.END

#/update
def update_function(update,context):
    chatid=update.message.chat_id
    text=update.message.text
    fname=update.message.chat.first_name
    sqldb.insertmessage(chatid,fname,text)
    bot.send_message(chatid,"Enter your USN")
    return USN

def updateusn(update,context):
    global usn
    chatid=update.message.chat_id
    text=update.message.text
    fname=update.message.chat.first_name
    sqldb.insertmessage(chatid,fname,text)
    usn=str(text)
    bot.send_message(chatid,"Enter your DOB in dd-mm-yyyy format")
    return DOB

def updatedob(update,context):
    global dob
    chatid=update.message.chat_id
    text=update.message.text
    fname=update.message.chat.first_name
    sqldb.insertmessage(chatid,fname,text)
    dob=str(text)
    bot.send_message(chatid,"Setup successful")
    sqldb.updatedetails(chatid,usn,dob)
    return te.ConversationHandler.END

def end(update,context):
    chatid=update.message.chat_id
    text=update.message.text
    fname=update.message.chat.first_name
    sqldb.insertmessage(chatid,fname,text)
    bot.send_message(chatid,"Setup successful")
    return te.ConversationHandler.END


#Command Handlers
def start_function(update,context):
    chatid=update.message.chat_id
    fname=update.message.chat.first_name
    text=update.message.text
    sqldb.insertmessage(chatid,fname,text)
    bot.send_message(chatid,"Hello "+fname)
    bot.send_message(chatid,"Your bot has started successfully\n\nThis bot can fetch your Attendence and Cie marks from SIS\n\nYou can control this bot by using these commands\n/setup->To run setup\n/update->To update your details\nAttendence->To display your attendence\nCie->To display your Cie marks\n\nLets start setting up your details")
    bot.send_message(chatid,"Start the setup by sending '/setup'")

def help_function(update,context):
    chatid=update.message.chat_id
    bot.send_message(chatid,
        "/setup->To run setup\n/update->To update your details\nAttendence->To display your attendence\nCie->To display your Cie marks"
    )


#Message Handlers
def message_function(Update,context):
    chatid=Update.message.chat_id
    try:
        details=sqldb.getdetails(chatid)
        usn=details[2]
        dob=details[3]
    except:
        print()
    fname=Update.message.chat.first_name
    text=Update.message.text
    print(chatid)
    msg=str(text)
    sqldb.insertmessage(chatid,fname,text)
    print(msg)
    if msg.lower()=="attendence":
        text=sis_scrap.scrap_attendence(usn,dob)
        bot.send_message(chatid,text)
    if msg.lower()=="cie":
        text=sis_scrap.scrap_cie(usn,dob)
        bot.send_message(chatid,text)


bot=t.Bot("6303319857:AAETADC5ZqWxX33GvO9025apZ-WrkoOsAkE")

updater=te.Updater("6303319857:AAETADC5ZqWxX33GvO9025apZ-WrkoOsAkE",use_context=True)
dispatcher=updater.dispatcher
start=te.CommandHandler("start",start_function)
dispatcher.add_handler(start)
con=te.ConversationHandler(
    entry_points=[te.CommandHandler("setup",setup)],
    states={
        USN : [te.MessageHandler(te.Filters.regex("1ms[1-2][0-9][a-z][a-z]\d {3}"),getusn)],
        DOB : [te.MessageHandler(te.Filters.regex("[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]"),getdob)]
    },
    fallbacks=[te.CommandHandler("end",end)]
)
dispatcher.add_handler(con)
help=te.CommandHandler("help",help_function)
dispatcher.add_handler(help)
update_handler=te.ConversationHandler(
    entry_points=[te.CommandHandler("update",update_function)],
    states={
        USN : [te.MessageHandler(te.Filters.regex("1ms[1-2][0-9][a-z][a-z]\d{3}"),updateusn)],
        DOB : [te.MessageHandler(te.Filters.regex("[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]"),updatedob)]
    },
    fallbacks=[te.CommandHandler("end",end)]
)
dispatcher.add_handler(update_handler)
message=te.MessageHandler(te.Filters.text,message_function)
dispatcher.add_handler(message)
updater.start_polling()
updater.idle()