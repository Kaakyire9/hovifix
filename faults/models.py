from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class FaultCall(models.Model):
    STATUS_CHOICES = [
        ('Waiting', 'Waiting'),
        ('Accepted', 'Accepted'),
        ('In Progress', 'In Progress'),
        ('Fixed', 'Fixed'),
        ('Rejected', 'Rejected'),
    ]

    caller = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Waiting')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.caller.username} - {self.status} at {self.location}"
    
    assigned_engineer = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='assigned_calls'
    
)

rejection_reason = models.TextField(blank=True, null=True)

