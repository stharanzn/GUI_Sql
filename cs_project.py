#modules
from tkinter import *
import tkinter as tk
import mysql.connector as myc
import turtle
import time
import pickle

#variables
penrun=1

try:
    custommdata=open("customdata","rb")
    rawcustomdata=pickle.load(custommdata)
    print(rawcustomdata)
    custommdata.close()

except:
    rawcustomdata = ['black','white']
    customdata = open('customdata','wb')
    rawcustomdata=pickle.dump(rawcustomdata,customdata)
    customdata.close()
    print(rawcustomdata)

print(rawcustomdata,'2')
startapp=0
tbgcolor="yellow"
tfgcolor="red"
defthemebg="black"
defthemefg="white"
themebg=rawcustomdata[0]
themefg=rawcustomdata[1]

#welcome screen
welwin=turtle.Screen()
welwin.setup(height=540,width=550)
welwin.bgcolor("black")
welwin.tracer(0)

#gradience
pen=turtle.Turtle()
pen.color("red")
pen.speed(0)
pen.shape("triangle")
pen.right(90)
pen.penup()
pen.shapesize(stretch_len=100,stretch_wid=70)
pen.setposition(0,1500)

images=["sharanzyoo.gif"]
for image in images:
    turtle.register_shape(image) 

while True:
    welwin.update()   
    rantime=time.process_time()
    if penrun==True:
        pen.forward(1)
    if rantime==2.5 and rantime<3:
        welwin.bgcolor("red")
    if rantime>3:
        pen.shapesize(stretch_len=1,stretch_wid=1)
        penrun=False
    if rantime==3 and rantime<4:
        pen.hideturtle()
        ppen=turtle.Turtle()
        ppen.shape("sharanzyoo.gif")
    if rantime>4:
        pen.goto(-170,-200)
        pen.color("black")
        pen.write("Welcome to the sharanz codes ",font=("Agency fb",25,"bold"))
    if rantime>6:
        turtle.bye()
        startapp=0
        break

if startapp==0:
    """
    0] Create  a new table nad to save or not
    1]view contents of table
    -3] Update data in table
    4] Delete Table
    5] View list of tables
    -6] Insert code
    """
    mydb=myc.connect(
        host="localhost",
        user="root",
        passwd="Tiger@12",
        database='stharanzn'
        )
    mycursor=mydb.cursor()

    #variables
    tables=[]
    sqlcode="show tables"
    mycursor.execute(sqlcode)
    for db in mycursor:
        tables.append(db)
    columns=[]
    rows=[]
    columnnames=[]
    rownames=[]
    columntype="varchar"
    columnlen="30"

    ##commands
    def newtab():
        wn=Tk()
        wn.title("Select table specifications ")
        wn.config(background=themebg)
        wn.geometry("410x100")
        wn.resizable(0,0)

        Label(wn,bg=themebg,width=20).grid(row=0,column=0)
        Label(wn,bg=themebg,width=20).grid(row=0,column=1)
        Label(wn,bg=themebg,width=20).grid(row=0,column=2)
        Label(wn,bg=themebg,width=20).grid(row=0,column=3)
        Label(wn,bg=themebg,width=20).grid(row=0,column=4)
        Label(wn,bg=themebg,width=20).grid(row=0,column=5)

        def submitdata():
            global columns
            global rows
            columns=[]
            rows=[]

            global clen,rlen
            nrowlen=nrows.get()
            ncolumnlen=ncolumns.get()
            nrowlen.strip()
            ncolumnlen.strip()
            rlen=0
            clen=0
            try:
                rlen=int(nrowlen)
                clen=int(ncolumnlen)
                    
            except:
                if rlen==0 or type(nrowlen)==str or clen==0 or type(ncolumnlen)==str:
                    msg=Text(wn,width=40,height=2,wrap=WORD,background=themefg)
                    msg.grid(row=4,column=0,columnspan=3)
                    msg.delete(0.0,END)
                    msg.insert(END,"""Please enter a valid number
        for rows or columns""")
                    
            if type(rlen)==int and type(clen)==int and rlen!=0 and clen!=0:
                for r in range(0,rlen*clen):
                    rows.append(r)

                for i in range(0,clen):
                    columns.append(i)
                wn.destroy()
                showtable()
            else:
                pass

        Label(wn,text="Enter length of rows       ",bg=themebg,fg=themefg).grid(row=0,column=0)
        Label(wn,text="Enter length of columns",bg=themebg,fg=themefg).grid(row=1,column=0)
        nrows=(Entry(wn,width=20,bg=themebg,fg=themefg))
        nrows.grid(row=0,column=1)
        ncolumns=(Entry(wn,width=20,bg=themebg,fg=themefg))
        ncolumns.grid(row=1,column=1)
        Button(wn,text="submit",width=10,bg=themebg,command=submitdata).grid(row=1,column=2)

        def showtable():
            global columns
            tabwn=Tk()
            tabwn.title("Here's your table ")
            tabwn.config(background=themebg)
            toplace=0
            start=0
            end=rlen
            temp=end
            for i in range (0,clen):
                columns[i]=(Entry(tabwn,width=25,bg="white",fg = 'black'))
                columns[i].grid(row=2,column=i)
                if i==0:
                    pass
                else:
                    start=end
                    temp+=rlen
                    end=temp
                for j in range(start,end):
                    rows[j]=(Entry(tabwn,width=20,bg="white",fg = 'black'))
                    rows[j].grid(row=toplace+3,column=i)
                    toplace+=1
                    if j==end-1:
                        toplace=0
            tablename=(Entry(tabwn,width=20,bg='white',fg = 'black'))
            tablename.grid(row=0,column=int(i/2))
            
            def tabcreation():

                def savetab():
                    mydb.commit()
                    msg=Tk()
                    msg.config(background=themebg)
                    
                    Label(msg,text=tabname+" successfully saved to the database ",bg=themebg,fg=themefg,font="normal 12 bold").grid(row=0,column=0)
                    tabwn.destroy()
                global columnnames,rownames,columntype,columnlen,rowpos,cpos
                tables=[]
                sqlcode="show tables"
                mycursor.execute(sqlcode)
                for db in mycursor:
                    tables.append(db)
                tabname=tablename.get()
                tabname.strip()
                tabfound=2
                compare=0
                columnnames=[]
                rownames=[]
                toplace=0
                createtab=1
                tname="('"+tabname+"',)"
                for i in range(0,len(tables)):
                    ttname=tables[i]
                    tttname=ttname[0]
                    if tttname==tabname:
                        tabfound=1
                        
                if tabfound==1:
                    message=Text(tabwn,width=30,height=1,wrap=WORD,background="white")
                    message.grid(row=rlen+3,column=0,columnspan=3)
                    message.delete(0.0,END)
                    message.insert(END,"Tablename already exixts ")
                else:
                    tabfound=0
                    
                if tabfound==0:
                    for i in range(0,clen):
                        columnname=columns[i].get()
                        columnname.strip()
                        if columnname=='':
                            cno=i+1
                            columnname="column_%s "%cno  
                        columnnames.append(columnname)
                    for j in range(0,rlen*clen):
                        rowname=rows[j].get()
                        rowname.strip()
                        if rowname=='':
                            rowname="NULL"
                        rownames.append(rowname)
                    if len(columnnames)==clen and len(rownames)==rlen*clen:
                        createtab=0
                if tabfound==0 and createtab==0:
                    for i in range(0,clen):
                        if i==0:
                            sqlcode="create table if not exists "+tabname+" "+ "(" +columnnames[0]+ " " +columntype+"("+columnlen +")"+")"
                            mycursor.execute(sqlcode)
                        else:
                            sqlcode="alter table "+tabname+" add "+ columnnames[i] + " "+ columntype  + " (" + columnlen+");"
                            mycursor.execute(sqlcode)
                    for j in range(0,rlen*clen):
                        compare+=1
                        if j<rlen:
                            sqlcode=("insert into "+tabname+"("+columnnames[toplace]+") values (' " + rownames[j]+" ' )")
                            mycursor.execute(sqlcode)
                        else:
                            if toplace>1:
                                sqlcode=("update "+tabname+" set "+columnnames[toplace]+ " = ' " +rownames[j]+ " ' where "+columnnames[toplace-1]+" = ' "+rownames[j-rlen]+" '  and " + columnnames[toplace-2] + " = ' "+ rownames[j-rlen*2] +" ' ")
                                mycursor.execute(sqlcode)
                            else:
                                sqlcode=("update "+tabname+" set "+columnnames[toplace]+ " = ' " +rownames[j]+ " ' where "+columnnames[toplace-1]+" = ' "+rownames[j-rlen]+" ' ")
                                mycursor.execute(sqlcode)
                        if compare==rlen:
                            compare=0
                            toplace+=1
                    tables.append(tablename)
                    Button(tabwn,text="Save table values",command=savetab).grid(row=j+6,column=int(i/2))
                    rowpos=j+6
                    cpos=int(i/2)
                else:
                    pass

            Label(tabwn,bg=themebg).grid(row=j+4,column=0)
            Label(tabwn,text="Table name:-",bg=themebg,fg=themefg,font="normal 10 bold").grid(row=0,column=0,sticky=E)
            Button(tabwn,text="create table ",width=15,command=tabcreation).grid(row=j+5,column=int(i/2))

    #command2
    def viewndeltab():
        wn=Tk()
        wn.title("View and delete table")
        wn.config(background=themebg)

        outputs=[]
        tables=[]
        mycursor.execute("show tables")
        for i in mycursor:
            tables.append(i)
        for i in range(0,len(tables)):
            output=Text(wn,bg=themebg,fg=themefg,width=20,height=1,wrap=WORD)
            output.grid(row=i,column=0,columnspan=2)
            outputs.append(output)
            outputs[i].delete(0.0,END)
            outputs[i].insert(END,tables[i])

        Label(wn,text="Enter the table name ",bg=themebg,fg=themefg,font="normal 12 bold").grid(row=i+1,column=0)
        tabname=(Entry(wn,width=20,bg=themebg,fg=themefg))
        tabname.grid(row=i+1,column=1)

        def deltab():
            tables=[]
            mycursor.execute("show tables")
            for i in mycursor:
                tables.append(i)
            todeltabname=tabname.get()
            todeltabname.strip()
            tabfound=2
            for i in range(0,len(tables)):
                ttname=tables[i]
                tttname=ttname[0]
                if tttname==todeltabname:
                    tabfound=1

            if tabfound==1:
                Label(wn,text="Are you sure you want to delete the above table",bg=themebg,fg=themefg).grid(row=i+5,column=0,columnspan=2,sticky=W)
                def yup():
                    mycursor.execute("drop table "+todeltabname)
                    wn.destroy()
                    viewndeltab()

                def nope():
                    wn.destroy()
                    viewndeltab()

                v=tk.IntVar()
                rb1=Radiobutton(wn,variable=v,value=1,text="Yes",command=yup) .grid(row=i+6,column=0,sticky=W)
                rb2=Radiobutton(wn,variable=v,value=2,text="No",command=nope) .grid(row=i+6,column=0,sticky=E)
            else:
                Label(wn,text="This table doesnot exist",bg=themebg,fg=themefg).grid(row=2,column=0,columnspan=2,sticky=W)
        Button(wn,text="delete",bg=themebg,fg=themefg,command=deltab).grid(row=i+4,column=1)

        def view():
            tabtoshow=tabname.get()
            tabtoshow.strip()
            tabfound=2
            compare=0
            toplace=0
            tables=[]
            mycursor.execute("show tables")
            for i in mycursor:
                tables.append(i)
            for i in range(0,len(tables)):
                ttname=tables[i]
                tttname=ttname[0]
                if tttname==tabtoshow:
                    tabfound=1
            if tabfound==1:
                wn.destroy()
                wnn=Tk()
                wnn.config(background=themebg)
                wnn.title(tabtoshow)
                getcolumns=[]
                toshowcolumns=[]
                mycursor.execute("desc "+tabtoshow)
                for db in mycursor:
                    getcolumns.append(db)
                for i in range(0,len(getcolumns)):
                    toappend=getcolumns[i]
                    toshowcolumns.append(toappend[0])
                coutputs=[]
                for i in range(0,len(toshowcolumns)):
                    toappend=Text(wnn,width=20,height=1,wrap=WORD,background="white",font="normal 12 bold")
                    toappend.grid(row=0,column=i)
                    coutputs.append(toappend)
                for i in range(0,len(toshowcolumns)):
                    coutputs[i].delete(0.0,END)
                    coutputs[i].insert(END,toshowcolumns[i])
                sqlcode="select * from "+tabtoshow
                mycursor.execute(sqlcode)
                data=[]
                for db in mycursor:
                    data.append(db)

                rlen=len(data)
                add=0
                fdata=[]
                    
                for i in range(0,len(data[0])):
                    for j in range(0,rlen):
                        toadd=data[j]
                        rtoadd=toadd[add]
                        fdata.append(rtoadd)
                    add+=1

                outputs=[]
                for i in range(0,len(data[0])):
                    for j in range(0,len(data)):
                        put=Text(wnn,width=15,height=1,wrap=WORD,background="white")
                        put.grid(row=j+1,column=i)
                        outputs.append(put)
                for i in range(0,len(fdata)):
                    outputs[i].delete(0.0,END)
                    outputs[i].insert(END,fdata[i])
            else:
                Label(wn,text="The tablename you searched for doesnot exist ",bg=themebg,fg=themefg,font="normal 11 bold").grid(row=i+3,column=0,columnspan=3)
                    
        Button(wn,text="View",bg=themebg,fg=themefg,command=view).grid(row=i+4,column=0)

    #insert data
    def insertdata():
            wn=Tk()
            wn.config(background=themebg)
            wn.title("Insert or update data")

            outputs=[]
            tables=[]
            mycursor.execute("show tables")
            for i in mycursor:
                tables.append(i)
            for i in range(0,len(tables)):
                output=Text(wn,width=20,height=1,wrap=WORD,background="white")
                output.grid(row=i,column=0,columnspan=2)
                outputs.append(output)
                outputs[i].delete(0.0,END)
                outputs[i].insert(END,tables[i])

            Label(wn,text="Enter the table name in which you want to insert or update your new data ",bg=themebg,fg=themefg,font="normal 12 bold").grid(row=1,column=2)
            viewtabname=(Entry(wn,width=20,bg=themebg,fg=themefg))
            viewtabname.grid(row=2,column=2)
            tables=[]
            mycursor.execute("show tables")
            for db in mycursor:
                tables.append(db)

            def updating():
                tabfound=0
                toedit=viewtabname.get()
                toedit.strip()
                for i in range(0,len(tables)):
                    ttname=tables[i]
                    tttname=ttname[0]   
                    if tttname==toedit:
                        tabfound=1
                        pass
                    
                if tabfound==1:
                    wn.destroy()
                    wnn=Tk()
                    wnn.config(background=themebg)
                    wnn.title(toedit)
                    getcolumns=[]
                    toshowcolumns=[]
                    mycursor.execute("desc "+toedit)
                    for db in mycursor:
                        getcolumns.append(db)
                    for i in range(0,len(getcolumns)):
                        toappend=getcolumns[i]
                        toshowcolumns.append(toappend[0])
                    coutputs=[]
                    for i in range(0,len(toshowcolumns)):
                        toappend=Text(wnn,width=20,height=1,wrap=WORD,background="white",font="normal 12 bold")
                        toappend.grid(row=0,column=i)
                        coutputs.append(toappend)
                    for i in range(0,len(toshowcolumns)):
                        coutputs[i].delete(0.0,END)
                        coutputs[i].insert(END,toshowcolumns[i])
                    sqlcode="select * from "+toedit
                    mycursor.execute(sqlcode)
                    data=[]
                    for db in mycursor:
                        data.append(db)

                    rlen=len(data)
                    add=0
                    fdata=[]
                        
                    for i in range(0,len(data[0])):
                        for j in range(0,rlen):
                            toadd=data[j]
                            rtoadd=toadd[add]
                            rtoadd.lstrip()
                            fdata.append(rtoadd)
                        add+=1
                    outputs=[]
                    for i in range(0,len(data[0])):
                        for j in range(0,len(data)):
                            put=Text(wnn,width=15,height=1,wrap=WORD,background="white")
                            put.grid(row=j+1,column=i)
                            outputs.append(put)
                    for i in range(0,len(fdata)):
                        outputs[i].delete(0.0,END)
                        outputs[i].insert(END,fdata[i])
                    def insertrow():
                        global incre,editcolumns
                        editcolumns=[]
                        textt=["New data column name","New data","Reference data column name","Reference data"]
                        for k in range(0,4):
                            editcolumns.append(k)
                            editcolumns[k]=(Entry(wnn,width=20,bg="white",fg = 'black'))
                            Label(wnn,text=textt[k],bg=themebg,fg=themefg,font="normal 11 bold").grid(row=len(data)+1,column=k)
                            editcolumns[k].grid(row=len(data)+2,column=k)
                            
                    insertrow()

                    def update():
                        global editcolumns
                        incre=0
                        ndata=[]
                        updatedata=0
                        for c in range(0,len(editcolumns)):
                            val=editcolumns[c].get()
                            val.strip()
                            if val=='':
                                Label(wnn,text="Insufficient data",bg=themebg,fg=themefg,font="normal 11 bold").grid(row=20,column=0,columnspan=3)
                                break
                            else:
                                updatedata=1
                                ndata.append(val)

                        if updatedata==1:
                            try:
                                sqlcode="update "+toedit+" set "+ndata[0]+" = ' "+ndata[1]+" ' where "+ndata[2]+" = ' " +ndata[3]+ " ' ; "
                                mycursor.execute(sqlcode)
                                mydb.commit()

                                Label(wnn,text="The data has been updated succesfully ",fg=themefg,bg=themebg).grid(row=len(data)*2,column=0)
                                incre+=1
                            except:
                                Label(wnn,text="Reference data doesnot exist",bg=themebg,fg=themefg,font="normal 11 bold").grid(row=20,column=0,columnspan=3)
                        else:
                            Label(wnn,text="Reference data doesnot exist",bg=themebg,fg=themefg,font="normal 11 bold").grid(row=20,column=0,columnspan=3)
                    
                    Button(wnn,text="update",command=update).grid(row=len(data)*2,column=int(len(toshowcolumns)/2))
                        
                        
                else:
                    Label(wn,text="The tablename you searched for doesnot exist ",bg=themebg,fg=themefg,font="normal 11 bold").grid(row=4,column=0,columnspan=3)


            def insertion():
                global incre
                tabfound=0
                toedit=viewtabname.get()
                toedit.strip()
                for i in range(0,len(tables)):
                    ttname=tables[i]
                    tttname=ttname[0]   
                    if tttname==toedit:
                        tabfound=1
                        pass
                    
                if tabfound==1:
                    wn.destroy()
                    wnn=Tk()
                    wnn.config(background=themebg)
                    wnn.title(toedit)
                    getcolumns=[]
                    toshowcolumns=[]
                    mycursor.execute("desc "+toedit)
                    for db in mycursor:
                        getcolumns.append(db)
                    for i in range(0,len(getcolumns)):
                        toappend=getcolumns[i]
                        toshowcolumns.append(toappend[0])
                    coutputs=[]
                    for i in range(0,len(toshowcolumns)):
                        toappend=Text(wnn,width=20,height=1,wrap=WORD,background="white",font="normal 12 bold")
                        toappend.grid(row=0,column=i)
                        coutputs.append(toappend)
                    for i in range(0,len(toshowcolumns)):
                        coutputs[i].delete(0.0,END)
                        coutputs[i].insert(END,toshowcolumns[i])
                    sqlcode="select * from "+toedit
                    mycursor.execute(sqlcode)
                    data=[]
                    for db in mycursor:
                        data.append(db)

                    rlen=len(data)
                    add=0
                    fdata=[]
                        
                    for i in range(0,len(data[0])):
                        for j in range(0,rlen):
                            toadd=data[j]
                            rtoadd=toadd[add]
                            fdata.append(rtoadd)
                        add+=1

                    outputs=[]
                    for i in range(0,len(data[0])):
                        for j in range(0,len(data)):
                            put=Text(wnn,width=15,height=1,wrap=WORD,background="white")
                            put.grid(row=j+1,column=i)
                            outputs.append(put)
                    for i in range(0,len(fdata)):
                        outputs[i].delete(0.0,END)
                        outputs[i].insert(END,fdata[i])
                    incre=1
                    def insertrow():
                        global incre,editcolumns
                        editcolumns=[]
                        for k in range(0,len(data[0])):
                            editcolumns.append(k)
                            editcolumns[k]=(Entry(wnn,width=20,bg="white",fg = 'black'))
                            editcolumns[k].grid(row=len(data)+incre,column=k)
                        incre+=1
                    insertrow()
                    def insertsave():
                        global editcolumns,incre
                        ndata=[]
                        for c in range(0,len(editcolumns)):
                            val=editcolumns[c].get()
                            val.strip()
                            ndata.append(val)
                        if ndata[0]=="":
                            ndata[0]="NULL"
                        
                        sqlcode="insert into "+toedit+" (  "+toshowcolumns[0] +" ) values ( ' " + ndata[0]  + " ' ) ; "
                        mycursor.execute(sqlcode)

                        for e in range(1,len(toshowcolumns)):
                            if ndata[e]=='':
                                ndata[e]="NULL"
                            if e==1:
                                sqlcode="update " +toedit+ " set " + toshowcolumns[e] + " = ' " + ndata[e] + " '  where " +toshowcolumns[0]+" = ' " + ndata[0] + " ' ; "
                            else: 
                                sqlcode="update " +toedit+ " set " + toshowcolumns[e] + " = ' " + ndata[e] + " ' where  " +toshowcolumns[0]+" = ' " + ndata[0] + " ' and "+toshowcolumns[1] +" = ' " +ndata[1] +" ' ;"   
                            mycursor.execute(sqlcode)
                        mydb.commit()
                        Label(wnn,text="The data has been inserted succesfully ",fg=themefg,bg=themebg).grid(row=17,column=0)
                        incre+=1
                        Button(wnn,text="add another ",bg=themebg,fg=themefg,command=insertrow).grid(row=16,column=int(len(toshowcolumns)/2))
                    Button(wnn,text="save",command=insertsave).grid(row=17,column=int(len(toshowcolumns)/2))
                        
                else:
                    Label(wn,text="The tablename you searched for doesnot exist ",bg=themebg,fg=themefg,font="normal 11 bold").grid(row=4,column=0,columnspan=3)
            Button(wn,text="Add",command=insertion).grid(row=3,column=2)
            Button(wn,text="update",command=updating).grid(row=5,column=2)

    def deletedata():
        wn=Tk()
        wn.config(background=themebg)
        wn.title("Delete data")

        outputs=[]
        tables=[]
        mycursor.execute("show tables")
        for i in mycursor:
            tables.append(i)
        for i in range(0,len(tables)):
            output=Text(wn,width=20,height=1,wrap=WORD,background="white")
            output.grid(row=i,column=0,columnspan=2)
            outputs.append(output)
            outputs[i].delete(0.0,END)
            outputs[i].insert(END,tables[i])
        row=len(tables)
        
        Label(wn,text="Enter the table name in which you want to delete your new data ",bg=themebg,fg=themefg,font="normal 12 bold").grid(row=row,column=0)
        tabname=(Entry(wn,width=20,bg=themebg,fg=themefg))
        tabname.grid(row=row,column=1)

        def opentodeltab():
            tabtodel=tabname.get()
            tabtodel.strip()
            tabfound=2
            compare=0
            toplace=0
            tables=[]
            mycursor.execute("show tables")
            for i in mycursor:
                tables.append(i)
            for i in range(0,len(tables)):
                ttname=tables[i]
                tttname=ttname[0]
                if tttname==tabtodel:
                    tabfound=1
            if tabfound==1:
                wn.destroy()
                wnn=Tk()
                wnn.config(background=themebg)
                wnn.title(tabtodel)
                getcolumns=[]
                toshowcolumns=[]
                mycursor.execute("desc "+tabtodel)
                for db in mycursor:
                    getcolumns.append(db)
                for i in range(0,len(getcolumns)):
                    toappend=getcolumns[i]
                    toshowcolumns.append(toappend[0])
                coutputs=[]
                for i in range(0,len(toshowcolumns)):
                    toappend=Text(wnn,width=20,height=1,wrap=WORD,background="white",font="normal 12 bold")
                    toappend.grid(row=0,column=i)
                    coutputs.append(toappend)
                for i in range(0,len(toshowcolumns)):
                    coutputs[i].delete(0.0,END)
                    coutputs[i].insert(END,toshowcolumns[i])
                sqlcode="select * from "+tabtodel
                mycursor.execute(sqlcode)
                data=[]
                for db in mycursor:
                    data.append(db)

                rlen=len(data)
                add=0
                fdata=[]
                    
                for i in range(0,len(data[0])):
                    for j in range(0,rlen):
                        toadd=data[j]
                        rtoadd=toadd[add]
                        fdata.append(rtoadd)
                    add+=1

                outputs=[]
                for i in range(0,len(data[0])):
                    for j in range(0,len(data)):
                        put=Text(wnn,width=15,height=1,wrap=WORD,background="white")
                        put.grid(row=j+1,column=i)
                        outputs.append(put)
                for i in range(0,len(fdata)):
                    outputs[i].delete(0.0,END)
                    outputs[i].insert(END,fdata[i])
                Label(wnn,text="Enter the %s from the table to delete"%toshowcolumns[0],bg=themebg,fg=themefg,font="normal 11 bold").grid(row=i,column=0)
                todeldata=(Entry(wnn,width=20,bg=themebg,fg=themefg))
                todeldata.grid(row=i,column=1)

                def delrow():
                    deldata=todeldata.get()
                    deldata.strip()
                    datafound=2
                    sqlcode="select * from "+tabtodel
                    mycursor.execute(sqlcode)
                    data=[]
                    for db in mycursor:
                        data.append(db)
                    for i in range(0,len(data)):
                        ttname=data[i]
                        tttname=ttname[0].strip()
                        if tttname==deldata:
                            datafound=1
                    if datafound==1:
                        sqlcode="delete from "+tabtodel+" where "+toshowcolumns[0]+" = ' " + deldata +" ' ; "
                        mycursor.execute(sqlcode)
                        mydb.commit()
                        Label(wnn,text="The data had been deleted sucessfully ",bg=themebg,fg=themefg,font="normal 11 bold").grid(row=i+15,column=0)
                        wnn.destroy()
                        wnnn=Tk()
                        wnnn.title("Operation sucessful ")
                        wnnn.config(background=themebg)

                        Label(wnnn,text="The data has been sucessfully deleted",bg=themebg,fg=themefg,font="normal 11 bold").grid(row=0,column=0)
                    
                    else:
                        print(len(data))
                        Label(wnn,text="The data does not exist ",bg=themebg,fg=themefg,font="normal 11 bold").grid(row=len(data)+15,column=0)
                
                Button(wnn,text="Delete row",command=delrow).grid(row=i+4,column=1)
            else:
                Label(wn,text="The tablename you searched for doesnot exist ",bg=themebg,fg=themefg,font="normal 11 bold").grid(row=i+3,column=0,columnspan=3)            
        
        Button(wn,text="open table",command=opentodeltab).grid(row=i+4,column=1)

    def modify():
        wn=Tk()
        wn.title("Modify window")
        wn.config(background=themebg)
        def modify():
            themebg=userbg.get()
            themebg.strip()
            themefg=userfg.get()
            themefg.strip()
            rawcustomdata=[]
            rawcustomdata=[themebg,themefg]
            colours=["black","white","red","yellow","green","blue","purple","grey","orange"]
            if rawcustomdata[0] in colours and rawcustomdata[1] in colours:
                custom=open("customdata","wb")
                pickle.dump(rawcustomdata,custom)
                custom.close()
                wn.destroy()
            else:
                Label(wn,text="The colour you entered isnt available",bg=themebg,fg=themefg,font="normal 11 bold").grid(row=6,column=0)
        def default():
            rawcustomdata=[defthemebg,defthemefg]
            custom=open("customdata","wb")
            pickle.dump(rawcustomdata,custom)
            custom.close()
            wn.destroy()
        
        Label(wn,text="Enter the background colour you want for the window ",bg=themebg,fg=themefg,font="normal 11 bold").grid(row=0,column=0)
        Label(wn,bg=themebg).grid(row=1,column=0)
        Label(wn,text="Enter the text colour you want for the window ",bg=themebg,fg=themefg,font="normal 11 bold").grid(row=2,column=0)
        userbg=(Entry(wn,width=15,bg=themebg,fg=themefg))
        userbg.grid(row=0,column=1)
        userfg=(Entry(wn,width=15,bg=themebg,fg=themefg))
        userfg.grid(row=2,column=1)
        Button(wn,text="Customise",command=modify,bg=themebg,fg=themefg,font="normal 11 bold").grid(row=4,column=0)
        Button(wn,text="Restore to default",command=default,bg=themebg,fg=themefg,font="normal 11 bold").grid(row=5,column=0)

#=========================================================================================================================================#

    def mainscreen():
        screen=Tk()
        screen.config(background=themebg)
        screen.title("Menu")

        Label (screen,text="""Hey there welcome to my programme.

        Handle your database with a graphical user interface.

        Here you can do many things with mysql database
        Select from below which one you would like to do.""",bg=themebg,fg=themefg,font="none 15 bold") .grid(columnspan=3)
        
        Label(screen,bg=themebg,width=20).grid(row=1,column=0)
        Button(screen,text="Create a new table ",fg=themefg,bg=themebg,font="normal 11 bold",command=newtab,width=15).grid(row=2,column=0,columnspan=3)

        Label(screen,bg=themebg,width=20).grid(row=3,column=0)
        Button(screen,text="View/Delete table",fg=themefg,bg=themebg,font="normal 11 bold",command=viewndeltab,width=15).grid(row=4,column=0,columnspan=3)

        Label(screen,bg=themebg,width=20).grid(row=5,column=0)
        Button(screen,text="Insert / Update data",fg=themefg,bg=themebg,font="normal 11 bold",command=insertdata,width=15).grid(row=6,column=0,columnspan=3)

        Label(screen,bg=themebg,width=20).grid(row=7,column=0)
        Button(screen,text="Delete data",fg=themefg,bg=themebg,font="normal 11 bold",command=deletedata,width=15).grid(row=8,column=0,columnspan=3)

        Label(screen,bg=themebg,width=20).grid(row=9,column=0)
        Button(screen,text="Customise Window",fg=themefg,bg=themebg,font="normal 11 bold",command=modify,width=15).grid(row=10,column=0,columnspan=3)

    mainscreen()
else:
    pass
