
# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.ttk
import tkinter.font as font
import tkinter.messagebox
import MySQLdb
import face_dataset
import face_training
import face_recognition
import student_management
import attendance_management
import os

import photo_register
from pathlib import Path

from datetime import datetime










 

  



   

    



 

    
root = Tk()
root.title("출석관리시스템")
root.geometry("600x600+100+100")
myFont = font.Font(family='Helvetica', size=30, weight='bold')


b1 =Button(root,text='학생관리',activebackground = "#0052cc",activeforeground='#ffffff',width=50,command=lambda:student_management.student_management(root))
b2 =Button(root,text='출석관리',activebackground = "#0052cc",activeforeground='#ffffff',width=50,command=lambda:attendance_management.attendance_management(root))
b3 =Button(root,text='출석하기',activebackground = "#0052cc",activeforeground='#ffffff',width=50,command=lambda:face_recognition.face_recognition())
b4 =Button(root,text='사진등록',activebackground = "#0052cc",activeforeground='#ffffff',width=50,command=lambda:photo_register.photo_registration(root))

b1['font'] = myFont
b2['font'] = myFont
b3['font'] = myFont
b4['font'] = myFont
b1.place(height=300,width=300,x=0,y=0)
b2.place(height=300,width=300,x=300,y=0)
b3.place(height=300,width=300,x=0,y=300)
b4.place(height=300,width=300,x=300,y=300)

      
root.mainloop()
