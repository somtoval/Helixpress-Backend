# serializers.py
from rest_framework import serializers
from .models import Journal, Volume, Issue, Paper, Submission, Newsletter, HomeSlider, Subject, News, Topic, UserProfile, Blog
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class JournalSerializer(serializers.ModelSerializer):
    article_count = serializers.ReadOnlyField()
    class Meta:
        model = Journal
        fields = [
            'id', 'name', 'about', 'abbrv', 'impact', 'issn', 'date_created', 'subject', 
            'aim_scope', 'reviewer_board', 'author_instructions', 'article_processing_charge', 
            'indexing_and_archiving', 'article_count', 'editors', 'reviewers'
        ]

class VolumeSerializer(serializers.ModelSerializer):
    # journal = JournalSerializer()
    # Optional or just leave it
    # journal = serializers.PrimaryKeyRelatedField(queryset=Journal.objects.all())

    class Meta:
        model = Volume
        fields = ['id', 'number', 'journal', 'date_created']

class IssueSerializer(serializers.ModelSerializer):
    # volume = VolumeSerializer()
    # journal = JournalSerializer()

    class Meta:
        model = Issue
        fields = ['id', 'number', 'volume', 'journal', 'special', 'date_created']

class PaperSerializer(serializers.ModelSerializer):
    # volume = VolumeSerializer()
    # issue = IssueSerializer()
    # journal = JournalSerializer()

    class Meta:
        model = Paper
        fields = ['id', 'title', 'author', 'description', 'institution', 'keywords', 'volume', 'issue', 'journal', 'document', 'date_created', 'doi', 'editorsChoice', 'view_count']

class TopicSerializer(serializers.ModelSerializer):
    computed_status = serializers.ReadOnlyField()

    class Meta:
        model = Topic
        fields = ['id', 'title', 'deadline', 'viewed_by', 'content', 'keywords', 'participating_journals', 'editors', 'computed_status']

class SubmissionSerializer(serializers.ModelSerializer):
    # journal = JournalSerializer()

    class Meta:
        model = Submission
        fields = ['id', 'firstname', 'lastname', 'email', 'phonenumber', 'institution', 'country', 'manuscript', 'supplementary', 'journal', 'status', 'date_submitted']

class NewsletterSerializer(serializers.ModelSerializer):
    # journal = JournalSerializer()

    class Meta:
        model = Newsletter
        fields = ['id', 'email', 'journal']

class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = '__all__'

class HomeSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSlider
        fields = ['id', 'title', 'body', 'pic', 'date_created']

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    computed_status = serializers.ReadOnlyField()

    class Meta:
        model = Topic
        fields = ['id', 'title', 'deadline', 'viewed_by', 'content', 'keywords', 'computed_status',
                'participating_journals', 
                'editors', 
                ]

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},  # To ensure password is not returned
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'interests', 'profiles', 'profile_picture']

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    bio = serializers.CharField(required=False, allow_blank=True)
    interests = serializers.CharField(required=False, allow_blank=True)
    profiles = serializers.JSONField(required=False, default=dict)
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    def create(self, validated_data):
        first_name=validated_data['first_name'],
        email=validated_data['email'],
        username = f'{first_name}:{email}'

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        # Now create the user profile
        UserProfile.objects.create(
            user=user,
            bio=validated_data.get('bio', ''),
            interests=validated_data.get('interests', ''),
            profiles=validated_data.get('profiles', {}),
            profile_picture=validated_data.get('profile_picture', None)
        )

        return user
    
class EmailTokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if not email or not password:
            raise serializers.ValidationError(
                {"detail": "Email and password are required"}
            )
        
        # Find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "No active account found with the given credentials"}
            )
        
        # Check password
        if not user.check_password(password):
            raise serializers.ValidationError(
                {"detail": "No active account found with the given credentials"}
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Add tokens to response
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        attrs['user'] = user
        
        return attrs
