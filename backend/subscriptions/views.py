import stripe
from django.http import JsonResponse
from django.conf import settings
import json
from django.http import HttpResponse
from stripe.error import SignatureVerificationError
from stripe import Webhook
from .models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': 'price_1QVg4FBRE1X4phKr29g3Dvfo',  # Replace with a Stripe Price ID
                        'quantity': 1,
                    },
                    {
                        'price': 'price_1QVg4FBRE1X4phKr4Dr7VyrJ',  # Replace with a Stripe Price ID
                        'quantity': 1,
                    },
                ],
                success_url='http://localhost:3000/subscription/success',
                cancel_url='http://localhost:3000/subscription/cancel',
            )
            return JsonResponse({'url': session.url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        


def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'invoice.payment_succeeded':
        subscription_id = event['data']['object']['subscription']
        # Update the subscription in your database
        Subscription.objects.filter(stripe_subscription_id=subscription_id).update(active=True)

    return HttpResponse(status=200)
