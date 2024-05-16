from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.urls import reverse



def send_email(user,maintenance_id, message, recipient_list):
    maintenance_url = reverse('maintenance') + f'?open_maintenance={maintenance_id}'
    
    # Render the HTML content from the template
    html_message = render_to_string("email/notification.html", context={
        "user": user,
        "message": message,
        "button_url": maintenance_url,  # Replace with your button URL
        "button_text": "View issue"  # Replace with your button text
    })


    # Create a plain text version of the HTML content
    plain_text_message = strip_tags(html_message)

    send_mail(
        "New Notification from ApexCare",
        plain_text_message,  # Use the plain text version for the message
        "notifications@z-techsoftware.com",
        recipient_list,
        html_message=html_message  # Attach the HTML content
    )