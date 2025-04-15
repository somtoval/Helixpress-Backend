from django.contrib import admin
from .models import Journal, Subject, Volume, Issue, Paper, Submission, Newsletter, HomeSlider, News, Topic, Blog

class JournalAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbrv', 'impact', 'issn', 'date_created']
    search_fields = ['name', 'issn', 'subject__name']
    list_filter = ['date_created', 'subject']
    ordering = ['-date_created']

class VolumeAdmin(admin.ModelAdmin):
    list_display = ['number', 'journal', 'date_created']
    search_fields = ['journal__name', 'number']
    list_filter = ['date_created']
    ordering = ['-date_created']

class IssueAdmin(admin.ModelAdmin):
    list_display = ['number', 'volume', 'journal', 'special', 'date_created']
    search_fields = ['journal__name', 'volume__number']
    list_filter = ['special', 'date_created']
    ordering = ['-date_created']

class PaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'journal', 'volume', 'issue', 'date_created']
    search_fields = ['title', 'author', 'journal__name', 'keywords']
    list_filter = ['journal', 'volume', 'issue', 'date_created']
    ordering = ['-date_created']

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'email', 'status', 'date_submitted']
    search_fields = ['firstname', 'lastname', 'email', 'institution']
    list_filter = ['status', 'date_submitted']
    ordering = ['-date_submitted']

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'journal']
    search_fields = ['email', 'journal__name']
    list_filter = ['journal']
    ordering = ['-id']

class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created']
    search_fields = ['title', 'body']
    list_filter = ['date_created']
    ordering = ['-date_created']

# Register models
admin.site.register(Subject)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Volume, VolumeAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(HomeSlider, HomeSliderAdmin)
admin.site.register(News)
admin.site.register(Blog)
admin.site.register(Topic)