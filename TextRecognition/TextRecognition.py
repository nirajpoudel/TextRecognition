from tkinter import*
from PIL import ImageTk,Image
from tkinter import Frame
from tkinter import ttk
from tkinter import Tk, filedialog
import cv2
import json
import io
import numpy as np
import requests

class HomePage(Frame):
    def __init__(self,master):
        self.master=master
        self.frame = Frame(master,bg='white')
        title = Label(master,text='Text Recognization',font=('times new roman',18,'bold'),bg='white',fg='black')
        title.place(x=0,y=0,relwidth=1)
        home_frame = Frame(master,bg='white')
        home_frame.place(x=20,y=100)
        
        self.select = Button(master,text='Select Image', font=("arial", 13, "bold"), bg="green", fg='white',command=self.read_image)
        self.select.place(x=180,y=330)
        self.canvas = Canvas(master, width= 350, height=250, bg="#fffdd0")
        self.canvas.place(x=70,y=60)
        
        self.canvas1 = Canvas(self.master, width= 455, height=280, bg="#fffdd0")
        self.canvas1.place(x=25,y=390)


    def read_image(self):
        global file_path
        file_path = filedialog.askopenfilename()
        des = Image.open(file_path)
        des.thumbnail((350,300),Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(des)
        self.canvas.bg_image = bg_image
        self.canvas.create_image(100, 120, image=self.canvas.bg_image)
        print(file_path)
        
        img = cv2.imread(file_path)
        
        url_api = "https://api.ocr.space/parse/image"
        _,compressedimage = cv2.imencode(".jpg", img, [1, 90])
        file_bytes = io.BytesIO(compressedimage)
        print(file_bytes)


        result = requests.post(url_api,
        files = {file_path: file_bytes},
        data = {"apikey": "f8be178b5888957",
                      "language": "eng"})

        result = result.content.decode()
        result = json.loads(result)
        print(result)

        parsed_results = result.get("ParsedResults")[0]
        text_detected = parsed_results.get("ParsedText")
        print(text_detected)

        lbl = Label(self.canvas1,text=text_detected,bg='#fffdd0',fg='black')
        lbl.config(font=("Courier", 8))
        lbl.place(x=5,y=5)
        



root = Tk()
root.title('Text')
root.geometry('500x700')
HomePage(root)
root.configure(bg="white")
root.mainloop()
