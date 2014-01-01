import smtplib

to = "adeeshj@gmail.com"

gmail_user = "aj.test.python@gmail.com"
gmail_pwd = "aj.testing.python"
smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_pwd)

smtpserver.sendmail(gmail_user, to, "Testing from my first smtp send!")

print "done!"

smtpserver.quit()