from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone  
from .models import Student, Skill, SkillOffer, SkillRequest, Connection, Message, Notification

# --- CONTEXT PROCESSOR ---
def global_context(request):
    if request.user.is_authenticated:
        try:
            student = request.user.student
            pending_count = Connection.objects.filter(receiver=student, status='pending').count()
            return {'pending_count': pending_count}
        except:
            return {'pending_count': 0}
    return {'pending_count': 0}

# ------------------------------
# Home & Authentication
# ------------------------------
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        availability = request.POST.get('availability', '')
        user = User.objects.create_user(username=username, email=email, password=password1)
        student = Student.objects.create(user=user, availability=availability)
        auth_login(request, user)
        messages.success(request, f"Welcome to EduSwap, {username}!")
        return redirect('profile')
    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
            messages.error(request, "Incorrect username. Please check and try again.")
            return render(request, 'login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Incorrect password. Please try again.")
    return render(request, 'login.html')

def logout_view(request):
    auth_logout(request)
    return redirect('home')

# ------------------------------
# Dashboard & Profile
# ------------------------------
@login_required
def dashboard(request):
    student = request.user.student
    
    # --- AUTO-CANCEL FEATURE ---
    if student.is_premium and student.premium_expiry:
        if timezone.now() > student.premium_expiry:
            student.is_premium = False
            student.premium_since = None
            student.save()
            messages.error(request, "Your Premium subscription has expired.")
            return redirect('subscription')

    status_filter = request.GET.get('status', 'all')
    all_conns = Connection.objects.filter((Q(sender=student) | Q(receiver=student)), is_deleted=False).order_by('-id')
    pending_count = all_conns.filter(status='pending').count()
    active_count = all_conns.filter(status='accepted').count()
    completed_count = all_conns.filter(status='completed').count()
    cancelled_count = all_conns.filter(status__in=['rejected', 'cancelled']).count()
    
    # Renewal Alert for Dashboard UI
    expiring_soon = False
    if student.is_premium and student.days_left <= 2:
        expiring_soon = True

    if status_filter == 'pending': connections = all_conns.filter(status='pending')
    elif status_filter == 'accepted': connections = all_conns.filter(status='accepted')
    elif status_filter == 'completed': connections = all_conns.filter(status='completed')
    elif status_filter == 'cancelled': connections = all_conns.filter(status__in=['rejected', 'cancelled'])
    else: connections = all_conns

    return render(request, 'dashboard.html', {
        'student': student, 'connections': connections, 'all_count': all_conns.count(),
        'active_count': active_count, 'pending_count': pending_count,
        'completed_count': completed_count, 'cancelled_count': cancelled_count,
        'current_status': status_filter,
        'expiring_soon': expiring_soon,
    })

@login_required
def profile(request):
    student, _ = Student.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'student': student})

@login_required
def profile_management(request):
    student, _ = Student.objects.get_or_create(user=request.user)
    if request.method == "POST":
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'profile_management.html', {'student': student})
        request.user.username = new_username
        request.user.email = new_email
        student.bio = request.POST.get('bio')
        student.availability = request.POST.get('availability')
        request.user.save()
        student.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    return render(request, 'profile_management.html', {'student': student})

# ------------------------------
# Skills Management
# ------------------------------
@login_required
def skill_offer(request):
    student = request.user.student
    if request.method == "POST":
        skill_name = request.POST.get('skill_name').strip()
        level = request.POST.get('proficiency_level')
        skill_obj, _ = Skill.objects.get_or_create(name=skill_name)
        SkillOffer.objects.get_or_create(student=student, skill=skill_obj, proficiency_level=level)
        messages.success(request, f"You are now offering {skill_name}!")
        return redirect('profile')
    return render(request, 'skill_offer.html')

@login_required
def skill_request(request):
    student = request.user.student
    if request.method == "POST":
        skill_name = request.POST.get('skill_name').strip()
        level = request.POST.get('desired_proficiency')
        skill_obj, _ = Skill.objects.get_or_create(name=skill_name)
        SkillRequest.objects.get_or_create(student=student, skill=skill_obj, desired_proficiency=level)
        messages.success(request, f"Requested {skill_name} added to your profile!")
        return redirect('profile')
    return render(request, 'skill_request.html')

@login_required
def delete_skill_offer(request, skill_id):
    skill_offer = get_object_or_404(SkillOffer, id=skill_id, student=request.user.student)
    skill_offer.delete()
    messages.info(request, "Skill offer removed.")
    return redirect('profile')

@login_required
def delete_skill_request(request, skill_id):
    skill_req = get_object_or_404(SkillRequest, id=skill_id, student=request.user.student)
    skill_req.delete()
    messages.info(request, "Skill request removed.")
    return redirect('profile')

# ------------------------------
# Discovery & Networking
# ------------------------------
@login_required
def browse(request):
    query = request.GET.get('q', '').strip()
    level_filter = request.GET.get('level', '').strip()
    me = request.user.student
    all_students = Student.objects.exclude(user=request.user)
    
    my_offers = set(me.offered_skills.values_list('skill_id', flat=True))
    my_requests = set(me.requested_skills.values_list('skill_id', flat=True))

    matched_students = []
    if query or level_filter:
        results = all_students
        if query: results = results.filter(offered_skills__skill__name__icontains=query)
        if level_filter: results = results.filter(offered_skills__proficiency_level=level_filter)
        matched_students = results.distinct()
        recommendations = all_students.exclude(id__in=matched_students.values_list('id', flat=True))
    else:
        recommendations = all_students

    def check_mutual(target_student):
        t_off = set(target_student.offered_skills.values_list('skill_id', flat=True))
        t_req = set(target_student.requested_skills.values_list('skill_id', flat=True))
        return bool(my_requests & t_off) and bool(my_offers & t_req)

    for s in matched_students: s.is_mutual = check_mutual(s)
    for s in recommendations: s.is_mutual = check_mutual(s)

    sent_requests = Connection.objects.filter(sender=me, status='pending').values_list('receiver_id', flat=True)
    return render(request, 'browse.html', {
        'students': matched_students,
        'recommendations': recommendations,
        'sent_requests': sent_requests,
        'query': query,
        'level_filter': level_filter
    })

@login_required
def search_students(request):
    query = request.GET.get('q', '')
    students = Student.objects.exclude(user=request.user).filter(
        Q(user__username__icontains=query) | Q(offered_skills__skill__name__icontains=query)
    ).distinct()
    return render(request, 'search_students.html', {'students': students, 'query': query})

@login_required
def skill_matching(request):
    student = request.user.student
    matches = []
    my_requests = SkillRequest.objects.filter(student=student)
    for req in my_requests:
        tutors = SkillOffer.objects.filter(skill=req.skill).exclude(student=student)
        for tutor in tutors:
            matches.append({'student': tutor.student, 'skill': tutor.skill, 'proficiency': tutor.proficiency_level})
    return render(request, 'skill_matching.html', {'matches': matches})

@login_required
def student_profile(request, student_id):
    me = request.user.student
    target_student = get_object_or_404(Student, id=student_id)
    
    my_offers = set(me.offered_skills.values_list('skill_id', flat=True))
    my_requests = set(me.requested_skills.values_list('skill_id', flat=True))
    t_off = set(target_student.offered_skills.values_list('skill_id', flat=True))
    t_req = set(target_student.requested_skills.values_list('skill_id', flat=True))
    is_mutual = bool(my_requests & t_off) and bool(my_offers & t_req)

    pending_connection = Connection.objects.filter(sender=me, receiver=target_student, status='pending').first()
    
    return render(request, 'student_profile.html', {
        'student': target_student,
        'offered_skills': target_student.offered_skills.all(),
        'requested_skills': target_student.requested_skills.all(),
        'pending_connection': pending_connection,
        'is_mutual': is_mutual,
    })

# ------------------------------
# Connections & Interactions
# ------------------------------
@login_required
def send_connection(request, student_id):
    sender = request.user.student
    receiver = get_object_or_404(Student, id=student_id)
    has_advanced_skills = receiver.offered_skills.filter(proficiency_level='Advanced').exists()
    if has_advanced_skills and not sender.is_premium:
        messages.warning(request, "Upgrade to Premium to connect with Advanced skill mentors!")
        return redirect('subscription')
    Connection.objects.get_or_create(sender=sender, receiver=receiver)
    messages.success(request, "Connection request sent!")
    return redirect(request.META.get('HTTP_REFERER', 'browse'))

@login_required
def cancel_request(request, connection_id):
    connection = get_object_or_404(Connection, id=connection_id, sender=request.user.student)
    connection.status = 'cancelled'
    connection.save()
    Notification.objects.create(
        student=connection.receiver,
        from_user=request.user.student,
        type='request_cancelled',
        message=f"{request.user.username} cancelled their request."
    )
    messages.info(request, "Request cancelled.")
    return redirect(request.META.get('HTTP_REFERER', 'connections'))

@login_required
def connections(request):
    student = request.user.student
    received = student.received_connections.filter(is_deleted=False).order_by('-id')
    sent = student.sent_connections.filter(is_deleted=False).order_by('-id')
    notifications = Notification.objects.filter(student=student).order_by('-created_at')

    # Renewal Alert Generator
    if student.is_premium and student.days_left <= 2:
        note_msg = f"Alert: Your premium subscription expires in {student.days_left} days!"
        if not Notification.objects.filter(student=student, message=note_msg).exists():
            Notification.objects.create(student=student, type='renewal_alert', message=note_msg)

    return render(request, 'connections.html', {'received': received, 'sent': sent, 'notifications': notifications, 'student': student})

@login_required
def update_connection(request, connection_id, action):
    student = request.user.student
    connection = get_object_or_404(Connection, id=connection_id)
    if action == 'accept' and connection.receiver == student:
        connection.status = 'accepted'
        connection.save()
        Notification.objects.create(student=connection.sender, from_user=student, type='request_accepted', message=f"{request.user.username} accepted your connection!")
        messages.success(request, "Connection accepted!")
    elif action == 'reject' and connection.receiver == student:
        connection.status = 'rejected'
        connection.save()
        Notification.objects.create(student=connection.sender, from_user=student, type='request_rejected', message=f"{request.user.username} declined your request.")
        messages.info(request, "Request declined.")
    elif action == 'complete':
        if connection.sender == student or connection.receiver == student:
            connection.status = 'completed'
            connection.save()
            messages.success(request, "Skill swap marked as completed!")
    return redirect('connections')

@login_required
def clear_notifications(request):
    Notification.objects.filter(student=request.user.student).delete()
    messages.success(request, "Notifications cleared.")
    return redirect('connections')

# ------------------------------
# Chat System
# ------------------------------
@login_required
def chat(request, student_id=None):
    me = request.user.student
    connections = Connection.objects.filter((Q(sender=me) | Q(receiver=me)), status__in=['accepted', 'completed'], is_deleted=False)
    contact_ids = [conn.receiver.id if conn.sender == me else conn.sender.id for conn in connections]
    contacts = Student.objects.filter(id__in=contact_ids)
    active_chat, messages_list = None, []
    if student_id:
        active_chat = get_object_or_404(Student, id=student_id)
        messages_list = Message.objects.filter((Q(sender=me) & Q(receiver=active_chat)) | (Q(sender=active_chat) & Q(receiver=me))).order_by('timestamp')
        if request.method == "POST":
            content = request.POST.get('message')
            if content:
                Message.objects.create(sender=me, receiver=active_chat, content=content)
                Notification.objects.create(student=active_chat, from_user=me, type='new_message', message=f"New message from {request.user.username}")
                return redirect('chat', student_id=student_id)
    return render(request, 'chat.html', {'contacts': contacts, 'messages': messages_list, 'active_chat': active_chat})

@login_required
def clear_chat(request, student_id):
    me = request.user.student
    other_person = get_object_or_404(Student, id=student_id)
    Message.objects.filter((Q(sender=me) & Q(receiver=other_person)) | (Q(sender=other_person) & Q(receiver=me))).delete()
    return redirect('chat', student_id=student_id)

# ------------------------------
# Subscription & Payments
# ------------------------------
@login_required
def subscription(request):
    return render(request, 'subscription.html', {'student': request.user.student})

@login_required
def payment_page(request):
    return render(request, 'payment.html', {'student': request.user.student})

@login_required
def upgrade_to_premium(request):
    student = request.user.student
    student.is_premium = True
    student.premium_since = timezone.now()
    student.save()
    
    # Create Notification for Payment Success
    Notification.objects.create(
        student=student,
        type='payment_success',
        message="Payment Successful! You are now a Premium Pro member."
    )
    
    messages.success(request, "Welcome to Premium!")
    return redirect('dashboard')

@login_required
def cancel_subscription(request):
    student = request.user.student
    student.is_premium = False
    student.premium_since = None
    student.save()
    messages.info(request, "Premium cancelled.")
    return redirect('profile')