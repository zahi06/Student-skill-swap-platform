from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    AVAILABILITY_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('weekends', 'Weekends'),
        ('flexible', 'Flexible'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_availability_display(self):
        if not self.availability:
            return "Not specified"
        return dict(self.AVAILABILITY_CHOICES).get(self.availability, "Not specified")


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SkillOffer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='offered_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(
        max_length=20,
        choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced'),
        ]
    )

    class Meta:
        unique_together = ('student', 'skill')

    def __str__(self):
        return f"{self.student.user.username} - {self.skill.name}"


class SkillRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='requested_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    desired_proficiency = models.CharField(
        max_length=20,
        choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced'),
        ]
    )

    class Meta:
        unique_together = ('student', 'skill')

    def __str__(self):
        return f"{self.student.user.username} wants {self.skill.name}"


class Connection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='sent_connections')
    receiver = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='received_connections')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"