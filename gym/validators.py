from rest_framework import serializers
from .models import ClassBooking

def validate_class_capacity(fitness_class):
    """
    Validator to check if the fitness class has reached its capacity.
    Counts active bookings in ClassBooking model.
    """
    current_bookings_count = ClassBooking.objects.filter(
        fitness_class=fitness_class, 
        status='booked'
    ).count()
    
    if current_bookings_count >= fitness_class.capacity:
        raise serializers.ValidationError(
            f"This class is full. Capacity: {fitness_class.capacity}, Booked: {current_bookings_count}"
        )
