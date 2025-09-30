from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Membership, Subscription, FitnessClass, ClassBooking, Attendance, Payment, Feedback
from .serializers import (
    MembershipSerializer, SubscriptionSerializer, FitnessClassSerializer,
    ClassBookingSerializer, AttendanceSerializer, PaymentSerializer, FeedbackSerializer
)

from gym.permission import IsOwnerOrAdmin, IsStaffOrAdmin, ReadOnlyOrAdmin 
from users.permissions import IsAdmin, IsMember,IsStaff

class MembershipViewSet(viewsets.ModelViewSet):
    """
    Membership Plan CRUD: Staff/Admin can manage; all authenticated users can view.
    """
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsStaffOrAdmin()]

class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    User Subscriptions: Member can buy; Owner/Staff/Admin can view/manage.
    """
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Subscription.objects.none()
            
        if user.role in ['ADMIN', 'STAFF']:
            return Subscription.objects.all()
        if user.role == 'MEMBER':
            return Subscription.objects.filter(user=user)
        
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

class FitnessClassViewSet(viewsets.ModelViewSet):
    """
    Fitness Classes: Staff/Admin can manage; all authenticated users can view.
    """
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsStaffOrAdmin()]

    def perform_create(self, serializer):
        if self.request.user.role == 'STAFF':
            serializer.save(instructor=self.request.user)
        else:
            serializer.save()

class ClassBookingViewSet(viewsets.ModelViewSet):
    """
    Class Bookings: Member can create; Owner/Staff/Admin can view/manage.
    """
    serializer_class = ClassBookingSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if not user.is_authenticated:
            return ClassBooking.objects.none()
            
        if user.role in ['ADMIN', 'STAFF']:
            return ClassBooking.objects.all()
        
        if user.role == 'MEMBER':
            return ClassBooking.objects.filter(member=user)
            
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
        responses={201: ClassBookingSerializer, 403: "Forbidden"}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(member=request.user) 
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AttendanceViewSet(viewsets.ModelViewSet):
    """
    Attendance Tracking: Staff/Admin can mark; Owner/Staff/Admin can view.
    """
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Attendance.objects.none()
        if user.role in ['ADMIN', 'STAFF']:
            return Attendance.objects.all()
        if user.role == 'MEMBER':
            return Attendance.objects.filter(member=user)
            
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

class PaymentViewSet(viewsets.ModelViewSet):
    """
    Payments: Member can create (pay); Owner/Staff/Admin can view/manage.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Payment.objects.none()
        if user.role in ['ADMIN', 'STAFF']:
            return Payment.objects.all()
        if user.role == 'MEMBER':
            return Payment.objects.filter(user=user)
        return Payment.objects.none()

    def get_permissions(self):

        
        if self.action == 'create':
            return [IsMember()]
        
        user = self.request.user
        if not user.is_authenticated:
            return [IsAuthenticated()]
        if user.role in ['STAFF', 'ADMIN']:
            return [IsStaffOrAdmin()]
        
        return [IsOwnerOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    Feedback & Reviews: Member can create; Owner/Staff/Admin can view/manage.
    """
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Feedback.objects.none()
            
        if user.role == 'ADMIN':
            return Feedback.objects.all()
        if user.role == 'STAFF':
        
            return Feedback.objects.filter(fitness_class__instructor=user)
        if user.role == 'MEMBER':
        
            return Feedback.objects.filter(member=user)
            
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