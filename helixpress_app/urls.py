# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

# Create the router
router = DefaultRouter()
router.register(r'subjects', views.SubjectViewSet)
router.register(r'journals', views.JournalViewSet)
router.register(r'volumes', views.VolumeViewSet)
router.register(r'issues', views.IssueViewSet)
router.register(r'papers', views.PaperViewSet, basename='paper')  # Add basename
router.register(r'submissions', views.SubmissionViewSet)
router.register(r'newsletters', views.NewsletterViewSet)
router.register(r'homesliders', views.HomeSliderViewSet)
router.register(r'news', views.NewsViewSet)
router.register(r'topics', views.TopicViewSet)
router.register(r'blogs', views.BlogViewSet)

urlpatterns = [
    # Registration & Authentication paths
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.EmailTokenObtainView.as_view(), name='login'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Custom search paths
    path('papers/search/', views.PaperSearchView.as_view(), name='paper-search'),
    path('topics/search/', views.TopicSearchView.as_view(), name='topic-search'),
    
    # Other explicit paths
    path('subjects/<uuid:subject_id>/journals/', views.JournalsInSubjectView.as_view(), name='journals-in-subject'),
    path('journals/<uuid:journal_id>/volumes/', views.VolumesInJournalView.as_view(), name='volumes-in-journal'),
    path('journals/<uuid:journal_id>/papers/', views.PapersInJournalView.as_view(), name='papers-in-journal'),
    path('volumes/<uuid:volume_id>/issues/', views.IssuesInVolumeView.as_view(), name='issues-in-volume'),
    path('issues/<uuid:issue_id>/papers/', views.PapersInIssueView.as_view(), name='papers-in-issue'),
    path('highly-accessed-papers/', views.HighlyAccessedPapersView.as_view(), name='highly-accessed-papers'),
    path('users/', views.UsersView.as_view(), name='all-users'),

    # Include router URLs last
    path('', include(router.urls)),
]