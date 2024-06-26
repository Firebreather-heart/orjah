import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
from .tasks import payment_completed
# instantiate Braintree payment gateway

# if settings.BRAINTREE_PRODUCTION:
#         braintree_env = braintree.Environment.Production
# else:
#         braintree_env = braintree.Environment.Sandbox
#     # Configure Braintree
# braintree.Configuration.configure(
#         braintree_env,
#         merchant_id=settings.BRAINTREE_MERCHANT_ID,
#         public_key=settings.BRAINTREE_PUBLIC_KEY,
#         private_key=settings.BRAINTREE_PRIVATE_KEY,
#     )
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost =  order.get_total_cost()
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
        'amount': f'{total_cost:.2f}',
        'payment_method_nonce': nonce,
        'options': {
        'submit_for_settlement': True
        }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            payment_completed.delay(order.id)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        client_token = gateway.client_token.generate()
        return render(request,
                            'payment/process.html',
                            {'order': order,
                            'braintree_client_token': client_token})
                        
def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')