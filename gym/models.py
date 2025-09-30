from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Membership(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(help_text="Duration in days")

    def __str__(self):
        return f"{self.name} - {self.price}"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'member'})
    plan = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=(('active','Active'), ('inactive','Inactive')),
        default='active'
    )

    def __str__(self):
        return f"{self.user} - {self.plan} ({self.status})"

class FitnessClass(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role':'staff'})
    schedule_time = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    booked_members = models.ManyToManyField(User, blank=True, related_name='booked_classes', limit_choices_to={'role':'member'})

    def __str__(self):
        return f"{self.name} by {self.instructor}"


class ClassBooking(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'member'})
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('booked','Booked'), ('cancelled','Cancelled')), default='booked')

    class Meta:
        unique_together = ('member', 'fitness_class')

    def __str__(self):
        return f"{self.member} - {self.fitness_class} ({self.status})"

class Attendance(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'member'})
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('present','Present'), ('absent','Absent')), default='absent')

    class Meta:
        unique_together = ('fitness_class', 'member', 'date')

    def __str__(self):
        return f"{self.member} - {self.fitness_class} ({self.status})"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    class_booking = models.ForeignKey(ClassBooking, on_delete=models.SET_NULL, null=True, blank=True)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('success','Success'), ('failed','Failed')), default='success')
    method = models.CharField(max_length=50, default='Cash/Manual')

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.status})"

class Feedback(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'member'})
    rating = models.PositiveIntegerField(default=5, choices=[(i,i) for i in range(1,6)])  
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.fitness_class} ({self.rating})"
