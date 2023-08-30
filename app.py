from flask import Flask,render_template,request,redirect
from flask_mysqldb import MySQL
import os
import smtplib
from email.message import EmailMessage
import ssl

app=Flask(__name__)

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="tijabo"

mysql=MySQL(app)



@app.route("/")
def index():
    return render_template("home.html")

@app.route("/send_message",methods=["POST","GET"])
def send_message():
        if request.method=="POST":
             email_sender=request.form['email_sender']
             email_receiver=request.form['email_receiver']
             subject=request.form['subject']
             body=request.form['body']


             cur=mysql.connection.cursor()
             cur.execute("INSERT INTO tijabo (first_name,last_name,email,message) VALUES (%s,%s,%s,%s)",(email_sender,email_receiver,subject,body))
             mysql.connection.commit()
             cur.close()



             email_sender=email_sender
             email_password='exqryrwlvsqeorji'
             email_receiver=email_receiver


             subject=request.form['subject']
             body=request.form['body']

             em=EmailMessage()
             em['From']=email_sender
             em['To']=email_receiver
             em['Subject']=subject
             em.set_content(body)

             context=ssl.create_default_context()

             with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                 smtp.login(email_sender,email_password)
                 smtp.sendmail(email_sender, email_receiver, em.as_string())
        return render_template("result.html")
        
             

if __name__ == "__main__":
    app.run(debug=True)
