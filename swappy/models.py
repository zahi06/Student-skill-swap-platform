from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

# ------------------------------
# User Profile Model
# ------------------------------
class Student(models.Model):
    AVAILABILITY_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('weekends', 'Weekends'),
        ('flexible', 'Flexible'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    bio = models.TextField(blank=True, null=True)
    availability = models.CharField(
        max_length=20, 
        choices=AVAILABILITY_CHOICES, 
        default='flexible'
    )
    # --- PREMIUM STATUS ---
    is_premium = models.BooleanField(default=False) 
    premium_since = models.DateTimeField(null=True, blank=True) # New Field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @property
    def premium_expiry(self):
        if self.premium_since:
            return self.premium_since + timedelta(days=30)
        return None

    @property
    def days_left(self):
        if self.premium_expiry:
            delta = self.premium_expiry - timezone.now()
            return max(0, delta.days)
        return 0


# ------------------------------
# Skill Models
# ------------------------------
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SkillOffer(models.Model):
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='offered_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)

    class Meta:
        unique_together = ('student', 'skill')

    def __str__(self):
        return f"{self.student.user.username} - {self.skill.name}"

    @property
    def is_premium_skill(self):
        return self.proficiency_level == 'Advanced'


class SkillRequest(models.Model):
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='requested_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    desired_proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)

    class Meta:
        unique_together = ('student', 'skill')

    def __str__(self):
        return f"{self.student.user.username} wants {self.skill.name}"


# ------------------------------
# Networking & Connection Model
# ------------------------------
class Connection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'), 
        ('completed', 'Completed'), 
    ]

    sender = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='sent_connections')
    receiver = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='received_connections')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False) 

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


# ------------------------------
# Communication Models
# ------------------------------
class Message(models.Model):
    sender = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"


class Notification(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='notifications')
    from_user = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')
    type = models.CharField(max_length=50, default='general') 
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.student.user.username}: {self.message}"