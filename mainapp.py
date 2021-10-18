#resizr, a project by pranav-avn.
#helps you to resize images by dimension adj/final file size

#importing stuff
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkFont
from tkmacosx import Button #can be deprecated if not running on MacOS
from tkinter import Toplevel, filedialog, image_names

app = tk.Tk()   #main widget creation
app.title('resizr')
impapplogo = Image.open("resizrlogopng.png")
applogintrm = impapplogo.resize((512,512))
applogo = ImageTk.PhotoImage(applogintrm)
app.iconphoto(True, applogo)

#root creation
root = tk.Canvas(app, width=600, height=450)
root.pack(fill='both', expand='false')


norm=tkFont.Font(family="MADE Outer Sans Bold", size=28)
normh=tkFont.Font(family="MADE Outer Sans Bold", size=22)
deftext=tkFont.Font(family="MADE Outer Sans Alt", size=15)
dafttext = tkFont.Font(family="Bebas Neue", size=25)

#defining global texture files
bg = tk.PhotoImage(file="bg.png")
resizrlogo = Image.open("resizrlogo.png")
resizrinterm = resizrlogo.resize((192,192))
resizr= ImageTk.PhotoImage(resizrinterm)
impbuttonbg = Image.open("buttonbg.png")
buttonbginterm = impbuttonbg.resize((192,192))
button_bg = ImageTk.PhotoImage(buttonbginterm)

#rendering stuff
root.create_image(0,0,image=bg, anchor='nw')
root.create_image(300,50,image=resizr)

root.create_text(300,100,text="Import Images to Resize.", font=deftext, fill='black')

root.create_text(300,175,text="Click the 'Browse' button and locate the image to be resized", font=dafttext, fill='black')

def browse_event(): #opens file browser and imports image
    print("browse_event")
    browse_btn['text'] = 'Loading...'
    global imported_image
    global usr_img
    app.file = filedialog.askopenfilename(title="Choose an image to resize", filetypes=[('Images', ['.png','.jpg', '.jpeg', '.gif'])])
    usr_img = Image.open(app.file)
    width, height = usr_img.size
    if width>=1024 and height>=1024:
        width=width//4
        height=height//4
    elif width>=256 and height>=256:
        width=width//2
        height=height//2
    usr_img_tmp = usr_img.resize((width,height))
    imported_image = ImageTk.PhotoImage(usr_img_tmp)
    img_disp = Toplevel(app)
    img_disp.title('Imported Image')
    importedimg = tk.Label(img_disp, image=imported_image)
    importedimg.pack()
    root.pack_forget()
    resize_options()

def resize_options():   #resize methods
    wind2 = tk.Canvas(app, width=600, height=450)
    wind2.pack(fill='both', expand='false')

    def dimension_adj_inter():
        wind2.pack_forget() #refresh screen
        dimension_adj()
    
    def filesize_adj_inter():
        wind2.pack_forget() #refresh screen
        filesize_adj()
    
    wind2.create_image(0,0,image=bg, anchor='nw')
    wind2.create_image(300,50,image=resizr)
    wind2.create_text(300,155,text="Choose the method to resize image.", font=dafttext, fill='black')
    dimensions_btn = Button(wind2, text="Dimensions", bg='#4E54C8', fg='#FFFFFF', borderless=1, overbackground='#8F94FB', command=dimension_adj_inter, font=norm)
    wind2.create_window(300,220, window=dimensions_btn)
    filesize_btn = Button(wind2, text="File Size", bg='#4E54C8', fg='#FFFFFF', borderless=1, overbackground='#8F94FB', command=filesize_adj_inter, font=norm)
    wind2.create_window(300,280, window=filesize_btn)


def dimension_adj():    #file dimension adjustment
    wind3 = tk.Canvas(app, width=600, height=450)
    wind3.pack(fill='both', expand='false')
    
    def dimension_sub():
        fwidth = int(fwidthentry.get())
        fheight= int(fheightentry.get())
        width, height = usr_img.size
        ogratio = width/height
        fratio = fwidth/fheight
        
        def ratio_mismatch():
            
            def yes_fn():
                dimenresize(fwidth, fheight)

            def no_fn():
                app.quit

            
            wind3.create_text(300,410,text="Final resolution not matching aspect ratio of original image", font=dafttext, fill='red')
            wind3.create_text(300,440,text="Image might be skewed. Do you still wish to proceed?", font=dafttext, fill='red')
            yes_btn = Button(wind3, text="Yes", bg='#4E54C8', fg='#FFFFFF', borderless=1, overbackground='#8F94FB', command=yes_fn, font=normh)
            wind3.create_window(300,310, window=yes_btn)
            no_btn = Button(wind3, text="No", bg='#4E54C8', fg='#FFFFFF', borderless=1, overbackground='#8F94FB', command=no_fn, font=normh)
            wind3.create_window(300,360, window=no_btn)
        
        if ogratio!=fratio:
            ratio_mismatch()
        else:
            dimenresize(fwidth, fheight)

            


    wind3.create_image(0,0,image=bg, anchor='nw')
    wind3.create_image(300,50,image=resizr)
    wind3.create_text(300,125,text="Enter the final image dimensions", font=dafttext, fill='black')
    fwidthentry = tk.Entry(wind3, width=10, font=dafttext)
    fwidthentry.insert(tk.END, 'Width')
    fheightentry = tk.Entry(wind3, width=10, font=dafttext)
    fheightentry.insert(tk.END, 'Height')
    fwidthentry.place(x=250, y=140)
    fheightentry.place(x=250, y=190)
    submit_btn = Button(wind3, text="Submit", bg='#4E54C8', fg='#FFFFFF', borderless=1, overbackground='#8F94FB', command=dimension_sub, font=norm)
    wind3.create_window(300,260, window=submit_btn)


def dimenresize(fw, fh):    #saving the resized file, resized thru dimension adjust
    og_img = usr_img.resize((fw,fh))
    fimage= ImageTk.PhotoImage(og_img)
    imgformat = usr_img.format
    og_img = og_img.save("output."+usr_img.format)
    f_img = ImageTk.PhotoImage(og_img)
    fimg_disp = Toplevel(app)
    fimg_disp.title('Output Image')
    fimg_ot = tk.Label(fimg_disp, image=f_img)
    fimg_ot.pack()    


def filesize_adj(): #deprecated as of now
    wind3 = tk.Canvas(app, width=600, height=450)
    wind3.pack(fill='both', expand='false')
    wind3.create_image(0,0,image=bg, anchor='nw')
    wind3.create_image(300,50,image=resizr)
    wind3.create_text(300,125,text="Yet to be Implemented, check back later :)", font=dafttext, fill='black')


browse_btn = Button(root, text="Browse", bg='#4E54C8', fg='#FFFFFF', borderless=1, overbackground='#8F94FB', command=browse_event, font=norm)   #browse button
root.create_window(300,250, window=browse_btn)


#final loop
app.mainloop()
