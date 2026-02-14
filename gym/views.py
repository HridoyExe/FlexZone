from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

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
