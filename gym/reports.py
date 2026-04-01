from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Count, Avg, Sum, Q
from .models import Subscription, Attendance, Feedback
  
class MemberShipReport(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        report = Subscription.objects.values('plan__name').annotate(total_member=Count('user'),total_earn=Sum('plan__price'))
        return Response(report)
    

class SubscriptionReport(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        report = Subscription.objects.all().order_by('-id')[:10].values(
            'user__email', 'plan__name', 'status'
        )
        # Rename keys for frontend compatibility
        formatted_report = [
            {
                'user_name': item['user__email'],
                'plan_name': item['plan__name'],
                'status': item['status']
            }
            for item in report
        ]
        return Response(formatted_report)
    
    
class AttendanceReport(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # Using -id for ordering to be consistent and reliable
        report = Attendance.objects.all().order_by('-id')[:10].values(
            'member__email', 'fitness_class__name', 'date', 'status'
        )
        # Rename keys and ensure dates are strings
        formatted_report = [
            {
                'member_name': item['member__email'],
                'class_name': item['fitness_class__name'] or 'General Session',
                'date': str(item['date']),
                'status': item['status']
            }
            for item in report
        ]
        return Response(formatted_report)
    

class FeedbackReport(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        report = Feedback.objects.all().order_by('-id')[:10].values(
            'member__email', 'fitness_class__name', 'rating', 'comment'
        )
        # Rename keys for frontend compatibility
        formatted_report = [
            {
                'member_name': item['member__email'],
                'class_name': item['fitness_class__name'],
                'rating': item['rating'],
                'comment': item['comment']
            }
            for item in report
        ]
        return Response(formatted_report)