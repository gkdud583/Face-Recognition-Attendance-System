
# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.ttk
import tkinter.font as font
import tkinter.messagebox
import MySQLdb

import os

from datetime import datetime







   

    
def attendance_management(root):
    am = Toplevel(root)
    am.title("출석관리")
    am.geometry("1000x800+140+140")
    la1 = Label(am,text='학번')
    myFont = font.Font(family='Helvetica', size=20, weight='bold')
    la1.place(height=100,width=150,x=55,y=5)
    la1['font']=myFont
    
    data1=Entry(am)
    data1.place(height=40,width=200,x=175,y=35)
    data1['font']=myFont
    data1.insert(0,"전체")
   
   
   
    
    la2 = Label(am,text="날짜")
    la2.place(height=100,width=150,x=395,y=5)
    la2['font']=myFont
    data2=Entry(am)
    data2.place(height=40,width=200,x=515,y=35)
    data2['font']=myFont
    data2.insert(0,"%s"%datetime.today().strftime("%Y-%m-%d"))
    def search_student():
        
        db = MySQLdb.connect(host="localhost",user="pi",password="raspberry",db="project",charset='utf8')
        cur = db.cursor(MySQLdb.cursors.DictCursor)
        get = datetime.strptime(data2.get(),"%Y-%m-%d")
       
        
        
        if(data1.get()=='전체'):
            
            sql = "select s.major,s.student_number,s.grade,s.name,a.time\
                   from student AS s\
                   JOIN attendance AS a\
                   where s.student_number = a.student_number AND a.date = %s"
          
            cur.execute(sql,(get,))
            while True:
                student = cur.fetchone()
                if not student: break
                treeview.insert('', 'end', text=student['major'], values=(student['student_number'],student['grade'],student['name'],"O",student['time']))
      
            sql = "select * from attendance where date=%s"
            cur.execute(sql,(get,))
            if(cur.fetchone()!=None):
            
                sql = "select s.major,s.student_number,s.grade,s.name\
                       from student AS s\
                       LEFT OUTER JOIN attendance AS a\
                       on s.student_number = a.student_number\
                       where a.student_number IS NULL"
                cur.execute(sql)
                while True:
                    student = cur.fetchone()
                    if not student: break
                    treeview.insert('', 'end', text=student['major'], values=(student['student_number'],student['grade'],student['name'],"X",""))    
          
            
            
            
        else:
            sql = "select s.major,s.student_number,s.grade,s.name,a.time\
                   from student AS s\
                   JOIN attendance AS a\
                   where s.student_number = %s AND s.student_number = a.student_number AND a.date=%s"
            cur.execute(sql,(int(data1.get()),get))
            student = cur.fetchone()
           
            if(student == None):
                sql = "select *\
                       from attendance\
                       where attendance.date =%s"
                cur.execute(sql,(get,))
                student = cur.fetchone()
                if(student != None):
                    sql = "select s.major,s.student_number,s.grade,s.name\
                           from student AS s\
                           where student_number = %s"
                    cur.execute(sql,(int(data1.get()),))
                    student = cur.fetchone()
                    treeview.insert('', 'end', text=student['major'], values=(student['student_number'],student['grade'],student['name'],"X","")) 
            
            else:
                treeview.insert('', 'end', text=student['major'], values=(student['student_number'],student['grade'],student['name'],"O",student['time']))
         
              
        
        
    bu=Button(am,text="검색",bg="steelblue",command=search_student)
    bu['font']=font.Font(family='Helvetica',size=15)
    bu.place(height=30,width=120,x=770,y=40)
    treeview = tkinter.ttk.Treeview(am,columns=["one","two","three","four","five"],displaycolumns=["one","two","three","four","five"],height=7)
    
    
    style = tkinter.ttk.Style()
    style.configure("Treeview.Heading", font=('Helvetica', 15 ,'bold'))
   
    treeview.column("#0",width=150)
    treeview.heading("#0",text="학과")

    treeview.column("#1",width=150,anchor="center")
    treeview.heading("#1",text="학번",anchor="center")

    treeview.column("#2",width=150,anchor="center")
    treeview.heading("#2",text="학년",anchor="center")

    treeview.column("#3",width=150,anchor="center")
    treeview.heading("#3",text="이름",anchor="center")

    treeview.column("#4",width=150,anchor="center")
    treeview.heading("#4",text="출석",anchor="center")

    treeview.column("#5",width=150,anchor="center")
    treeview.heading("#5",text="시간",anchor="center")


    


    

    scrollbar = Scrollbar(treeview)
    scrollbar.pack(side = RIGHT, fill=Y )  
    scrollbar.config(command = treeview.yview )

    treeview.place(height=600,width=902,x=50,y=100)
    
