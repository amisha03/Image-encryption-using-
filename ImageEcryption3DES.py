from tkinter import *
import smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from des import *

import tkinter
import tkinter.filedialog

import base64


encoded=open("binencoded",'wb+')
d=des()

def encrypt():
    master = tkinter.Tk()
    file = tkinter.filedialog.askopenfile(parent=master,mode='rb+',title='Choose a file')

    if file != None:
        data = file.read()
        
        str=base64.b64encode(data)
        
        en1=d.encrypt(app.key1,str)
        en2=d.decrypt(app.key2,en1)
        en3=d.encrypt(app.key3,en2)
        
        encoded.write(bytes(en3,"utf-8"))

        encoded.close()
        print("Encryption Done")

def decrypt():
    
    master = tkinter.Tk()
    file = tkinter.filedialog.askopenfile(parent=master, mode='rb+', title='Choose a file')
    if file!=None:
        te=file.read().decode(encoding="utf-8")
    
        de3 = d.decrypt(app.key3, te)
        de2 = d.encrypt(app.key2, de3)
        de1 = d.decrypt(app.key1, de2)
    
        dec = base64.b64decode(de1)
        print("Decryption Done")
        decodeit = open('decrypted_tdes.jpeg', 'wb')
    
        decodeit.write(dec)
        decodeit.close()


def mail():
    subject = "Encrypted File"
    body = "This is an email with encrypted file "
    sender_email = "crypto.tdes@gmail.com"

    app.password=app.passvar.get()
    app.receiver_email=app.receiver_emailvar.get()
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = app.receiver_email
    message["Subject"] = subject
    message["Bcc"] = app.receiver_email

    # body to email
    message.attach(MIMEText(body, "plain"))
    filename = "binencoded"  # In same directory as script
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    message.attach(part)
    text = message.as_string()
    print("Sending Encrypted file to ",app.receiver_email)
    print("Password ",app.password)

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, app.password)
        server.sendmail(sender_email, app.receiver_email, text)
        print("Mail Sent")
    
    #  password - wkbM2964k5PZ

def qExit():
    roott.destroy()



def submit():
    app.key1 = app.key1_var.get()
    app.key2 = app.key2_var.get()
    app.key3 = app.key3_var.get()

    newWindow = Toplevel(roott)
    newWindow.title("New Window")
    newWindow.geometry("1100x300")


    #Encode Button

    btnEncode = Button(newWindow, padx=16, pady=8, bd=5,
                      fg="black", font=('arial', 10, 'bold'),
                      width=10, text="Encode", bg="green",
                      command=encrypt).grid(row=1200, column=1)

    # Decode button
    btnDecode = Button(newWindow, padx=16, pady=8, bd=5,
                     fg="black", font=('arial', 10, 'bold'),
                     width=10, text="Decode", bg="red",
                     command=decrypt).grid(row=2400, column=1)


    app.key1_var.set("")
    app.key2_var.set("")
    app.key3_var.set("")


class App:

    def __init__(self, root):
        self.key1_var = StringVar()
        self.key2_var = StringVar()
        self.key3_var = StringVar()
        self.key1=""
        self.key2=""
        self.key3=""
        self.lblInfo = Label(root, font=('helvetica', 30, 'bold'),
                        text="Image encryption \n 3 DES",
                        fg="Black", bd=10, anchor='w')

        self.lblInfo.grid(row=0, column=2)

        # labels for the key1
        self.lblkey1 = Label(root, text='Key1', font=('calibre', 10, 'bold'))
        self.txtkey1 = Entry(root, textvariable=self.key1_var, font=('calibre', 10, 'normal'))
        self.lblkey1.grid(row=40, column=0)
        self.txtkey1.grid(row=40, column=1)


        # labels for the key2
        self.lblkey2 = Label(root, text='Key2', font=('calibre', 10, 'bold'))
        self.txtkey2 = Entry(root, textvariable=self.key2_var, font=('calibre', 10, 'normal'))
        self.lblkey2.grid(row=80, column=0)
        self.txtkey2.grid(row=80, column=1)


        # labels for the key3
        self.lblkey3 = Label(root, text='Key3', font=('calibre', 10, 'bold'))
        self.txtkey3 = Entry(root, textvariable=self.key3_var, font=('calibre', 10, 'normal'))
        self.lblkey3.grid(row=120, column=0)
        self.txtkey3.grid(row=120, column=1)

        # labels for the password
        self.password = ""
        self.passvar = StringVar()
        self.passwordlbl = Label(root, text='Password', font=('calibre', 10, 'bold'))
        self.passwordtxt = Entry(root, textvariable=self.passvar, font=('calibre', 10, 'normal'))

        # labels for the receiver_email
        self.receiver_email = ""


        self.receiver_emailvar = StringVar()

        self.receiver_emaillbl = Label(root, text='Reciever', font=('calibre', 10, 'bold'))
        self.receiver_emailltxt = Entry(root, textvariable=self.receiver_emailvar, font=('calibre', 10, 'normal'))

        # labels for the key

        self.passwordlbl.grid(row=40, column=2)
        self.passwordtxt.grid(row=40, column=3)
        self.receiver_emaillbl.grid(row=80, column=2)
        self.receiver_emailltxt.grid(row=80, column=3)


roott = Tk()

sub_btn = Button(roott, padx=16, pady=8, bd=5,
                  fg="black", font=('arial', 10, 'bold'),
                  width=10, text="Submit", bg="green",
                  command=submit).grid(row=1200, column=1)
btnMail = Button(roott, padx=16, pady=8, bd=5,
                              fg="black", font=('arial', 10, 'bold'),
                              width=10, text="Send mail", bg="blue",
                              command=mail).grid(row=1200, column=2)


# defining size of window
roott.geometry("1100x300")

# setting up the title of window
roott.title("Image Encryption and Decryption")
app = App(roott)
roott.mainloop()





