from celery.task import task
from celery.utils.mail import Message, Mailer
from ConfigParser import ConfigParser
import logging

config = ConfigParser()
config.read('cybercom.cfg')

logging.basicConfig(level=logging.INFO)

mailer = Mailer(
    host=config.get('email', 'host'),
    port=config.getint('email', 'port'),
    user=config.get('email', 'user'),
    password=config.get('email', 'pass'),
    use_tls=config.getboolean('email', 'use_tls'),
    timeout=20
)


@task(bind=True)
def sendmail(self, to, subject=None, body=None):
    """
    Sendmail Task
    
    Sends an email.

    args:
      to: email address to send to
      subject: subject line of email
      body: body text of email
    """

    message = Message(
        to=to,
        sender=config.get('email', 'user'),
        subject=subject,
        body=body
    )
    try:
        raise Exception('testing')
        logging.info("Sending email to: {0}".format(to))
        mailer.send(message)
    except Exception as e:
        logging.error("Error sending email: {0}".format(e))
        self.retry(countdown=5, max_retries=3)
    return True
