from celery.task import task
from celery.utils.log import get_task_logger
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from celery.exceptions import MaxRetriesExceededError
from os import environ

logger = get_task_logger(__name__)

host = environ.get('EMAIL_HOST')
port = environ.get('EMAIL_PORT')
user = environ.get('EMAIL_HOST_USER')
password = environ.get('EMAIL_HOST_PASSWORD')
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
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    if attachment is not None:
        filename, data = attachment
        attachfile = MIMEBase('text', 'plain')
        attachfile.set_payload(data)
        attachfile.add_header('Content-Transfer-Encoding', 'base64')
        attachfile['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
        msg.attach(attachfile)

    try:
        logger.info("Sending email to: {0}".format(to))
        server = smtplib.SMTP(host, port, timeout=timeout)
        server.starttls()  # Do not send credentials over the network in the clear!
        server.ehlo()
        server.login(user, password)
        server.sendmail(user, to.split(","), msg.as_string())
        server.close()
    except MaxRetriesExceededError as e:
        return {"error": e}
    except Exception as e:
        logger.error("Error sending email: {0}".format(e))
        self.retry(countdown=10, max_retries=3)
    return True
