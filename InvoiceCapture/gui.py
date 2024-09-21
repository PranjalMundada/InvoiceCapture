# -*- coding: utf-8 -*-
import os
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import Listbox, Menu, Scale, Radiobutton, Checkbutton, messagebox
from ocr import OCR
from fetcher import Attachement_Fetcher
from GPT import GPT
import requests
import shutil
from html2image import Html2Image

#os.environ['KMP_DUPLICATE_LIB_OK']='False'

class GUI:
    
    
    def __init__(self):
        
        self.root_window = tk.Tk()
        self.root_window.title("Invoice, Health Insurance Claim, Balance sheet Analyser and Processer")
        self.root_window.geometry('1250x780')
        self.root_window.resizable(tk.FALSE, tk.FALSE)
        
        ''' MENU '''
        self.menu = Menu(self.root_window)
        self.root_window.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='New')
        self.filemenu.add_command(label='Open...')
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.root_window.quit)
        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=self.helpmenu)
        self.helpmenu.add_command(label='About')
    
    
        ''' PANEL SECTION '''
        self.url_panel       = tk.Frame(self.root_window, bd=1,  relief="flat", background = self.root_window.cget("background"))
        self.doc_type_panel  = tk.Frame(self.root_window,  bd=1, relief="groove", background = self.root_window.cget("background"))
        self.main_panel      = tk.Frame(self.root_window, height = 400)
        self.question_panel  =tk.Frame(self.root_window)
        self.footer_panel    = tk.Frame(self.root_window)

        self.url_panel.pack()
        self.doc_type_panel.pack()
        self.main_panel.pack(fill = tk.BOTH)  
        self.question_panel.pack()  
        self.footer_panel.pack(fill = tk.BOTH)
        
         
        ''' URL PANEL CONSTRUCT '''
        self.url_label       = tk.Label(self.url_panel, text = 'URL :')
        self.url_text_field  = tk.Entry(self.url_panel, text = 'https://google.com', font = ('arial', 13), width = 90)
        #self.url_text_field.insert(0, 'https://google.com')
        self.fetch_button    = tk.Button(self.url_panel, text = "Fetch", pady=2, width  = 15, relief="raised",  bg='#009696', activebackground='gray', command = self.fetch_button_clicked)
        self.gmail_fetch_button   = tk.Button(self.url_panel, text = "Start Gmail Fetch", pady=2, width  = 13, bg='#009696', command = self.gmail_fetch_button_clicked) 
        
        self.url_label.grid(row = 0, column = 0)
        self.url_text_field.grid(row = 0, column = 1)
        self.fetch_button.grid( row = 0, column = 2)
        self.gmail_fetch_button.grid( row = 0, column = 3)
        
        ''' DOC TYPE FRAME '''
        self.radio = tk.IntVar()
        self.R1 = Radiobutton(self.doc_type_panel, text="Invoice", variable= self.radio, value=1, command = self.radio_button_selected )  
        self.R1.pack(fill='x', padx=5, pady=5, side=tk.LEFT)  
        self.R2 = Radiobutton(self.doc_type_panel, text="Health Insurance Claim", variable=self.radio, value=2, command = self.radio_button_selected)  
        self.R2.pack(fill='x', padx=5, pady=5, side=tk.LEFT)  
        self.R3 = Radiobutton(self.doc_type_panel, text="Balance Sheet", variable=self.radio, value=3, command = self.radio_button_selected)  
        self.R3.pack( fill='x', padx=5, pady=5, side=tk.RIGHT)  
        
        #self.R2.set(0)
        self.R1.deselect()
        self.R2.deselect()
        self.R3.deselect()
        print(self.radio.get())
        
        #print('Value of Radio is :', self.radio.get())
        
        ''' MAIN PANEL CONSTRUCT '''
        #self.listbox = Listbox(self.main_panel, bg = "light grey",font = "Helvetica", borderwidth = 1, selectmode=SINGLE)
        #self.listbox.bind('<<ListboxSelect>>', self.process_selected_image)
        #self.listbox.pack(fill = tk.BOTH, padx=5, pady=5, side = tk.LEFT, expand=tk.FALSE)
        
        self.listbox_border = tk.Frame(self.main_panel, width=200, height=500, bd=1, relief="sunken", background="white")
        self.listbox_border.pack( side = tk.LEFT,  padx=5, pady=5, fill=tk.BOTH, expand=tk.FALSE)
        
        
        self.listbox = tk.Listbox(self.listbox_border, width=20, height=10,
                             borderwidth=0, highlightthickness=0,
                             background=self.listbox_border.cget("background"),
        )
        self.listbox.bind('<<ListboxSelect>>', self.process_selected_image)

        self.vsb = tk.Scrollbar(self.listbox_border, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.vsb)
        self.vsb.pack(side="right", fill="y")
        self.listbox.pack(padx=10, pady=10, fill="both", expand=True)
        
        for i in range(10):
            self.listbox.insert("end", "Item #{}".format(i))

        #self.listbox.grid( row = 0, column = 0, sticky='w', padx=10,pady=10,columnspan=1)
        
        self.image_frame = tk.Frame(self.main_panel, bd=1, relief="sunken", background="white")
        self.image_frame.pack(fill = tk.BOTH, padx=5, pady=5, side = tk.LEFT, expand=tk.FALSE)
        

        self.xscrollbar = tk.Scrollbar(self.image_frame, orient=tk.HORIZONTAL, bg = 'gray')
        self.xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.yscrollbar = tk.Scrollbar(self.image_frame, elementborderwidth = 2, repeatdelay = 100, width = 10, bg='red',troughcolor = 'blue', orient="vertical")
        self.yscrollbar.pack(side="right", fill=tk.Y)

        
        self.canvas = tk.Canvas(self.image_frame, bd=0, xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set, width=300, height=300)
        
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH) # grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        self.canvas.bind("<B1-Motion>", self.move)
        
        #File = "res/images/handtext.png"
        #img = ImageTk.PhotoImage(Image.open(File))
        
        image = Image.open('res/images/handtext.png')
        image = image.resize((400, 600))
        img = ImageTk.PhotoImage(image)
        
        #print (img.width(), ' ' ,img.height())
        
        self.canvas.config(width = img.width(), height = img.height())
        self.imageContainer = self.canvas.create_image(0,0,image=img, anchor="nw")
        
        self.xscrollbar.config(command=self.canvas.xview)
        self.yscrollbar.config(command=self.canvas.yview)
        
        
        '''
        image = Image.open('res/images/handtext.png')
        image = image.resize((400, 600))
        self.image_tk = ImageTk.PhotoImage(image)

        self.vsb_image_x = tk.Scrollbar(self.image_frame, orient=tk.HORIZONTAL)
        self.vsb_image_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.vsb_image_y = tk.Scrollbar(self.image_frame, orient=tk.VERTICAL)
        self.vsb_image_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        #self.image_label.grid( row = 0, column = 1, sticky='w', padx=10,pady=10, columnspan=2)
        #self.image_label.configure(yscrollcommand=self.vsb_image)
        self.image_label = tk.Label(self.image_frame, image=self.image_tk, bg = 'white', xscrollcommand=self.vsb_image_x.set, yscrollcommand=self.vsb_image_y.set)
        self.image_label.pack(fill = tk.BOTH, padx=5, pady=5, side = tk.LEFT, expand=tk.TRUE)
        
        
        self.vsb_image_x.config(command=self.image_label.xview)
        self.vsb_image_y.config(command=self.image_label.yview)
        
        '''
        
        self.response_frame = tk.Frame(self.main_panel, bd=1, relief="sunken", background="white")
        self.response_frame.pack(fill = tk.BOTH, padx=5, pady=5, side = tk.LEFT, expand=tk.FALSE)

        self.response_box  = tk.Text(self.response_frame)
        #self.response_box.grid( row = 0, column = 3, sticky='w', padx=10,pady=10, columnspan=2)
        self.response_box.pack(fill = tk.BOTH, padx=5, pady=5,side = tk.LEFT, expand=tk.FALSE)
        
        path="attachments"
        
        dir_list = os.listdir(path)
        
        list=[]
        count = 0
        for item in dir_list:
            list.append(item)
            self.listbox.insert(count, item)
            count = count +1
        print(list)    
        
        
        ''' QUESTION PANEL CONSTRUCT '''
        self.Checkbutton1 = tk.IntVar()
        self.Checkbutton2 = tk.IntVar()  
        self.Checkbutton3 = tk.IntVar()
        self.Checkbutton4 = tk.IntVar()

        
        self.ocr_button   = tk.Button(self.question_panel, text = "Convert Image to Text", pady=2, width  = 16, relief="raised", command = self.ocr_button_clicked)
        self.ocr_button.grid(row = 0, column = 0, columnspan = 1 )

        self.check_panel = tk.Frame(self.question_panel, relief="groove", background = self.root_window.cget("background") , width = 100)
        self.check_panel.grid(row = 0, column = 1, columnspan = 2 )
          
        self.check_button_1 = Checkbutton(self.check_panel, text = "Validate Total", variable = self.Checkbutton1, onvalue = 1, offvalue = 0, width=13)
        self.check_button_2 = Checkbutton(self.check_panel, text = "Validate Tax", variable = self.Checkbutton2, onvalue = 1, offvalue = 0 , width=13)
        self.check_button_3 = Checkbutton(self.check_panel, text = "Get Due Date", variable = self.Checkbutton3, onvalue = 1, offvalue = 0, width=13)
        self.check_button_4 = Checkbutton(self.check_panel, text = "Find Duplicate", variable = self.Checkbutton4, onvalue = 1, offvalue = 0, width=13)
        self.check_button_1.pack(side = tk.LEFT)
        self.check_button_2.pack(side = tk.LEFT)
        self.check_button_3.pack(side = tk.LEFT)
        self.check_button_4.pack(side = tk.LEFT)
        
        self.standard_question_button   = tk.Button(self.question_panel, text = "Standard Questions", pady=2, width  = 15, relief="raised", command = self.standard_question_clicked)
        self.clear_response_button   = tk.Button(self.question_panel,text = "Clear Responses", pady=2, width  = 15, command = self.clear_response_button_clicked )

        self.standard_question_button.grid(row = 0, column = 3)        
        self.clear_response_button.grid(row = 0, column = 4)        
         
        self.question_title  =  tk.Label(self.question_panel, text = "Custom question :")
        self.custom_question_field    =  tk.Entry(self.question_panel, font = ('arial', 15), width = 70)
        self.custom_question_button   = tk.Button(self.question_panel,text = "Submit", pady=2, width  = 15, command = self.custom_question_button_clicked)
        
        self.question_title.grid(row = 1, column = 0)
        self.custom_question_field.grid(row=1,column=1, columnspan = 1)
        self.custom_question_button.grid(row = 1, column = 3) 
        
        
        
        self.post_to_system_button   = tk.Button(self.question_panel,text = "Post To System", pady=2, width  = 15, command = self.post_to_system_button_clicked)
        self.post_to_system_button.grid(row = 1, column = 4) 

        self.status_label    = tk.Label(self.footer_panel, text = 'Status :') 
        self.status_label    = tk.Label(self.footer_panel, text = '') 
        self.status_label.pack(side = tk.LEFT)
        self.status_label.pack(side = tk.LEFT)
        self.footer_panel.pack()
        
        self.root_window.mainloop()
        
            
    def move(self, e):
        step=5 
        x1,y1=5
        x2,y2=x1+15,y1+15
        r1=self.canvas.create_rectangle(x1, y1, x2,y2,fill='red')  # draw rectangle 
        self.canvas.move(r1,step,step) # increase x and y both, move right-down

    
    def radio_button_selected(self):
        type(self.radio)
        print('Radiobutton  value :',self.radio.get())
        
    def ocr_button_clicked(self):
        print('ocr_button_clicked')
        self.ocr_response = ''
        file_name = 'attachments/'+self.listbox.get(self.listbox.curselection())
        print(file_name)
        self.ocr_response = self.do_ocr(file_name)
        print(self.ocr_response)
        
        #self.response_box.delete(tk.START,tk.END)
        self.response_box.insert(tk.END,"############ OCR Containt ###############")

        self.response_box.insert(tk.END,self.ocr_response)
        self.response_box.insert(tk.END,"\n----------------------------------------------------\n")
        
        print("111")
        
        if self.ocr_response != '':
            tk.messagebox.showinfo(title='Image Proccessed', message='Image has been processed successfully. You can ask questions now' )
        else:
            tk.messagebox.showinfo(title='Image Not Proccessed', message='Image NOT proccessed sucessfully' )
   
        

    def standard_question_clicked(self):

        print("Radio  value is : ", self.radio.get())
        
        #self.ocr_response = self.do_ocr()
        #" ".join(flexiple)
            
        print(type(self.ocr_response))
        
        qr = self.ocr_response
        
        if self.radio.get() == 1:
          
            qr = "Following is the invoice : " + qr # " ".join(self.ocr_response)
        
            if self.Checkbutton1.get()  == 1:
                str = 'Please validate total of the invoice in mathematical format.' 
                qr = qr + str
                    
            if self.Checkbutton2.get()  == 1:
                str = 'Please validate tax also.'
                qr = qr + str
          
            if self.Checkbutton3.get()  == 1:
                str ='Is due date greater than invoice date?' 
                qr = qr + str
          
            if self.Checkbutton4.get()  == 1:       
                str = 'Are there any duplicate line items in the Invoice?'
                qr = qr + str
            
      
        #qr = "Please validate total of following invoice in mathematical format: " + " ".join(self.ocr_response)
        rs = self.gpt(qr)
        
        self.response_box.insert(tk.END,"############ Response to Question ###############\n")
        self.response_box.insert(tk.END,rs)
        
    def do_ocr(self, fileName):
        print(fileName)
        ocr = OCR()
        res1 = ocr.recognize(fileName)
        #formatted_res = '{} '.format(res1)  
        formatted_res = " ".join(res1)

        return formatted_res
        
        
        
    def gpt(self, question): 
        gpt = GPT();
        return gpt.chatgpt_conversastion(question)
        #result =  self.gpt_chat(question )
        #self.response_box.delete("start","end")
        #self.response_box.insert(tk.INSERT,result)
        

    def new_document_received(self, file_name):
        self.listbox.append(file_name)
        tk.messagebox.showinfo(title='No URL', message="Did not provided URL", iconbitmap='res/images/messagebox_info_icon.png' )

        #refresh image sin list box
    
    def process_selected_image(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        #n = lst.curselection()
        file_name = "attachments/"+value
        #file_nmae = "res/images/handtext.png"
        
        
        print(file_name)
        image = Image.open(file_name)
        image = image.resize((400, 600))
        self.img = ImageTk.PhotoImage(image)
        
        print (self.img.width(), ' ' ,self.img.height())
 
        print( ' point 4 ') 
        
        #self.canvas.configure(image = file_name)
        #self.canvas.imgref = img
        
        #self.image_on_canvas = self.canvas.create_image(10, 10, anchor='nw', image = img)

        self.canvas.itemconfig(self.imageContainer, image = self.img)

        print( ' point 5') 
        
        #self.image_label.image=img
        print("Show image done")

        
        
        #img = tk.PhotoImage(file="attachments/"+value)
        
        #self.image_label = tk.Label(self.p1, image=img, bg = 'white')
        #self.image_label.pack(fill = tk.BOTH, padx=5, pady=5, side = tk.LEFT, expand=tk.FALSE)
    
        #self.image_label.configure(image = img)
        #self.image_label.image=img
        #print("Show image done")
        
        #self.do_ocr(file_name)
       
        
    def fetch_button_clicked(self):
        print("fetch button clicked")
        url = self.url_text_field.get()
        print(":",url,":")

        if url.startswith('https://') or url.startswith('file://'):
            print("Inside of if loop")

            self.image_from_url(url)
            #htmltoimage = MyHTMLToImage()
            #htmltoimage.url2Image( url, "attachements/downloadedpage.png")
       
            hti = Html2Image()
            hti.screenshot(url='https://www.python.org', save_as='python_org.png')
        
            #matter = do_ocr(file_name)
            #print(matter)
        else :
            print("Inside of else loop")
            tk.messagebox.showinfo(title='No URL', message="Did not provided URL" )
            

    def gmail_fetch_button_clicked(self):
        print("Gmail_fetch_button_clicked button clicked")
        
        if self.gmail_fetch_button.cget('text') == "Start Gmail Fetch" :
            print('')
            # START IMAGE FETCHER 
            self.fetcher = Attachement_Fetcher(self) 
            self.fetcher.start_fetching()
            print(self.fetcher)
            self.gmail_fetch_button.config(text = "STOP Gmail Fetch", bg='gray', fg='red')

        else :
            print('')
            # STOP IMAGE FETCHER 
            self.fetcher.stop_fetching()
            self.gmail_fetch_button.config(text = "Start Gmail Fetch", bg='white', fg='black')
            
        
    def clear_response_button_clicked(self):
        print("")
        self.response_box.delete('1.0', tk.END)

    def post_to_system_button_clicked(self):
        print("post_to_system_button_clicked ")
        question_string = "Get all data in JSON format from :" +" ".join(self.ocr_response)+ ". and only show JSON "
        rs = self.gpt(question_string)
        self.response_box.insert(tk.END,"\n ####### This Document has been posted with below JSON Object ##########\n")
        self.response_box.insert(tk.END,rs)
        
    def custom_question_button_clicked(self):
        print("")
        custom_question = self.custom_question_field.get()
        question_string = "please answer " + custom_question +" using follwoing data :" +" ".join(self.ocr_response)
        self.custom_question_field.delete('0', tk.END)
        
        rs = self.gpt(question_string)
        self.response_box.insert(tk.END,"\n ############ ANSWER TO YOUR QUESTION IS ###############\n")
        self.response_box.insert(tk.END,rs)
  
        
    def image_from_url(self, url):
        
        file_name = "images/images_p.png"
        
        hti = Html2Image()
        hti.screenshot(url, save_as=file_name)

        res = requests.get(url, stream = True)
        
        if res.status_code == 200:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ',file_name)
        else:
            print('Image Couldn\'t be retrieved')
          

    
gui = GUI()
