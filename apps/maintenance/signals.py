from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.maintenance.models import MaintenanceAssigning, MaintenanceRequest, Message, Notification
from apps.maintenance.utils import send_email


@receiver(post_save, sender=MaintenanceAssigning)
def maintenance_assigned(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            message=f'Maintenance request <b>{instance.maintenance.request_title}</b> assigned to you. Please reload the page.',
            recipient=instance.user,
            event="new_assignment"
        )
        send_email(instance.user,instance.maintenance.id, f'Maintenance request <b>{instance.maintenance.request_title}</b> assigned to you. Please check your portal.', [instance.user.email])

    notification = Notification.objects.create(
        message=f'',
        recipient=instance.user,
        event="change"
    )

@receiver(post_save, sender=MaintenanceRequest)
def maintenance_status_changed(sender, instance, created, **kwargs):
    if not created:  # this means the instance is updated
        # Create notification
        notification = Notification.objects.create(
            message=f'Status of maintenance request <b>{instance.request_title}</b> updated. Please reload the page.',
            recipient=instance.user,
            event="new_assignment"
        )
        send_email(instance.user,instance.id, f'Maintenance request <b>{instance.request_title}</b> status changed to <b>{instance.status}</b> . Please check your portal.', [instance.user.email])
    
    notification = Notification.objects.create(
        message=f'',
        recipient=instance.user,
        event="change"
    )
    

@receiver(post_save, sender=Message)
def new_message(sender, instance, created, **kwargs):
    if created:
        assigned_employees = instance.maintenance.maintenance_assigning.all()
        for assigned_employee in assigned_employees:
            
            notification = Notification.objects.create(
                message=f'You have new message in <b>{instance.maintenance.request_title}</b>.',
                recipient=assigned_employee.user,
                event="new_message"
            )
            send_email(assigned_employee.user,instance.maintenance.id, f'New message received in <b>{instance.maintenance.request_title}</b> which is assigned to you. Please check your portal.', [assigned_employee.user.email])
    
    notification = Notification.objects.create(
        message=f'',
        recipient=instance.user,
        event="change"
    )