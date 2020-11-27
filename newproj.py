#project (checkpoint)

# So what should be the theme of the project?
# The theme would be making a gui based programme.
# Can have mysql database.
# saves data after encoding(basically make an encoder program as well)

from tkinter import *
from tkinter import messagebox
import math
import random
import mysql.connector as mys
from time import sleep

#variables
themeback="black"
fontback=themeback
fontcolor="red"
entryback="white"
toshow='*'
databasename='mysql'
temptab = None

class loginwindow():
    def __init__(self):
        def connect():
            global conn
            connestablished = False
            uname=username.get()
            upass=password.get()
            if uname=='':
                uname='root'

            try:
                mys.connect(host='localhost',user=uname,passwd=upass,database=databasename)
                connestablished = True

            except Exception as e:
                messagebox.showerror("Status","Connection failed with error \n" + e)
            
            if connestablished == True:
                conn = mys.connect(host='localhost',user=uname,passwd=upass,database=databasename)
                messagebox.showinfo("Status","Connection Successful")
                loginwin.destroy()
                mycursor=conn.cursor()
                datawin=databasewin(mycursor)
                

        loginwin=Tk()
        loginwin.title("Connecting to mysql server")
        loginwin.config(background=themeback)
        loginwin.state("zoomed")
        Label(loginwin,text="Login to mysql \n\n",bg=fontback,fg=fontcolor,font="Agency_fb 20 bold").grid(column=0,row=0,columnspan=3)

        Label(loginwin,text="Enter your user (Default 'root'): ",bg=fontback,fg=fontcolor,font="Agency_fb 12 bold").grid(column=0,row=1)
        rootvar=StringVar()
        rootvar.set("root")
        username=Entry(loginwin,text=rootvar,width=20,bg=entryback)
        username.grid(column=2,row=1,sticky=E)

        Label(loginwin,text="",bg=fontback,fg=fontcolor).grid(column=1,row=2)
        Label(loginwin,text="",bg=fontback,fg=fontcolor).grid(column=1,row=4)        

        Label(loginwin,text="Enter your mysql password\n(leave empty for no password):",bg=fontback,fg=fontcolor,font="Agency_fb 12 bold").grid(column=0,row=3,sticky = S)
        password=Entry(loginwin,width=20,bg=entryback,show=toshow)
        password.grid(column=2,row=3,sticky=S)

        Button(loginwin,text="Login",width=15,command=connect).grid(column=1,row=5,sticky=S)

class listtab():
    def __init__(self, mycursor, tablename):
        self.cursor = mycursor
        self.tablename= tablename
        self.pw = PanedWindow(orient = 'horizontal')
        self.pw.grid(column = 0, row = 1100, columnspan = 10)
        self.pw.config(background = themeback)
        self.showlist(self.cursor,self.tablename)

    def showlist(self, cursor, tablename):
        cursor.execute(f'select * from {tablename}')
        tablelist = cursor.fetchall()
        cursor.execute(f'desc {tablename}')
        tabname = cursor.fetchall()
        print(tabname)
        cno = 0
        rno = 0
        listbuttons = []
        print(tablelist)
        #for i in range(len(tablelist)):
            

class tablewin():
    def __init__(self,database,mycursor):
        self.database = database
        self.cursor = mycursor
        self.pw=PanedWindow(orient = 'horizontal')
        self.pw.grid(column = 0, row = 1010, columnspan = 4)
        self.pw.config(background = themeback)
        self.cno = 0
        self.rno = 0
        self.showtable()
    
    def databaseview(self,cursor):
        databasewin(cursor)

    def showtable(self):
        self.cursor.execute('use {}'.format(self.database))
        self.cursor.execute("show tables")
        tables = self.cursor.fetchall()

        Label(self.pw, text = "Database:- " + self.database + '\n',bg = fontback , fg = fontcolor, font = "Agency_fb 12 bold").grid(column = 0, row = 0, columnspan = 7)

        if len(tables) == 0:
            Label(self.pw,text = "No tables to show in this database ",fg = fontcolor, bg = fontback, font = "Agency_fb 12 bold").grid(column = 1,row = 2,columnspan = 3)
        
        else:
            tablebuttons = []
            self.cno = 0
            self.rno =1
            for i in range(0,len(tables)):
                if self.cno > 6 :
                    self.cno = 0
                    self.rno +=1
                tablebutton = Button(self.pw, text = tables[i][0],width = 15, command = lambda i = i:listtab(self.cursor, tables[i][0])).grid(column = self.cno, row = self.rno)
                tablebuttons.append(tablebutton)
                self.cno += 2

class databasewin():
    def __init__(self,mycursor):
        self.cursor = mycursor
        self.finaldata = self.purify()
        self.datalen=len(self.finaldata)
        self.window()
        self.tableopen = False

    def purify(self):
        #variables
        output=[]
        ci=0
        ri=0
        unwanted=('information_schema', 'mysql', 'performance_schema', 'sakila', 'sys', 'world')
        self.cursor=conn.cursor()
        self.cursor.execute("Show databases;")
        databases=self.cursor.fetchall()
        noofdatabases=len(databases)
        cleardatabase = []
        for i in range(noofdatabases):
            if databases[i][0] not in unwanted:
                cleardatabase.append(databases[i][0])
        return cleardatabase

    def buttonpressed(self,selecteddatabase):
        global temptab
        if self.tableopen == False:
            self.tableopen = True
        else:
            temptab.pw.destroy()

        temptab = tablewin(selecteddatabase,self.cursor)

    def logout(self,window):
        global conn
        conn.close()
        window.destroy()
        loginwindow()
    
    def window(self):
        datawindow=Tk()
        datawindow.title("Available data ")
        datawindow.config(background=themeback)
        datawindow.state('zoomed')
        if self.datalen == 0:
            Label(datawindow,text="There are no databases to work on. \n To make a new database click on the button below",fg=fontcolor,bg=fontback,font="Agency_fb 20 bold").grid(column=0,row=0,columnspan=self.datalen)
        else:
            Label(datawindow,text="Select a database to work on \n",fg=fontcolor,bg=fontback,font="Agency_fb 20 bold").grid(column=0,row=0,columnspan=self.datalen)
            buttons = []
            cno = 0
            rno = 2
            for i in range(0,self.datalen):
                if cno > 3 :
                    cno = 0
                    rno += 1
                button = Button(datawindow,text = self.finaldata[i],width = 15, command = lambda i = i : self.buttonpressed(self.finaldata[i]))
                button.grid(column = cno, row = 2)
                cno += 1
                buttons.append(button)
        Button(datawindow, text = "Logout",width = 15,command = lambda: self.logout(datawindow)).grid(column = int(cno/2), row = 100)
        

        
log=loginwindow()
