from django.urls import path
from . import views

urlpatterns = [
    # --- Home Page ---
    path('', views.home, name='home'),

    # --- Authentication (Login/Register) ---
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # --- User Dashboard & Profile ---
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile-management/', views.profile_management, name='profile_management'),

    # --- Premium Subscription & Payments ---
    path('subscription/', views.subscription, name='subscription'),  
    path('payment/', views.payment_page, name='payment_page'),
    path('upgrade-process/', views.upgrade_to_premium, name='upgrade_to_premium'),
    path('cancel-subscription/', views.cancel_subscription, name='cancel_subscription'), 
    
    # --- Skills Management (Add & Delete) ---
    path('skill-offer/', views.skill_offer, name='skill_offer'),
    path('skill-request/', views.skill_request, name='skill_request'),
    path('delete-offer/<int:skill_id>/', views.delete_skill_offer, name='delete_skill_offer'),
    path('delete-request/<int:skill_id>/', views.delete_skill_request, name='delete_skill_request'),

    # --- Discovery & Networking ---
    path('browse/', views.browse, name='browse'),
    path('search/', views.search_students, name='search_students'),
    path('skill-matching/', views.skill_matching, name='skill_matching'),
    path('student/<int:student_id>/', views.student_profile, name='student_profile'),

    # --- Connections & Interactions ---
    path('connections/', views.connections, name='connections'),
    path('send-connection/<int:student_id>/', views.send_connection, name='send_connection'),
    path('cancel-request/<int:connection_id>/', views.cancel_request, name='cancel_request'),
    path('update-connection/<int:connection_id>/<str:action>/', views.update_connection, name='update_connection'),
    path('clear-notifications/', views.clear_notifications, name='clear_notifications'),

    # --- Chat System ---
    path('chat/', views.chat, name='chat_lobby'), 
    path('chat/<int:student_id>/', views.chat, name='chat'),
    path('clear-chat/<int:student_id>/', views.clear_chat, name='clear_chat'),
]