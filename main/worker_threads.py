import threading, time
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from main.models.psmt import PSMTRequest
from authentication.models import PelClient

TEST_NOTIFY_EMAILS = ["joseph.mbuku@peleza.com"]
NOTIFY_EMAILS = ["verify@peleza.com"]
TIMEOUT = 60
MAX_RETRIES = 3


class MailerThread(threading.Thread):
    def __init__(
        self,
        request_id=None,
        dataset_name=None,
        company_name=None,
        approved=False,
        instance: PSMTRequest = None,
    ):
        super().__init__()
        self.retries = 0
        self.request_id = request_id
        self.dataset_name = dataset_name
        self.company_name = company_name
        #
        self.instance = instance
        self.approved = approved

    def send_new_request_mail(self):
        context = {
            "request_id": self.request_id,
            "company_name": self.company_name,
        }

        subject, to = (
            "NEW VERIFICATION REQUEST HAS BEEN PLACED",
            NOTIFY_EMAILS
            if "test" not in str(self.dataset_name).lower().strip()
            else TEST_NOTIFY_EMAILS,
        )
        html_content = render_to_string("newRequest.html", context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, to=to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def send_mail(self):
        func = self.send_approved_email if self.instance else self.send_new_request_mail
        try:
            func()
        except Exception as e:
            if self.retries < MAX_RETRIES:
                self.retries += 1
                time.sleep(TIMEOUT)
                self.send_mail()

    def send_approved_email(self):
        user = PelClient.objects.filter(client_id=self.instance.client_id).first()

        user_email = (
            [str(user.client_login_username).lower().strip()]
            if user
            else TEST_NOTIFY_EMAILS
        )

        context = {
            "dataset_name": self.instance.bg_dataset_name,
            "registration_number": self.instance.registration_number,
            "report_url": "/",
            "request_ref_number": self.instance.request_ref_number,
        }

        subject, to = (
            "REQUEST FINAL STATUS NOTIFICATION",
            user_email
            if "test" not in str(self.dataset_name).lower().strip()
            else user_email,
        )
        html_content = render_to_string("approvedRequest.html", context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, to=to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def run(self):
        self.send_mail()


mailer = MailerThread()
