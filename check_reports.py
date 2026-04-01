import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_management.settings')
django.setup()

from gym.models import Subscription, Attendance, Feedback

print("Checking Subscriptions...")
try:
    s = Subscription.objects.all().values('user__email', 'plan__name', 'status')[:1]
    print("Subscription OK:", list(s))
except Exception as e:
    print("Subscription Error:", e)

print("\nChecking Attendance...")
try:
    a = Attendance.objects.all().values('member__email', 'fitness_class__name', 'date', 'status')[:1]
    print("Attendance OK:", list(a))
except Exception as e:
    print("Attendance Error:", e)

print("\nChecking Feedback...")
try:
    f = Feedback.objects.all().values('member__email', 'fitness_class__name', 'rating', 'comment')[:1]
    print("Feedback OK:", list(f))
except Exception as e:
    print("Feedback Error:", e)
