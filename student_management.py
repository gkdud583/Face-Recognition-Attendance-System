
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






 
def student_management(root):
    sm = Toplevel(root)
    sm.title("학생관리")
    
    sm.geometry("1000x800+150+150")
    sm.resizable(False,False)
    la1 = Label(sm,text='학번')
    myFont = font.Font(family='Helvetica', size=20, weight='bold')
    la1.place(height=100,width=150,x=250,y=5)
    la1['font']=myFont
    
    data1=Entry(sm)
    data1.place(height=40,width=200,x=400,y=35)
    data1['font']=myFont
    data1.insert(0,"전체")
    def search_student():
        if(data1.get()=="전체"):
            sql = "select * from student"
            cur.execute(sql)
            
            while(True):
                student = cur.fetchone()
                if not student: break
                treeview.insert('', 'end', text=student['major'], values=(student['student_number'],student['grade'],student['name']))
        else:
            sql = "select * from student where student_number = %s"
            cur.execute(sql,(int(data1.get()),))
            student = cur.fetchone()
            if(student == None):
                tkinter.messagebox.showwarning("알림","정보를 찾을 수 없습니다.",parent=sm)
            else:
                treeview.insert('', 'end', text=student['major'], values=(student['student_number'],student['grade'],student['name']))
    bu=Button(sm,text="검색",bg="steelblue",command=search_student)
    bu['font']=font.Font(family='Helvetica',size=15)
    bu.place(height=40,width=100,x=630,y=35)

    
    
  
    treeview = tkinter.ttk.Treeview(sm,columns=["one","two","three","four"],displaycolumns=["one","two","three","four"])

    
    style = tkinter.ttk.Style()
    style.configure("Treeview.Heading", font=('Helvetica', 15 ,'bold'))
   
    treeview.column("#0",width=200)
    treeview.heading("#0",text="학과")

    treeview.column("#1",width=200,anchor="center")
    treeview.heading("#1",text="학번",anchor="center")

    treeview.column("#2",width=200,anchor="center")
    treeview.heading("#2",text="학년",anchor="center")

    treeview.column("#3",width=200,anchor="center")
    treeview.heading("#3",text="이름",anchor="center")

    

    scrollbar = Scrollbar(treeview)
    scrollbar.pack(side = RIGHT, fill=Y )  
    scrollbar.config(command = treeview.yview )

    treeview.place(height=600,width=802,x=70,y=100)
    

    #데이터삽입

    bottom_b1 =Button(sm,text="추가",bg="steelblue",command=lambda:insert_student(root))
    bottom_b1['font']=font.Font(family='Helvetica',size=15)
    bottom_b1.place(height=40,width=100,x=90,y=745)


    bottom_b2 =Button(sm,text="수정",bg="steelblue",command=lambda:update_student(root))
    bottom_b2['font']=font.Font(family='Helvetica',size=15)
    bottom_b2.place(height=40,width=100,x=420,y=745)
    

    bottom_b3 =Button(sm,text="삭제",bg="steelblue",command=lambda:delete_student(root))
    bottom_b3['font']=font.Font(family='Helvetica',size=15)
    bottom_b3.place(height=40,width=100,x=720,y=745)
  
def insert_student(root):
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
    
    def err_c():
        sql = "insert into student values(%s,%s,%s,%s)"
        cur.execute(sql,(int(data1.get()),data2.get(),int(data3.get()),data4.get()))
        db.commit()
       

        sql = "select picture_count from picture where student_number = %s"
   
        cur.execute(sql,(int(data1.get()),))
        student = cur.fetchone()
        
        face_dataset.face_dataset(data1.get(),0)
        sql = "insert into picture values(%s,%s)"
        cur.execute(sql,(30,int(data1.get())))
      
        db.commit()
        tkinter.messagebox.showinfo("알림","학생 등록되었습니다",parent=sm)
    bu=Button(sm,text="사진등록",bg="steelblue",command=lambda: err_c())
    bu['font']=font.Font(family='Helvetica',size=15)
    bu.place(height=30,width=120,x=90,y=295)

 
 
    
def update_student(root):
    
    sm = Toplevel(root)
    sm.title("학생수정")
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


    def process_update():
        sql = "update student set major=%s,grade=%s,name=%s where student_number = %s"
        cur.execute(sql,(data2.get(),int(data3.get()),data4.get(),int(data1.get())))
        tkinter.messagebox.showinfo("알림","저장되었습니다",parent=sm)
        db.commit()
                    
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
         
                  
    
    bu=Button(sm,text="저장하기",bg="steelblue",command=process_update)
    bu['font']=font.Font(family='Helvetica',size=15)
    bu.place(height=30,width=120,x=90,y=295)
   
    bu=Button(sm,text="검색",bg="steelblue",command=process_search)
    bu['font']=font.Font(family='Helvetica',size=15)
    bu.place(height=30,width=70,x=220,y=5)
   
   

    


   
   
    

def delete_student(root):
    sm = Toplevel(root)
    sm.title("학생삭제")
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


    def process_delete():
        sql = "delete from student where student_number =%s"
        cur.execute(sql,(int(data1.get()),))
        for p in Path("/home/pi/fdCam/dataset").glob("User."+data1.get()+".*.jpg"):
            p.unlink()
        db.commit()
        Path("/home/pi/fdCam/trainer/").glob("trainer.yml")
        
        tkinter.messagebox.showinfo("알림","삭제되었습니다",parent=sm)
        face_training.face_training()
       
                    
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
                  
    
    bu=Button(sm,text="삭제하기",bg="steelblue",command=process_delete)
    bu['font']=font.Font(family='Helvetica',size=15)
    bu.place(height=30,width=120,x=90,y=295)
   
    bu=Button(sm,text="검색",bg="steelblue",command=process_search)
    bu['font']=font.Font(family='Helvetica',size=15)
    bu.place(height=30,width=70,x=220,y=5)
  
