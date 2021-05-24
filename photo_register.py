
# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.ttk
import tkinter.font as font
import tkinter.messagebox
import MySQLdb
import face_dataset
import face_training
import face_recognition
import os
from pathlib import Path

from datetime import datetime

db = MySQLdb.connect(host="localhost",user="pi",password="raspberry",db="project",charset='utf8')
cur = db.cursor(MySQLdb.cursors.DictCursor)





   

    

def photo_registration(root):
    sm = Toplevel(root)
    sm.title("학생등록")
    sm.geometry("300x350+150+150")
    la1 = Label(sm,text='학번')
    myFont = font.Font(family='Helvetica', size=15, weight='bold')
    la1.place(height=30,width=40,x=30,y=5)
    la1['font']=myFont
    data1=Entry(sm)
    data1.place(height=30,width=120,x=90,y=5)
    data1['font']=myFont


    la2 = Label(sm,text='학과')
    myFont = font.Font(family='Helvetica', size=15, weight='bold')
    la2.place(height=30,width=40,x=30,y=85)
    la2['font']=myFont
    data2=Entry(sm)
    data2.place(height=30,width=120,x=90,y=85)
    data2['font']=myFont

    la3 = Label(sm,text='학년')
    myFont = font.Font(family='Helvetica', size=15, weight='bold')
    la3.place(height=30,width=40,x=30,y=165)
    la3['font']=myFont
    data3=Entry(sm)
    data3.place(height=30,width=120,x=90,y=165)
    data3['font']=myFont

    la4 = Label(sm,text='이름')
    myFont = font.Font(family='Helvetica', size=15, weight='bold')
    la4.place(height=30,width=40,x=30,y=245)
    la4['font']=myFont
    data4=Entry(sm)
    data4.place(height=30,width=120,x=90,y=245)
    data4['font']=myFont
    def process_search():
        
        sql = "select * from student where student_number = %s"
        cur.execute(sql,(int(data1.get()),))
        student = cur.fetchone()
        if(student==None):
            tkinter.messagebox.showwarning("알림","정보를 찾을 수 없습니다",parent=sm)
        else:
            data2.insert(0,"%s"%student['major'])
            data3.insert(0,"%s"%student['grade'])
            data4.insert(0,"%s"%student['name'])
         
                  
    
  
   
    def err_c():
      

        sql = "select picture_count from picture where student_number = %s"
   
        cur.execute(sql,(int(data1.get()),))
        student = cur.fetchone()
       
      
        face_dataset.face_dataset(data1.get(),student['picture_count'])
        c=int(student['picture_count'])
        sql = "update picture set picture_count=%s where student_number=%s"
        cur.execute(sql,(c+30,int(data1.get())))
      
        db.commit()
        tkinter.messagebox.showinfo("알림","사진이 추가 등록되었습니다.",parent=sm)
    bu=Button(sm,text="검색",bg="steelblue",command=process_search)
    bu['font']=font.Font(family='Helvetica',size=15)
    bu.place(height=30,width=70,x=220,y=5)
   
   
    bu=Button(sm,text="사진등록",bg="steelblue",command=lambda: err_c())
    bu['font']=font.Font(family='Helvetica',size=15)
    bu.place(height=30,width=120,x=90,y=295)
