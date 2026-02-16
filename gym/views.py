from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.conf import settings as main_settings
from drf_yasg.utils import swagger_auto_schema
from sslcommerz_lib import SSLCOMMERZ
import uuid
from datetime import date, timedelta
from decouple import config

from .models import Membership, Subscription, FitnessClass, ClassBooking, Attendance, Payment, Feedback
from .serializers import (
    MembershipSerializer, SubscriptionSerializer, FitnessClassSerializer,
    ClassBookingSerializer, AttendanceSerializer, PaymentSerializer, FeedbackSerializer
)

from gym.permission import IsOwnerOrAdmin, IsStaffOrAdmin, ReadOnlyOrAdmin 
from users.permissions import IsAdmin, IsMember, IsStaff
from .pagination import StandardResultsSetPagination

# ----------------------- Membership -----------------------
class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all().order_by('id')
    serializer_class = MembershipSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsStaffOrAdmin()]

# ----------------------- Subscription -----------------------
class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Subscription.objects.none()
        if user.role in ['ADMIN', 'STAFF']:
            return Subscription.objects.all().order_by('id')
        if user.role == 'MEMBER':
            return Subscription.objects.filter(user=user).order_by('id')
        return Subscription.objects.none()

    def get_permissions(self):
        user = self.request.user
        if not user.is_authenticated:
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsMember()]
        if self.action == 'destroy':
            return [IsAdmin()]
        if user.role in ['STAFF', 'ADMIN']:
            return [IsStaffOrAdmin()]
        return [IsOwnerOrAdmin()]

    def perform_create(self, serializer):
        from datetime import timedelta, date
        plan = serializer.validated_data['plan']
       
        calculated_end_date = date.today() + timedelta(days=plan.duration_days)
        serializer.save(user=self.request.user, end_date=calculated_end_date, status='inactive')

# ----------------------- FitnessClass -----------------------
class FitnessClassViewSet(viewsets.ModelViewSet):
    queryset = FitnessClass.objects.all().order_by('id')
    serializer_class = FitnessClassSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsStaffOrAdmin()]

    def perform_create(self, serializer):
        if self.request.user.role == 'STAFF':
            serializer.save(instructor=self.request.user)
        else:
            serializer.save()

# ----------------------- ClassBooking -----------------------
class ClassBookingViewSet(viewsets.ModelViewSet):
    serializer_class = ClassBookingSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return ClassBooking.objects.none()
        if user.role in ['ADMIN', 'STAFF']:
            return ClassBooking.objects.all().order_by('id')
        if user.role == 'MEMBER':
            return ClassBooking.objects.filter(member=user).order_by('id')
        return ClassBooking.objects.none()

    def get_permissions(self):
        user = self.request.user
        if not user.is_authenticated:
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsMember()]
        if user.role in ['STAFF', 'ADMIN']:
            return [IsStaffOrAdmin()]
        return [IsOwnerOrAdmin()]

    @swagger_auto_schema(
        operation_description="Book a class (Member only)",
        request_body=ClassBookingSerializer,
        responses={201: ClassBookingSerializer, 400: "Bad Request"}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)

# ----------------------- Attendance -----------------------
class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Attendance.objects.none()
        if user.role in ['ADMIN', 'STAFF']:
            return Attendance.objects.all().order_by('id')
        if user.role == 'MEMBER':
            return Attendance.objects.filter(member=user).order_by('id')
        return Attendance.objects.none()

    def get_permissions(self):
        user = self.request.user
        if not user.is_authenticated:
            return [IsAuthenticated()]
        if self.action not in ['list', 'retrieve']:
            return [IsStaffOrAdmin()]
        if user.role in ['STAFF', 'ADMIN']:
            return [IsStaffOrAdmin()]
        return [IsOwnerOrAdmin()]

# ----------------------- Payment -----------------------
class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all().order_by('id')
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Payment.objects.none()
        if user.role in ['ADMIN', 'STAFF']:
            return Payment.objects.all().order_by('id')
        if user.role == 'MEMBER':
            return Payment.objects.filter(user=user).order_by('id')
        return Payment.objects.none()

    def get_permissions(self):
        user = self.request.user
        if self.action == 'create':
            return [IsMember()]
        if not user.is_authenticated:
            return [IsAuthenticated()]
        if user.role in ['STAFF', 'ADMIN']:
            return [IsStaffOrAdmin()]
        return [IsOwnerOrAdmin()]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user, status='success', method='Online/Card')
        
       
        if payment.subscription and payment.status == 'success':
            sub = payment.subscription
            sub.status = 'active'
            sub.save()

# ----------------------- SSLCommerz Payment Logic -----------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    user = request.user
    plan_id = request.data.get("plan_id")
    
    try:
        plan = Membership.objects.get(id=plan_id)
    except Membership.DoesNotExist:
        return Response({"error": "Membership plan not found"}, status=404)

    end_date = date.today() + timedelta(days=plan.duration_days)
    subscription = Subscription.objects.create(
        user=user,
        plan=plan,
        end_date=end_date,
        status='inactive'
    )

    transaction_id = str(uuid.uuid4())[:18]
    
    payment = Payment.objects.create(
        user=user,
        subscription=subscription,
        amount=plan.price,
        status='pending',
        method='SSLCommerz',
        transaction_id=transaction_id
    )

    ssl_settings = {
        'store_id': config('SSL_STORE_ID', default='phima6986b97727f1d'),
        'store_pass': config('SSL_STORE_PASS', default='phima6986b97727f1d@ssl'),
        'issandbox': config('SSL_IS_SANDBOX', default=True, cast=bool)
    }
    
    sslcz = SSLCOMMERZ(ssl_settings)
    
    post_body = {}
    post_body['total_amount'] = float(plan.price)
    post_body['currency'] = "BDT"
    post_body['tran_id'] = transaction_id
    post_body['success_url'] = f"{main_settings.BACKEND_URL}/api/payments/success/"
    post_body['fail_url'] = f"{main_settings.BACKEND_URL}/api/payments/fail/"
    post_body['cancel_url'] = f"{main_settings.BACKEND_URL}/api/payments/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = request.data.get("cus_name", f"{user.first_name} {user.last_name}" if user.first_name else user.email)
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = request.data.get("cus_phone", getattr(user, 'phone_number', '01700000000'))
    post_body['cus_add1'] = request.data.get("cus_address", getattr(user, 'address', 'Dhaka'))
    post_body['cus_city'] = "Dhaka"
    post_body['cus_state'] = "Dhaka"
    post_body['cus_postcode'] = "1212"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = f"Gym Membership: {plan.name}"
    post_body['product_category'] = "Fitness"
    post_body['product_profile'] = "general"

    response = sslcz.createSession(post_body)
    
    if response.get('status') == 'SUCCESS':
        return Response({"payment_url": response['GatewayPageURL']})
    else:
        return Response({"error": response}, status=400)

@csrf_exempt
@api_view(['POST'])
def payment_success(request):
   
    transaction_id = request.data.get('tran_id')
    val_id = request.data.get('val_id')
    
    try:
        payment = Payment.objects.get(transaction_id=transaction_id)
        payment.status = 'success'
        payment.save()
        
        if payment.subscription:
            sub = payment.subscription
            sub.status = 'active'
            sub.save()
            
        return redirect(f"{main_settings.FRONTEND_URL}/dashboard?payment=success")
    except Payment.DoesNotExist:
        return redirect(f"{main_settings.FRONTEND_URL}/dashboard?payment=error")

@csrf_exempt
@api_view(['POST'])
def payment_fail(request):
    return redirect(f"{main_settings.FRONTEND_URL}/dashboard?payment=fail")

@csrf_exempt
@api_view(['POST'])
def payment_cancel(request):
    return redirect(f"{main_settings.FRONTEND_URL}/dashboard?payment=cancel")

# ----------------------- Feedback -----------------------
class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all().order_by('id')
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Feedback.objects.none()
        if user.role == 'ADMIN':
            return Feedback.objects.all().order_by('id')
        if user.role == 'STAFF':
            return Feedback.objects.filter(fitness_class__instructor=user).order_by('id')
        if user.role == 'MEMBER':
            return Feedback.objects.filter(member=user).order_by('id')
        return Feedback.objects.none()

    def get_permissions(self):
        user = self.request.user
        if not user.is_authenticated:
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsMember()]
        if user.role in ['STAFF', 'ADMIN']:
            return [IsStaffOrAdmin()]
        return [IsOwnerOrAdmin()]

    @swagger_auto_schema(
        operation_description="Leave feedback for a class (Member only)",
        request_body=FeedbackSerializer,
        responses={201: FeedbackSerializer, 403: "Forbidden"}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(member=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
