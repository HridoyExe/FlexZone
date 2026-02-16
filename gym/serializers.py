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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            # Ensure we return the full URL for Cloudinary images
            representation['image'] = instance.image.url if hasattr(instance.image, 'url') else str(instance.image)
        return representation

class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    plan = serializers.PrimaryKeyRelatedField(queryset=Membership.objects.all())
    start_date = serializers.DateField(format="%Y-%m-%d", read_only=True)
    end_date = serializers.DateField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Include full details of the plan
        representation['plan'] = MembershipSerializer(instance.plan).data
        # Include essential user info if needed
        representation['plan_name'] = instance.plan.name
        return representation

class FitnessClassSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    booked_members_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    schedule_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    
    class Meta:
        model = FitnessClass
        fields = ('id', 'name', 'instructor', 'description', 'capacity', 'image', 'schedule_time', 'booked_members_count', 'average_rating', 'total_reviews')
        read_only_fields = ['booked_members'] 

    def get_booked_members_count(self, obj):
        return obj.booked_members.count()

    def get_average_rating(self, obj):
        from .models import Feedback
        feedbacks = Feedback.objects.filter(fitness_class=obj)
        if not feedbacks.exists():
            return 0
        avg = sum(f.rating for f in feedbacks) / feedbacks.count()
        return round(avg, 1)

    def get_total_reviews(self, obj):
        from .models import Feedback
        return Feedback.objects.filter(fitness_class=obj).count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation['image'] = instance.image.url if hasattr(instance.image, 'url') else str(instance.image)
        return representation

from .validators import validate_class_capacity

class ClassBookingSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)
    fitness_class = serializers.PrimaryKeyRelatedField(
        queryset=FitnessClass.objects.all(),
        validators=[validate_class_capacity]
    )
    booking_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ClassBooking
        fields = '__all__'
        read_only_fields = ['member', 'booking_date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Include full details of the fitness class
        representation['fitness_class'] = FitnessClassSerializer(instance.fitness_class).data
        return representation

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
