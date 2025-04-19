// static/faults/js/engineer_dashboard.js

let lastCallIds = new Set();

function loadCalls() {
    fetch('/engineer/calls/json/')  // Adjust this URL to match your Django URL name
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const tbody = document.getElementById('calls-body');
            const alertSound = document.getElementById('alertSound');
            let currentCallIds = new Set();
            tbody.innerHTML = '';

            data.calls.forEach(call => {
                currentCallIds.add(call.id);

                // Play sound if this call is new
                if (!lastCallIds.has(call.id)) {
                    alertSound.play();
                }

                const row = document.createElement('tr');
                row.classList.add(call.status.toLowerCase().replace(' ', '-')); // e.g., "waiting", "in-progress"

                // Highlight row for specific statuses
                if (call.status === 'Waiting') {
                    row.style.backgroundColor = "#fff8dc"; // Light yellow
                } else if (call.status === 'In Progress') {
                    row.style.backgroundColor = "#e0ffe0"; // Light green
                }

                row.innerHTML = `
                    <td>${call.caller}</td>
                    <td>${call.location}</td>
                    <td>${call.status}</td>
                    <td>${call.created_at}</td>
                    <td>
                        ${call.status === 'Waiting' ? `
                        <form class="action-form" data-id="${call.id}" data-action="accept">
                            <button type="submit">✅ Accept</button>
                        </form>
                        <form class="action-form" data-id="${call.id}" data-action="reject">
                            <input type="text" name="reason" placeholder="Reason">
                            <button type="submit">❌ Reject</button>
                        </form>
                        ` : call.status}
                    </td>
                `;

                tbody.appendChild(row);
            });

            lastCallIds = currentCallIds;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

// Handle Accept/Reject via AJAX
function handleActionForms() {
    document.body.addEventListener('submit', function (e) {
        if (e.target.classList.contains('action-form')) {
            e.preventDefault();

            const form = e.target;
            const callId = form.dataset.id;
            const action = form.dataset.action;
            const reasonInput = form.querySelector('input[name="reason"]');
            const reason = reasonInput ? reasonInput.value : '';

            // Validate reason for rejection
            if (action === 'reject' && !reason) {
                alert('Please provide a reason for rejection.');
                return;
            }

            fetch('/engineer/action/', {  // Update to match your URL for action view
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({
                    call_id: callId,
                    action: action,
                    reason: reason
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    loadCalls();  // Refresh the list after the action is taken
                }
            })
            .catch(error => {
                console.error('Error handling action:', error);
            });
        }
    });
}

function getCSRFToken() {
    return document.cookie.match(/csrftoken=([^;]+)/)[1];
}

// Initial load + polling
window.onload = () => {
    loadCalls();
    handleActionForms();
    setInterval(loadCalls, 10000);  // Auto-refresh every 10 seconds
};
