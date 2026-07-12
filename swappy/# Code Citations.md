# Code Citations

## License: unknown
https://github.com/Hwang-Kyu-Cheol/CigaretteProject_withGit/blob/6008f9e4f5059b1db22fdddb09f63ed9470f0cdd/Member_App/views.py

```
I've analyzed your EduSwap codebase and identified several frontend and backend issues. Here are the problems and fixes:

## Issues Found:

### **Backend Issues:**

1. **Missing `get_availability_display()` method** - Student model doesn't have this
2. **Skills parsing in registration** - Skills are accepted but never processed
3. **No validation in skill operations** - Missing error handling
4. **Race condition in connection creation** - Duplicate connections possible
5. **Missing imports in views** - Some views may have issues

### **Frontend Issues:**

1. **Profile page shows wrong availability format** - Using undefined method
2. **Skill offer/request forms don't load existing skills** - Should show dropdown
3. **Register form collects skills but doesn't use them** - Data loss
4. **Missing error handling in some templates**

## Fixes:

### 1. Fix [swappy/models.py](swappy/models.py):

````python
// filepath: swappy/models.py
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    availability = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening'),
            ('weekends', 'Weekends'),
            ('flexible', 'Flexible'),
        ],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_availability_display(self):
        """Return human-readable availability"""
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

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"
````

### 2. Fix [swappy/views.py](swappy/views.py):

````python
// filepath: swappy/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Student, Skill, SkillOffer, SkillRequest, Connection


# Home Page
def home(request):
    return render(request, 'home.html')


# Register
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        skills_teach = request.POST.get('skills_teach', '')
        skills
```


## License: unknown
https://github.com/Hwang-Kyu-Cheol/CigaretteProject_withGit/blob/6008f9e4f5059b1db22fdddb09f63ed9470f0cdd/Member_App/views.py

```
I've analyzed your EduSwap codebase and identified several frontend and backend issues. Here are the problems and fixes:

## Issues Found:

### **Backend Issues:**

1. **Missing `get_availability_display()` method** - Student model doesn't have this
2. **Skills parsing in registration** - Skills are accepted but never processed
3. **No validation in skill operations** - Missing error handling
4. **Race condition in connection creation** - Duplicate connections possible
5. **Missing imports in views** - Some views may have issues

### **Frontend Issues:**

1. **Profile page shows wrong availability format** - Using undefined method
2. **Skill offer/request forms don't load existing skills** - Should show dropdown
3. **Register form collects skills but doesn't use them** - Data loss
4. **Missing error handling in some templates**

## Fixes:

### 1. Fix [swappy/models.py](swappy/models.py):

````python
// filepath: swappy/models.py
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    availability = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening'),
            ('weekends', 'Weekends'),
            ('flexible', 'Flexible'),
        ],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_availability_display(self):
        """Return human-readable availability"""
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

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"
````

### 2. Fix [swappy/views.py](swappy/views.py):

````python
// filepath: swappy/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Student, Skill, SkillOffer, SkillRequest, Connection


# Home Page
def home(request):
    return render(request, 'home.html')


# Register
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        skills_teach = request.POST.get('skills_teach', '')
        skills
```


## License: unknown
https://github.com/Hwang-Kyu-Cheol/CigaretteProject_withGit/blob/6008f9e4f5059b1db22fdddb09f63ed9470f0cdd/Member_App/views.py

```
I've analyzed your EduSwap codebase and identified several frontend and backend issues. Here are the problems and fixes:

## Issues Found:

### **Backend Issues:**

1. **Missing `get_availability_display()` method** - Student model doesn't have this
2. **Skills parsing in registration** - Skills are accepted but never processed
3. **No validation in skill operations** - Missing error handling
4. **Race condition in connection creation** - Duplicate connections possible
5. **Missing imports in views** - Some views may have issues

### **Frontend Issues:**

1. **Profile page shows wrong availability format** - Using undefined method
2. **Skill offer/request forms don't load existing skills** - Should show dropdown
3. **Register form collects skills but doesn't use them** - Data loss
4. **Missing error handling in some templates**

## Fixes:

### 1. Fix [swappy/models.py](swappy/models.py):

````python
// filepath: swappy/models.py
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    availability = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening'),
            ('weekends', 'Weekends'),
            ('flexible', 'Flexible'),
        ],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_availability_display(self):
        """Return human-readable availability"""
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

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"
````

### 2. Fix [swappy/views.py](swappy/views.py):

````python
// filepath: swappy/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Student, Skill, SkillOffer, SkillRequest, Connection


# Home Page
def home(request):
    return render(request, 'home.html')


# Register
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        skills_teach = request.POST.get('skills_teach', '')
        skills
```


## License: unknown
https://github.com/Hwang-Kyu-Cheol/CigaretteProject_withGit/blob/6008f9e4f5059b1db22fdddb09f63ed9470f0cdd/Member_App/views.py

```
I've analyzed your EduSwap codebase and identified several frontend and backend issues. Here are the problems and fixes:

## Issues Found:

### **Backend Issues:**

1. **Missing `get_availability_display()` method** - Student model doesn't have this
2. **Skills parsing in registration** - Skills are accepted but never processed
3. **No validation in skill operations** - Missing error handling
4. **Race condition in connection creation** - Duplicate connections possible
5. **Missing imports in views** - Some views may have issues

### **Frontend Issues:**

1. **Profile page shows wrong availability format** - Using undefined method
2. **Skill offer/request forms don't load existing skills** - Should show dropdown
3. **Register form collects skills but doesn't use them** - Data loss
4. **Missing error handling in some templates**

## Fixes:

### 1. Fix [swappy/models.py](swappy/models.py):

````python
// filepath: swappy/models.py
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    availability = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening'),
            ('weekends', 'Weekends'),
            ('flexible', 'Flexible'),
        ],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_availability_display(self):
        """Return human-readable availability"""
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

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"
````

### 2. Fix [swappy/views.py](swappy/views.py):

````python
// filepath: swappy/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Student, Skill, SkillOffer, SkillRequest, Connection


# Home Page
def home(request):
    return render(request, 'home.html')


# Register
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        skills_teach = request.POST.get('skills_teach', '')
        skills
```


## License: unknown
https://github.com/Hwang-Kyu-Cheol/CigaretteProject_withGit/blob/6008f9e4f5059b1db22fdddb09f63ed9470f0cdd/Member_App/views.py

```
I've analyzed your EduSwap codebase and identified several frontend and backend issues. Here are the problems and fixes:

## Issues Found:

### **Backend Issues:**

1. **Missing `get_availability_display()` method** - Student model doesn't have this
2. **Skills parsing in registration** - Skills are accepted but never processed
3. **No validation in skill operations** - Missing error handling
4. **Race condition in connection creation** - Duplicate connections possible
5. **Missing imports in views** - Some views may have issues

### **Frontend Issues:**

1. **Profile page shows wrong availability format** - Using undefined method
2. **Skill offer/request forms don't load existing skills** - Should show dropdown
3. **Register form collects skills but doesn't use them** - Data loss
4. **Missing error handling in some templates**

## Fixes:

### 1. Fix [swappy/models.py](swappy/models.py):

````python
// filepath: swappy/models.py
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    availability = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening'),
            ('weekends', 'Weekends'),
            ('flexible', 'Flexible'),
        ],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_availability_display(self):
        """Return human-readable availability"""
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

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"
````

### 2. Fix [swappy/views.py](swappy/views.py):

````python
// filepath: swappy/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Student, Skill, SkillOffer, SkillRequest, Connection


# Home Page
def home(request):
    return render(request, 'home.html')


# Register
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        skills_teach = request.POST.get('skills_teach', '')
        skills
```


## License: unknown
https://github.com/Hwang-Kyu-Cheol/CigaretteProject_withGit/blob/6008f9e4f5059b1db22fdddb09f63ed9470f0cdd/Member_App/views.py

```
I've analyzed your EduSwap codebase and identified several frontend and backend issues. Here are the problems and fixes:

## Issues Found:

### **Backend Issues:**

1. **Missing `get_availability_display()` method** - Student model doesn't have this
2. **Skills parsing in registration** - Skills are accepted but never processed
3. **No validation in skill operations** - Missing error handling
4. **Race condition in connection creation** - Duplicate connections possible
5. **Missing imports in views** - Some views may have issues

### **Frontend Issues:**

1. **Profile page shows wrong availability format** - Using undefined method
2. **Skill offer/request forms don't load existing skills** - Should show dropdown
3. **Register form collects skills but doesn't use them** - Data loss
4. **Missing error handling in some templates**

## Fixes:

### 1. Fix [swappy/models.py](swappy/models.py):

````python
// filepath: swappy/models.py
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    availability = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening'),
            ('weekends', 'Weekends'),
            ('flexible', 'Flexible'),
        ],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_availability_display(self):
        """Return human-readable availability"""
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

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"
````

### 2. Fix [swappy/views.py](swappy/views.py):

````python
// filepath: swappy/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Student, Skill, SkillOffer, SkillRequest, Connection


# Home Page
def home(request):
    return render(request, 'home.html')


# Register
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        skills_teach = request.POST.get('skills_teach', '')
        skills
```


## License: unknown
https://github.com/Hwang-Kyu-Cheol/CigaretteProject_withGit/blob/6008f9e4f5059b1db22fdddb09f63ed9470f0cdd/Member_App/views.py

```
I've analyzed your EduSwap codebase and identified several frontend and backend issues. Here are the problems and fixes:

## Issues Found:

### **Backend Issues:**

1. **Missing `get_availability_display()` method** - Student model doesn't have this
2. **Skills parsing in registration** - Skills are accepted but never processed
3. **No validation in skill operations** - Missing error handling
4. **Race condition in connection creation** - Duplicate connections possible
5. **Missing imports in views** - Some views may have issues

### **Frontend Issues:**

1. **Profile page shows wrong availability format** - Using undefined method
2. **Skill offer/request forms don't load existing skills** - Should show dropdown
3. **Register form collects skills but doesn't use them** - Data loss
4. **Missing error handling in some templates**

## Fixes:

### 1. Fix [swappy/models.py](swappy/models.py):

````python
// filepath: swappy/models.py
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    availability = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening'),
            ('weekends', 'Weekends'),
            ('flexible', 'Flexible'),
        ],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_availability_display(self):
        """Return human-readable availability"""
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

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"
````

### 2. Fix [swappy/views.py](swappy/views.py):

````python
// filepath: swappy/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Student, Skill, SkillOffer, SkillRequest, Connection


# Home Page
def home(request):
    return render(request, 'home.html')


# Register
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        skills_teach = request.POST.get('skills_teach', '')
        skills
```

