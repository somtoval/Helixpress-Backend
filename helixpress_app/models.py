from django.db import models
import uuid
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# class Role(models.Model):
#     name = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name

class UserProfile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # roles = models.ManyToManyField('Role') # Now that we are passing reviewer and editor as attributes to journal it isn't necessary to have role attribute in the userprofile, it's just redundant because youcan determine whether a user is an editor or a reviewer by checking if they are associated with the Journal as an editor or reviewer.
    bio = models.TextField(null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
    profiles = models.JSONField(default=dict, null=True, blank=True)  # Store profile links as a JSON field
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Subject(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Journal(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    about = models.CharField(max_length=20000, null=True, blank=True)
    abbrv = models.CharField(max_length=200, null=True, blank=True)
    impact = models.CharField(max_length=200, null=True, blank=True)
    pic = models.ImageField(upload_to='journals_pics/', null=False, blank=False)
    issn = models.CharField(max_length=200, null=True, blank=True)
    subject = models.ManyToManyField(Subject, blank=True, related_name='journals')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    aim_scope = models.TextField(null=True, blank=True)
    reviewer_board = models.TextField(null=True, blank=True)
    author_instructions = models.TextField(null=True, blank=True)
    article_processing_charge = models.TextField(null=True, blank=True)
    indexing_and_archiving = models.TextField(null=True, blank=True)

    editors = models.ManyToManyField(UserProfile, related_name='editor_journals', blank=True)
    reviewers = models.ManyToManyField(UserProfile, related_name='reviewer_journals', blank=True)

    def __str__(self):
        return self.name

    @property
    def article_count(self):
        papers = self.paper_set.all()
        return papers.count()

class Volume(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    number = models.IntegerField(null=True)
    journal = models.ForeignKey(Journal, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.number} {self.journal.name}"

class Issue(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    number = models.IntegerField(null=True)
    volume = models.ForeignKey(Volume, null=True, on_delete=models.CASCADE)
    journal = models.ForeignKey(Journal, null=True, on_delete=models.CASCADE)
    special = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Issue:{self.number} < Volume:{self.volume.number} < {self.volume.journal.name}"

class Paper(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    title = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)
    institution = models.CharField(max_length=200, null=True)
    keywords = models.TextField(null=True, blank=True)
    volume = models.ForeignKey(Volume, null=True, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, null=True, on_delete=models.CASCADE)
    journal = models.ForeignKey(Journal, null=True, on_delete=models.CASCADE)
    document = models.FileField(upload_to='published_papers/%Y/%m/%d/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    doi = models.CharField(max_length=200, null=True)
    editorsChoice = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    phonenumber = models.CharField(max_length=200, null=True)
    institution = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    manuscript = models.FileField(upload_to='submitted_manuscripts/%Y/%m/%d/')
    supplementary = models.FileField(upload_to='supplementary_papers/%Y/%m/%d/', null=True, blank=True)
    journal = models.ForeignKey(Journal, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date_submitted = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Newsletter(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    journal = models.ForeignKey(Journal, null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.email

class HomeSlider(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    title = models.CharField(max_length=200, null=True)
    body = models.TextField(null=True)
    pic = models.ImageField(null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
    
class News(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    title = models.CharField(max_length=200, null=True)
    body = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
    
class Blog(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    title = models.CharField(max_length=200, null=True)
    body = models.TextField(null=True)
    author = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
    
class Topic(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed')
    ]
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    title = models.CharField(max_length=200, null=True)
    deadline = models.DateTimeField(null=True)
    viewed_by = models.PositiveIntegerField(default=0)
    content = models.TextField(null=True)
    keywords = models.TextField(null=True)
    participating_journals = models.ManyToManyField(Journal, related_name='topics')
    editors = models.ManyToManyField(UserProfile, related_name='editor_topics', blank=True)

    def __str__(self):
        return self.title
    
    @property
    def computed_status(self):
        if self.deadline and timezone.now() > self.deadline:
            return 'closed'
        return 'open'
