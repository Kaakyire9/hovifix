from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from .models import FaultCall
from .forms import AssignEngineerForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

User = get_user_model()


@login_required
def call_engineer_view(request):
    if request.method == 'POST':
        user = request.user
        location = user.profile.location if hasattr(user, 'profile') else "Unknown"

        # Just create the call — signal will handle assignment
        FaultCall.objects.create(
            caller=user,
            location=location,
            status='Waiting'
        )

        return redirect('call_success')

    return render(request, 'faults/call_engineer.html')




@login_required
def call_success_view(request):
    return render(request, 'faults/call_success.html')


@login_required
def flm_dashboard_view(request):
    # List all calls (latest first)
    calls = FaultCall.objects.order_by('-created_at')

    # Filter engineers: staff in Engineering department
    engineers = CustomUser.objects.filter(role='Staff', department='Engineering')

    # Initialize the form
    form = AssignEngineerForm()

    if request.method == 'POST':
        call_id = request.POST.get('call_id')
        engineer_id = request.POST.get('engineer_id')

        if call_id and engineer_id:
            call = get_object_or_404(FaultCall, id=call_id)
            engineer = get_object_or_404(CustomUser, id=engineer_id)
            call.assigned_engineer = engineer
            call.save()
            return redirect('flm_dashboard')

    return render(request, 'faults/flm_dashboard.html', {
        'calls': calls,
        'engineers': engineers,
        'form': form  # Pass the form to the template
    })

@login_required
def engineer_dashboard_view(request):
    # Only show calls assigned to the logged-in engineer
    calls = FaultCall.objects.filter(assigned_engineer=request.user).order_by('-created_at')

    if request.method == 'POST':
        call_id = request.POST.get('call_id')
        action = request.POST.get('action')
        reason = request.POST.get('reason')

        if call_id and action:
            call = FaultCall.objects.get(id=call_id)

            if action == 'accept':
                call.status = 'In Progress'
                call.save()
            elif action == 'reject':
                call.status = 'Rejected'
                call.rejection_reason = reason or "No reason given"
                call.assigned_engineer = None  # Optional: Unassign so FLM can reassign
                call.save()

            return redirect('engineer_dashboard')

    return render(request, 'faults/engineer_dashboard.html', {
        'calls': calls,
    })

def get_fault_calls(request):
    # Fetch the most recent calls
    calls = FaultCall.objects.order_by('-created_at')[:10]  # Limit to 10 most recent calls

    calls_data = [
        {
            'id': call.id,
            'caller': str(call.caller),
            'location': call.location,
            'status': call.status,
            'assigned_engineer': str(call.assigned_engineer) if call.assigned_engineer else 'Not Assigned',
        }
        for call in calls
    ]

    return JsonResponse({'calls': calls_data})

@login_required
def engineer_calls_json(request):
    calls = FaultCall.objects.filter(assigned_engineer=request.user).order_by('-created_at')
    data = []
    for call in calls:
        data.append({
            'id': call.id,
            'caller': call.caller.get_full_name(),
            'location': call.location,
            'status': call.status,
            'created_at': call.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return JsonResponse({'calls': data})

@csrf_exempt  # CSRF token still handled via header
@require_POST
@login_required
def engineer_action_api(request):
    try:
        data = json.loads(request.body)
        call_id = data.get('call_id')
        action = data.get('action')
        reason = data.get('reason', '')

        call = FaultCall.objects.get(id=call_id, assigned_engineer=request.user)

        if action == 'accept':
            call.status = 'In Progress'
        elif action == 'reject':
            call.status = 'Rejected'
            call.rejection_reason = reason
            call.assigned_engineer = None  # Optional: unassign for FLM to reassign
        call.save()
        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    

@login_required
def update_call_status(request):
    call_id = request.POST.get('call_id')
    action = request.POST.get('action')
    reason = request.POST.get('reason', '')

    try:
        call = FaultCall.objects.get(id=call_id, assigned_engineer=request.user)

        if action == 'accept':
            call.status = 'In Progress'
        elif action == 'reject':
            call.status = 'Rejected'
            call.rejection_reason = reason
            call.assigned_engineer = None  # Optional: so FLM can reassign

        call.save()
        return JsonResponse({"success": True})
    except FaultCall.DoesNotExist:
        return JsonResponse({"success": False, "error": "Call not found"})
    
def poll_calls(request):
    calls = FaultCall.objects.filter(assigned_engineer__isnull=True,status='Waiting'
).order_by('-created_at')
    engineers = CustomUser.objects.filter(role='Engineer')

    calls_data = [
        {
            'id': call.id,
            'caller': call.caller,
            'location': call.location,
            'status': call.status,
            'assigned_engineer': call.assigned_engineer.get_full_name() if call.assigned_engineer else None,
        }
        for call in calls
    ]

    engineers_data = [
        {'id': eng.id, 'name': eng.get_full_name()}
        for eng in engineers
    ]

    return JsonResponse({'calls': calls_data, 'engineers': engineers_data})

