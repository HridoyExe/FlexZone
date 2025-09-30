from django.contrib import admin
from .models import Membership, Subscription, FitnessClass, ClassBooking, Attendance, Payment, Feedback

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days')
    search_fields = ('name',)
    list_filter = ('duration_days',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'status')
    search_fields = ('user__username', 'plan__name')
    list_filter = ('status', 'plan')

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor', 'schedule_time', 'capacity')
    search_fields = ('name', 'instructor__username')
    list_filter = ('schedule_time',)

@admin.register(ClassBooking)
class ClassBookingAdmin(admin.ModelAdmin):
    list_display = ('member', 'fitness_class', 'booking_date', 'status')
    search_fields = ('member__username', 'fitness_class__name')
    list_filter = ('status', 'booking_date')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('fitness_class', 'member', 'date', 'status')
    search_fields = ('fitness_class__name', 'member__username')
    list_filter = ('status', 'date')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription', 'class_booking', 'amount', 'status', 'method', 'date')
    search_fields = ('user__username',)
    list_filter = ('status', 'method')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('fitness_class', 'member', 'rating', 'date')
    search_fields = ('fitness_class__name', 'member__username')
    list_filter = ('rating', 'date')
