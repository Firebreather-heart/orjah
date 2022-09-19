from celery import shared_task as task
from firemail.main import sendmail
from .models import Order

@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.firstname},\n\n' \
    f'You have successfully placed an order.' \
    f'Your order ID is {order.id}.'
    mail_sent = sendmail(subject=subject, payload = message,recipient=order.email)
    return mail_sent