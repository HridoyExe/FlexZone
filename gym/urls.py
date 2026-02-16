from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .reports import MemberShipReport, AttendanceReport, FeedbackReport,SubscriptionReport

from .views import (
    MembershipViewSet, SubscriptionViewSet, FitnessClassViewSet,
    ClassBookingViewSet, AttendanceViewSet, PaymentViewSet, FeedbackViewSet,
    initiate_payment, payment_success, payment_fail, payment_cancel
)


router = DefaultRouter()
router.register('memberships', MembershipViewSet, basename='membership')
router.register('subscriptions', SubscriptionViewSet, basename='subscription')
router.register('payments', PaymentViewSet, basename='payment')
router.register('fitness-classes', FitnessClassViewSet, basename='fitnessclass')
router.register('class-bookings', ClassBookingViewSet, basename='classbooking')
router.register('attendance', AttendanceViewSet, basename='attendance')
router.register('feedbacks', FeedbackViewSet, basename='feedback')

fitness_router = routers.NestedDefaultRouter(router, 'fitness-classes', lookup='fitness_class')
fitness_router.register('bookings', ClassBookingViewSet, basename='fitness-class-bookings')
fitness_router.register('attendance', AttendanceViewSet, basename='fitness-class-attendance')
fitness_router.register('feedbacks', FeedbackViewSet, basename='fitness-class-feedbacks')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(fitness_router.urls)),
    # SSLCommerz Payment URLs
    path('payments/initiate/', initiate_payment, name='initiate-payment'),
    path('payments/success/', payment_success, name='payment-success'),
    path('payments/fail/', payment_fail, name='payment-fail'),
    path('payments/cancel/', payment_cancel, name='payment-cancel'),
    path('reports/membership/', MemberShipReport.as_view(), name='membership-report'),
    path('reports/attendance/', AttendanceReport.as_view(), name='attendance-report'),
    path('reports/subscriptions/',SubscriptionReport.as_view(),name='subscriptions-report'),
    path('reports/feedback/', FeedbackReport.as_view(), name='feedback-report'),
]
