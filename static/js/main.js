/**
 * Build Bright University (BBU) - Main Static JavaScript
 * Provides UI interactivity, auto-dismiss alerts, and tooltips.
 */

document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss alert messages after 5 seconds
    const alerts = document.querySelectorAll('.alert.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.6s ease';
            alert.style.opacity = '0';
            setTimeout(function () {
                alert.remove();
            }, 600);
        }, 5000);
    });

    // Console confirmation of static JS loaded
    console.log('✅ BBU Student Management System - Static assets loaded successfully.');
});
