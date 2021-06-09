from tkinter import *
import MySQLdb
import tkinter
from tkinter import messagebox
from pusher import Pusher
import pysher
from dotenv import load_dotenv
import os
import json
#provided by pusher for API calling
APP_ID=''
APP_KEY=''
APP_SECRET=''
APP_CLUSTER=''
pusher = None
clientPusher=None
channel = None
user = None
chatroom=None
chatrooms = ["sports", "general", "education", "health", "technology"]
master = Tk() 
label = Label(master, text='Username:')
label.grid(row =0)
label2 = Label(master, text='Password:') 
label2.grid(row=2)
e1 = Entry(master) 
e2 = Entry(master,show="*") 
e1.grid(row = 1) 
e2.grid(row=3)
conn = MySQLdb.connect(host ='localhost',user = 'root',passwd='',database ='chat')
cursor = conn.cursor()

def register():
	username = e1.get()
	password = e2.get()
	query = ('SELECT * FROM details WHERE username = %s AND password = %s')
	cursor.execute(query,[username,password])
	result = cursor.fetchall()
	if result:
		for i in result:
			print("!!!User Exists Try Login!!!")
		
	else:
		query ="INSERT details (`username`, `password`) VALUES (%s, %s)"
		cursor.execute(query,[username,password])
		conn.commit()
		print("!!!!Successfully Registered!!!!")

btn = Button(master, text="register",command = register)
btn.grid(row = 4)

def chat():
	top = tkinter.Tk()
	top.title("MyMessenger")
	
	messages_frame = tkinter.Frame(top)
	my_msg = tkinter.StringVar()  # For the messages to be sent.
	my_msg.set("Type your messages here.")
	scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
	# Following will contain the messages.

	
	
	def CurSelet(evt):
		value = str((Lb.get(Lb.curselection())))
		global chatroom
		chatroom = value
		initPusher()
		
		
		
	
	def initPusher():
		global pusher
		pusher = Pusher(app_id = APP_ID,key= APP_KEY, secret=APP_SECRET,cluster= APP_CLUSTER)
		global clientPusher
		clientPusher = pysher.Pusher(APP_KEY,APP_CLUSTER)
		clientPusher.connection.bind('pusher:connection_established',connectHandler)
		clientPusher.connect()
	def connectHandler(data):

		channel = clientPusher.subscribe(chatroom)
		channel.bind('newmessage', pusherCallback)
		
		
	def getInput():
		msg = entry_field.get()
		msg_list.insert(END,msg)
		pusher.trigger(chatroom, u'newmessage', {"user": user, "message": msg})

	def pusherCallback(message):
		message = json.loads(message)
		data = message['message']
		print(data)
		if message['user']!= user:
			msg_list.insert(END,data)
	
	
	
	Lb = Listbox(messages_frame,height=15,yscrollcommand=scrollbar.set)
	Lb.bind('<<ListboxSelect>>',CurSelet)
	for items in chatrooms:
		Lb.insert(END,items)
	Lb.pack(side = tkinter.LEFT) 
	msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
	
	scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
	msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
	msg_list.pack()
	messages_frame.pack()

	entry_field = tkinter.Entry(top,width = 30 ,textvariable=my_msg)
	entry_field.bind("<Return>",getInput)
	entry_field.pack()

	send_button = tkinter.Button(top, text="Send",width = 30,command = getInput)
	send_button.pack(side = tkinter.RIGHT)
	tkinter.mainloop()

def login():
	username = e1.get()
	password = e2.get()
	query = ('SELECT * FROM details WHERE username = %s AND password = %s')
	cursor.execute(query,[username,password])
	result = cursor.fetchall()
	if result:
		for i in result:
			print( "!!!!Successfully Logged-In!!!!")
			global user
			user = username
		chat()
	else:
		print("!!!!!Account Not Regitered Yet!!!!!")
	
	

btn2 = Button(master,text ="login", command = login)
btn2.grid(row=5)

master.mainloop()



