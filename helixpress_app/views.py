from rest_framework import viewsets, generics, filters, status, views
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Journal, Volume, Issue, Paper, Submission, Newsletter, HomeSlider, Subject, News, Topic, UserProfile, Blog
from .serializers import JournalSerializer, VolumeSerializer, IssueSerializer, PaperSerializer, SubmissionSerializer, NewsletterSerializer, HomeSliderSerializer, SubjectSerializer, NewsSerializer, TopicSerializer, RegisterSerializer, EmailTokenObtainSerializer, UserSerializer, BlogSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

import logging
logger = logging.getLogger(__name__)

# Pagination class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Custom default page size
    page_size_query_param = 'page_size'
    max_page_size = 100  # Max results per page

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class JournalsInSubjectView(generics.ListAPIView):
    serializer_class = JournalSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        subject_id = self.kwargs['subject_id']  # Get the subject_id from URL
        return Journal.objects.filter(subject__id=subject_id)
    
class UsersView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Received journal ID: {kwargs}")
        return super().retrieve(request, *args, **kwargs)

class VolumesInJournalView(generics.ListAPIView):
    serializer_class = VolumeSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        journal_id = self.kwargs['journal_id']  # Get the journal_id from URL
        return Volume.objects.filter(journal__id=journal_id)

class PapersInJournalView(generics.ListAPIView):
    serializer_class = PaperSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        journal_id = self.kwargs['journal_id']  # Get the journal_id from URL
        return Paper.objects.filter(journal__id=journal_id)

class VolumeViewSet(viewsets.ModelViewSet):
    queryset = Volume.objects.all()
    serializer_class = VolumeSerializer

class IssuesInVolumeView(generics.ListAPIView):
    serializer_class = IssueSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        volume_id = self.kwargs['volume_id']  # Get the volume_id from URL
        return Issue.objects.filter(volume__id=volume_id)

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class PapersInIssueView(generics.ListAPIView):
    serializer_class = PaperSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        issue_id = self.kwargs['issue_id']  # Get the issue_id from URL
        return Paper.objects.filter(issue__id=issue_id)

class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class PaperSearchView(generics.ListAPIView):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'keywords', 'author', 'journal__name', 'author__email']  # Fields to search on
    ordering_fields = ['title', 'created_at']
    pagination_class = StandardResultsSetPagination

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

class HomeSliderViewSet(viewsets.ModelViewSet):
    queryset = HomeSlider.objects.all()
    serializer_class = HomeSliderSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-date_created')
    serializer_class = NewsSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_created', 'title']

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-date_created')
    serializer_class = BlogSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_created', 'title']

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all().order_by('-deadline')
    serializer_class = TopicSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['deadline', 'title']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.viewed_by += 1
        instance.save(update_fields=['viewed_by'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class TopicSearchView(generics.ListAPIView):
    serializer_class = TopicSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # This line fetches all Topic objects and tells Django to prefetch the related participating_journals and editors for each topic efficiently.
        queryset = Topic.objects.all().prefetch_related('participating_journals', 'editors')
        
        title = self.request.query_params.get('title', None)
        journal_id = self.request.query_params.get('journal', None)
        status = self.request.query_params.get('status', None)
        subject_id = self.request.query_params.get('subject', None)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if journal_id:
            queryset = queryset.filter(participating_journals__id=journal_id)

        if subject_id:
            queryset = queryset.filter(participating_journals__subject__id=subject_id)

        if status:
            if status.lower() == 'closed':
                queryset = queryset.filter(deadline__lt=timezone.now())
            elif status.lower() == 'open':
                queryset = queryset.filter(deadline__gte=timezone.now())

        return queryset.distinct()


class HighlyAccessedPapersView(views.APIView):
    def get(self, request):
        papers = Paper.objects.all().order_by('-view_count')[:10]
        serializer = PaperSerializer(papers, many=True)
        return Response(serializer.data)
    
class RegisterView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # This will create both the user and user profile
            return Response({
                'message': 'User registered successfully.',
                'user': RegisterSerializer(user).data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmailTokenObtainView(views.APIView):
    def post(self, request):
        serializer = EmailTokenObtainSerializer(data=request.data)
        
        if serializer.is_valid():
            return Response({
                'refresh': serializer.validated_data['refresh'],
                'access': serializer.validated_data['access'],
                'user_id': serializer.validated_data['user'].id,
                'email': serializer.validated_data['user'].email
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete the user's refresh token to logout
            RefreshToken.for_user(request.user).blacklist()
            return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)