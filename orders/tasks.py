from celery import shared_task as task
from django.core.mail import send_mail as sendmail
from .models import Order

@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'  # type: ignore
    message = f'Dear {order.firstname},\n\n' \
    f'You have successfully placed an order.' \
    f'Your order ID is {order.id}.'  # type: ignore
    mail_sent = sendmail(
        subject,
        message,
        'admin@myshop.com',
        [order.email],
    )
    return mail_sent