# faults/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FaultCall
from accounts.models import CustomUser

@receiver(post_save, sender=FaultCall)
def auto_assign_engineer(sender, instance, created, **kwargs):
    if not created or instance.assigned_engineer:
        return  # Only run on first creation and if no one is assigned

    caller = instance.caller
    user_shift = getattr(caller, 'shift', None)

    if user_shift:
        # Look for available engineers on the same shift
        available_engineers = CustomUser.objects.filter(
            role='Staff',
            department='Engineering',
            shift=user_shift
        ).exclude(
            faultcall__status='In Progress'
        ).distinct()

        if available_engineers.exists():
            engineer = available_engineers.first()
            instance.assigned_engineer = engineer
            instance.status = 'In Progress'
            instance.save()
            print(f"Auto-assigned engineer {engineer.get_full_name()} to call {instance.id}")
        else:
            print(f"No available engineers found on shift: {user_shift}")
    else:
        print("Caller shift not found")
