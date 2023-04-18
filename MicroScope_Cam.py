#MicroScope CMOS Camera Viewer with Scale-Bar
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk, ImageOps  #

class Application(tk.Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)

        self.pack()

        self.master.title("MicroScope CMOS Camera Viewer(NY-CZ=0.35-0.7倍Zoom経由)")       # Window title
        self.master.geometry("1200x650")             # TK window size(width x height)

        #Initialize view, camera
        self.view_width  = 800
        self.view_height = 600
        self.view_magnify  = 1/2  # Camera to Picture ratio 2:1   
        self.camera_id   = 0      # 0=PC_Cam   1=External_USB_Cam
        self.frame_rate  = 10
        self.disp_id = None         #for picture animation

        # Canvas
        self.canvas = tk.Canvas(root, width=self.view_width, height=self.view_height, bg='gray')
        self.canvas.pack(side=tk.LEFT,expand=True,anchor=tk.NW)
        # on Canvas, bind mouse event（Left Click)
        self.canvas.bind('<Button-1>', self.canvas_click)
        self.canvas.pack(expand = True, fill = tk.BOTH)

        #Default save file
        file_name1 = "Capture.jpg"
        self.typelist1 = [("Capture.jpg", ".jpg"),]        
        self.ini_dir = os.path.dirname(__file__)        # get present program directory
        self.file_path = os.path.join(self.ini_dir, file_name1)
        #print (self.file_path)
        self.count   = 0

        # Initialize show scale profile
        self.show_scale  = True   # True= Show Scale    , False= Hide Scale 
        self.relaylens_magnify =0.7  # Zoom lens x0.35 -> x0.70
        self.lens_magnify   = 10.0   # Objective Lens x10 Default
        self.str_length = '100um'
        self.length = 100.0          # Scale length 
        self.pixel_length = 4.2      # 4.2um/Pixel
        self.x0  = 150
        self.y0  = 50

        # Preset Color for Button(tkinter)
        self.color_green = str('#ccffaa') #green
        self.color_gray  = str('#f2f2f2') #gray(Back ground color)
        self.color_red   = str('#ffaacc') #red
        # Preset Color for Scale(opencv)
        self.white = (255,255,255)  #Color order is BGR on cv2(opencv)
        self.red = (0,0,255)        #BGR  #RGB(255,0,0)
        self.aqua = (255,255,0)     #BGR  #RGB(0,255,255)
        self.green = (0,255,0)
        self.black = (0,0,0)
        self.color = self.white

        #camera Open 
        self.capture = cv2.VideoCapture(self.camera_id)
        self.frame_prf_0=self.capture.get(cv2.CAP_PROP_FRAME_WIDTH) # get camera profile
        self.frame_prf_1=self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        str_text = 'Camera_'+str(self.camera_id)+'\n'+'Width  :'+str(self.frame_prf_0)+'\n'+'Height :' + str(self.frame_prf_1)
        tk.messagebox.showinfo(title="Camera connected", message=str_text)
        #camera Re-open with "cv2.CAP_DSHOW"
        self.capture = cv2.VideoCapture(self.camera_id,cv2.CAP_DSHOW)
        #self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,self.frame_prf_0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,1600)   # Force write size without using camera profile temporarily.
        #self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,self.frame_prf_1)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,1200)
        self.capture.set(cv2.CAP_PROP_FPS,self.frame_rate)
        self.view_x = int(1600 * self.view_magnify)
        self.view_y = int(1200 * self.view_magnify)
        aspect_ratio = self.view_x / self.view_y
        if self.view_x > self.view_width:
            self.view_magnify = self.view_magnify*self.view_width/self.view_x
            self.view_x = self.view_width
            self.view_y = int(self.view_width / aspect_ratio)
        if self.view_y > self.view_height:
            self.view_magnify = self.view_magnify*self.view_height/self.view_y
            self.view_y = self.view_height
            self.view_x = int(self.view_height * aspect_ratio)


        # frame1
        frame1 = tk.Frame(root, bd=2, pady=5, padx=5)
        frame1.pack(side=tk.RIGHT,expand=True,anchor=tk.NE)
        #camera operation
        self.btn_live = tk.Button(frame1, text='Play//Pause', command=self.btn_click, width=10, height=2, background=self.color_green)
        self.btn_live.grid(row=0, column=0, padx=5, pady=5)
        btn_exit = tk.Button(frame1, text='Exit', command=root.quit, width=10, height=2)
        btn_exit.grid(row=0, column=1, padx=5, pady=5)
        column_0 = ('0', '1')
        btn_camera = tk.Button(frame1, text='Change Camera', command=self.Set_Camera, width=15, height=2)
        btn_camera.grid(row=1, column=0, padx=5, pady=5)
        self.combobox_0 = ttk.Combobox(frame1, height=1, width=10, justify='center', values=column_0)
        self.combobox_0.insert(0, '1')
        self.combobox_0.grid(row=1, column=1, padx=5, pady=5)
        #Save picture
        label_save_filename = tk.Label(frame1, text='show Save File name.')
        label_save_filename.grid(row=2, column=0, padx=5, pady=5)
        self.save_filename = tk.Text(frame1,  height=4,width=25)
        self.save_filename.grid(row=3, column=0, padx=5, pady=5)
        self.save_filename.insert(tk.END, str(self.file_path))
        btn_Set_Plot1 = tk.Button(frame1, text='Change save file', command=self.Set_File_Path, width=15, height=1)
        btn_Set_Plot1.grid(row=4, column=0, padx=5, pady=5)  
        self.btn_save = tk.Button(frame1, text='Save Image File', command=self.Caputure_Image, width=15, height=2)
        self.btn_save.grid(row=5, column=0, padx=5, pady=5)
        #Show scale
        btn_scale = tk.Button(frame1, text='Scale on/off', command=self.Show_Scale, width=15, height=1)
        btn_scale.grid(row=6, column=0, padx=5, pady=5)
        column_1 = ('x5', 'x10', 'x20', 'x50', 'x100')
        btn_Lens = tk.Button(frame1, text='Set Objective Lens', command=self.Set_Objective_Lens, width=15, height=1)
        btn_Lens.grid(row=7, column=0, padx=5, pady=5)
        self.combobox_1 = ttk.Combobox(frame1, height=1, width=10, justify='center', values=column_1)
        self.combobox_1.insert(0, 'X10')
        self.combobox_1.grid(row=7, column=1, padx=5, pady=5)
        column_2 = ('10um', '20um', '50um', '100um', '200um','500um','1000um')
        btn_Length = tk.Button(frame1, text='Set Length', command=self.Set_Length, width=15,height=1)
        btn_Length.grid(row=8, column=0, padx=5, pady=5)
        self.combobox_2 = ttk.Combobox(frame1, height=1, width=10, justify='center', values=column_2)
        self.combobox_2.insert(0, '100um')
        self.combobox_2.grid(row=8, column=1, padx=5, pady=5)
        column_3 = ('white', 'green', 'aqua', 'black', 'red')
        btn_Length = tk.Button(frame1, text='Set Color', command=self.Set_Color, width=15,height=1)
        btn_Length.grid(row=9, column=0, padx=5, pady=5)
        self.combobox_3 = ttk.Combobox(frame1, height=1, width=10, justify='center', values=column_3)
        self.combobox_3.insert(0, 'white')
        self.combobox_3.grid(row=9, column=1, padx=5, pady=5)
        btn_Config = tk.Button(frame1, text='Set Configration', command=self.Set_Config, width=15,height=2, background=self.color_green)
        btn_Config.grid(row=10, column=0, padx=5, pady=5)
        #mouse click event
        label_start_x = tk.Label(frame1, text='mouse_pos_x')
        label_start_x.grid(row=11, column=0)
        label_start_y = tk.Label(frame1, text='mouse_pos_y')
        label_start_y.grid(row=12, column=0)
        self.en_x0 = tk.Entry(frame1, width=10, justify='right')
        self.en_x0.grid(row=11, column=1)
        self.en_x0.insert(tk.END, self.x0)
        self.en_y0 = tk.Entry(frame1, width=10, justify='right')
        self.en_y0.grid(row=12, column=1)
        self.en_y0.insert(0, self.y0)
        #Notes
        label_save_filename = tk.Label(frame1, text='Image View is shown in 1/2 scale.')
        label_save_filename.grid(row=13, column=0, padx=5, pady=5)
        label_save_filename = tk.Label(frame1, text='Move the Scale to where mouse is clicked.')
        label_save_filename.grid(row=14, column=0, padx=5, pady=5)

    def canvas_click(self, event):
        '''Canvas mouse click event'''
        self.x0 = int(event.x / self.view_magnify)
        self.y0 = int(event.y / self.view_magnify)
        self.en_x0.delete(0,'end')
        self.en_y0.delete(0,'end')
        self.en_x0.insert(tk.END, self.x0)
        self.en_y0.insert(tk.END, self.y0)
        return

    def btn_click(self):
        '''Play//Pause button '''

        if self.disp_id is None:
            # 動画を表示
            self.disp_image()
            self.btn_live.configure(bg = self.color_red)     # live button color changed
            self.btn_save.configure(bg = self.color_gray)    # save button color changed
        else:
            # 動画を停止
            self.after_cancel(self.disp_id)
            self.disp_id = None
            self.btn_live.configure(bg = self.color_gray)     # live button color changed
            self.btn_save.configure(bg = self.color_green)    # save button color changed
        return

    def disp_image(self):
        '''Show image on Canvas'''

        # make image
        self.make_image()

        # canvas size
        #canvas_width = self.canvas.winfo_width()
        #canvas_height = self.canvas.winfo_height()
        canvas_width = self.view_x
        canvas_height = self.view_y      

        # Resize image to Canvas with original aspect ratio.
        pil_image = ImageOps.pad(self.pil_image, (canvas_width, canvas_height))

        # change PIL.Image to PhotoImage
        self.photo_image = ImageTk.PhotoImage(image=pil_image)

        # canva image
        self.canvas.create_image(
                canvas_width / 2,       # location X&Y(Center of Canvas)
                canvas_height / 2,                   
                image=self.photo_image  # image data
                )

        # show disp_image after 10msec
        self.disp_id = self.after(10, self.disp_image)
        return
        
    def make_image(self):        
        # OpenCV to Canvas
        ret, frame = self.capture.read()

        if self.show_scale:
            #Text
            cv2.putText(img=frame, text=self.str_length, org=(self.x0-130, self.y0), fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale=0.9, color=self.color, thickness=2, lineType=cv2.LINE_AA)

            #Scale
            self.multi_factor = self.lens_magnify * self.relaylens_magnify
            pixels = self.length / self.pixel_length * self.multi_factor
            height=  10
            length= int(pixels)
            x_loc = self.x0
            y_loc = self.y0
            cv2.line(frame, (x_loc, y_loc), (x_loc+length, y_loc), self.color,thickness=2)
            cv2.line(frame, (x_loc, y_loc), (x_loc, y_loc-height), self.color,thickness=2)
            cv2.line(frame, (x_loc+length, y_loc), (x_loc+length, y_loc-height), self.color,thickness=2)
        else:
            pass

        # BGR→RGB 
        #cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if frame.ndim == 2:  # mono
            cv_image = frame
        if frame.shape[2] == 1:  # mono (8bit)
            cv_image = frame
        elif frame.shape[2] == 3:  # Color(24bit)
            cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        elif frame.shape[2] == 4:  # Color with Transparent(32bit)
            cv_image = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGBA)
        
        pil_image = Image.fromarray(cv_image)
        self.pil_image = pil_image
        return
    
    def Set_File_Path(self):
        #20221108 add defaultextension = ""  ....automatically add extension
        filename=filedialog.asksaveasfilename(initialdir=self.ini_dir, filetypes=self.typelist1, title="Set File_path", defaultextension = "")
        if filename == "":
            return
        else:
            self.file_path = filename
            self.f_root, self.ext = os.path.splitext(self.file_path)
            self.ini_dir = self.f_root
            self.save_filename.delete('1.0','end')                   # Delete  all
            self.save_filename.insert(tk.END, str(self.file_path))
            print('Set File_path =' , os.path.abspath(self.file_path))
            return    
        
    def Caputure_Image(self):
        '''Save picture'''
        self.pil_image.save(self.file_path)
        #self.create_modeless_dialog()    # 2022/12/21 delete
        tk.messagebox.showinfo(title="Image file saved", message="Image file saved.")
        #self.pil_image.save('{}_{}.{}'.format(self.base_path, self.count, self.ext))
        #self.count += 1
        return
                
    def Set_Camera(self):
        # button color changed
        self.btn_live.configure(bg = self.color_green)   # live button color changed
        self.btn_save.configure(bg = self.color_gray)    # save button color changed
        # Pause Camera and Change Camera
        if self.disp_id is None:
            pass
        else:
            # Pause camera
            self.after_cancel(self.disp_id)
            self.disp_id = None# Pause
        # release Camera
        self.capture.release()
        self.camera_id = int(self.combobox_0.get())
        # Open Camera 
        self.capture = cv2.VideoCapture(self.camera_id)

        self.frame_prf_0=self.capture.get(cv2.CAP_PROP_FRAME_WIDTH) # Get camera profile
        self.frame_prf_1=self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        str_text = 'Camera_'+str(self.camera_id)+'\n'+'Width  :'+str(self.frame_prf_0)+'\n'+'Height :' + str(self.frame_prf_1)
        tk.messagebox.showinfo(title="Camera connected", message=str_text)
        #Camera Re-open and change cv2.CAP_DSHOW mode
        self.capture = cv2.VideoCapture(self.camera_id,cv2.CAP_DSHOW)
        #self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,self.frame_prf_0)
        #self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,self.frame_prf_1)
        #self.capture.set(cv2.CAP_PROP_FPS,self.frame_rate)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,1600)   # Force write size without using camera profile temporarily.
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,1200)
        self.capture.set(cv2.CAP_PROP_FPS,self.frame_rate)        
        self.view_x = int(1600 * self.view_magnify)
        self.view_y = int(1200 * self.view_magnify)
        if self.view_x > self.view_width:
            self.view_magnify = self.view_magnify*self.view_width/self.view_x
            aspect_ratio = self.view_x / self.view_y
            self.view_x = self.view_width
            self.view_y = int(self.view_width / aspect_ratio)
            
        if self.view_y > self.view_height:
            self.view_magnify = self.view_magnify*self.view_height/self.view_y
            aspect_ratio = self.view_x / self.view_y
            self.view_y = self.view_height
            self.view_x = int(self.view_height * aspect_ratio)
        return

    def Set_Objective_Lens(self):
        name = self.combobox_1.get()
        if name == 'x5':
            self.lens_magnify =   5.0
        elif name == 'x10':
            self.lens_magnify =  10.0
        elif name == 'x20':
            self.lens_magnify =  20.0
        elif name == 'x50':
            self.lens_magnify =  50.0
        elif name == 'x100':
            self.lens_magnify = 100.0
        else:
            pass
        return
            
    def Set_Length(self):
        self.str_length = self.combobox_2.get()
        if self.str_length == '10um':
            self.length =  10.0
        elif self.str_length == '20um':
            self.length =  20.0
        elif self.str_length == '50um':
            self.length =  50.0
        elif self.str_length == '100um':
            self.length =  100.0
        elif self.str_length == '200um':
            self.length = 200.0
        elif self.str_length == '500um':
            self.length = 500.0
        elif self.str_length == '1000um':
            self.length = 1000.0
        else:
            pass
        return

    def Set_Color(self):
        name = self.combobox_3.get()
        if name == 'white':
            self.color =   self.white
        elif name == 'black':
            self.color =   self.black
        elif name == 'green':
            self.color =   self.green
        elif name == 'aqua':
            self.color =   self.aqua
        elif name == 'red':
            self.color =   self.red 
        else:
            pass
        return
        
    def Set_Config(self):
        self.capture.set(cv2.CAP_PROP_SETTINGS,1)
        #self.caputre.set(cv2.CAP_PROP_AUTO_EXPOSURE,3)  #auto mode
        #self.caputre.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)  #manual mode
        #self.caputre.set(cv2.CAP_PROP_EXPOSURE,desired_exposure_value)  #0->1s -1->500ms,,-13->122.1us       
        return

    #  Show scale according to  "On/Off" button.
    def Show_Scale(self):
        self.show_scale = not self.show_scale
        return
        
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()
