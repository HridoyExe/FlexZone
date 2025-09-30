from rest_framework import serializers
from .models import Membership, Subscription, FitnessClass, ClassBooking, Attendance, Payment, Feedback
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'role')
        ref_name = "UserGymApp"

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    plan = serializers.PrimaryKeyRelatedField(queryset=Membership.objects.all())
    start_date = serializers.DateField(format="%Y-%m-%d")
    end_date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Subscription
        fields = '__all__'

class FitnessClassSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    booked_members_count = serializers.SerializerMethodField()
    schedule_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = FitnessClass
        fields = '__all__'
    
        read_only_fields = ['booked_members'] 

    def get_booked_members_count(self, obj):
        return obj.booked_members.count()

class ClassBookingSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)
    fitness_class = serializers.PrimaryKeyRelatedField(queryset=FitnessClass.objects.all())
    booking_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ClassBooking
        fields = '__all__'
        read_only_fields = ['member', 'booking_date']

class AttendanceSerializer(serializers.ModelSerializer):
    member = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    fitness_class = serializers.PrimaryKeyRelatedField(queryset=FitnessClass.objects.all())
    date = serializers.DateField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    subscription = serializers.PrimaryKeyRelatedField(queryset=Subscription.objects.all(), allow_null=True, required=False)
    class_booking = serializers.PrimaryKeyRelatedField(queryset=ClassBooking.objects.all(), allow_null=True, required=False)
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['user', 'date']

class FeedbackSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)
    fitness_class = serializers.PrimaryKeyRelatedField(queryset=FitnessClass.objects.all())
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['member', 'date']
