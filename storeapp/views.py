from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, Category, CategoryOffer
from .serializers import ProductSerializers, CategorySerializers, CategoryOfferSerializer
import razorpay
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order

@api_view(['POST'])
def create_order(request):
    user = request.user
    total_amount = request.data.get('total_amount')

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    razorpay_order = client.order.create({
        "amount": int(float(total_amount) * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    order = Order.objects.create(
        user=user,
        total_amount=total_amount,
        razorpay_order_id=razorpay_order['id']
    )

    return Response({
        "order_id": razorpay_order['id'],
        "amount": razorpay_order['amount'],
        "currency": razorpay_order['currency']
    })



@api_view(['POST'])
def verify_payment(request):
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    data = request.data

    params_dict = {
        'razorpay_order_id': data['razorpay_order_id'],
        'razorpay_payment_id': data['razorpay_payment_id'],
        'razorpay_signature': data['razorpay_signature']
    }

    try:
        client.utility.verify_payment_signature(params_dict)

        order = Order.objects.get(
            razorpay_order_id=data['razorpay_order_id']
        )

        order.razorpay_payment_id = data['razorpay_payment_id']
        order.razorpay_signature = data['razorpay_signature']
        order.payment_status = 'SUCCESS'
        order.save()

        return Response({"status": "Payment Verified"})

    except:
        return Response({"status": "Payment Failed"})


# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializers

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def get_queryset(self):
        queryset = Product.objects.all()

        category_id = self.request.query_params.get('category')
        search = self.request.query_params.get('q')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset
        
@api_view(['GET'])
def get_category_offer(request, category_id):

    offer = CategoryOffer.objects.get(
        category_id=category_id
    )

    serializer = CategoryOfferSerializer(offer)

    return Response(serializer.data)
    



