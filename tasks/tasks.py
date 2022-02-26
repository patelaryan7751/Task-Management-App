from celery.decorators import periodic_task
from datetime import datetime, timedelta

from tasks.models import STATUS_CHOICES, Task, TaskEmail


from django.core.mail import send_mail


from django.contrib.auth.models import User


@periodic_task(run_every=timedelta(seconds=10))
def send_email_reminder():
    now = datetime.now()
    for userReport in TaskEmail.objects.exclude(email_prev_sent_at=now.day).filter(mail_time__lt=now.hour):
        user = User.objects.get(id=userReport.user.id)
        sendemail(user)
        userReport.email_prev_sent_at = now.day
        userReport.save()


def sendemail(user):
    subject = f"{user}'s Report"
    content = "***************** Your tasks report **********:\n\n"
    email = "tasks@taskmanager.org",
    sendingto_email = []
    sendingto_email.append(user.email)

    for choice in STATUS_CHOICES:
        pending_qs = Task.objects.filter(
            user=user, status=choice[0], deleted=False)
        content += f"-Task Status:{choice[0]}:\n\n Task count:{pending_qs.count}\n"

    send_mail(
        subject,
        content,
        email,
        sendingto_email,
        fail_silently=False,
    )

    print(f"{user} email sent!!")
