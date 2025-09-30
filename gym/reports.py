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
        report = Subscription.objects.values('plan__name').annotate(total_members=Count('user'),total_earnings=Sum('plan__price'))
        return Response(report)
    
    
class AttendanceReport(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        report = Attendance.objects.values('fitness_class__name').annotate(present_count=Count('id',filter=Q(status='present')), absent_count=Count('id', filter=Q(status='absent')))
        return Response(report)
    

class FeedbackReport(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        report = Feedback.objects.values('fitness_class__name').annotate(avg_rating=Avg('rating'),total_feedbacks=Count('id'))
        return Response(report)