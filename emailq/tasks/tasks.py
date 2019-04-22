from celery.task import task
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from celery.exceptions import MaxRetriesExceededError
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
import logging

config = ConfigParser()
config.read('cybercom.cfg')

logging.basicConfig(level=logging.INFO)

host = config.get('email', 'host')
port = config.getint('email', 'port')
user = config.get('email', 'user')
password = config.get('email', 'pass')
timeout = 20


@task(bind=True)
def sendmail(self, to, subject=None, body=None, attachment=None):
    """
    Sendmail Task
    
    Sends an email.

    args:
      to: email address[es] to send to separated by comma
      subject: subject line of email
      body: body text of email
      attachment: [filename as string, data as base64 encoded value]

    """

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = "Lib.CC-1@ou.edu"
    msg['To'] = to
    msg.attach(MIMEText(body))

    if attachment is not None:
        filename, data = attachment
        attachfile = MIMEBase('text', 'plain')
        attachfile.set_payload(data)
        attachfile.add_header('Content-Transfer-Encoding', 'base64')
        attachfile['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
        msg.attach(attachfile)

    try:
        logging.info("Sending email to: {0}".format(to))
        server = smtplib.SMTP(host, port, timeout=timeout)
        server.starttls()  # Do not send credentials over the network in the clear!
        server.ehlo()
        server.login(user, password)
        server.sendmail(user, to.split(","), msg.as_string())
        server.close()
    except MaxRetriesExceededError as e:
        return {"error": e}
    except Exception as e:
        logging.error("Error sending email: {0}".format(e))
        self.retry(countdown=10, max_retries=3)
    return True
