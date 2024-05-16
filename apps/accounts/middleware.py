import json
from django.utils import timezone

from apps.accounts.models import Action

class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            # Update the last_activity field for the authenticated user
            request.user.last_activity = timezone.now()
            request.user.save()

        response = self.get_response(request)
        return response

class LogUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Capture the start time of the request
        start_time = timezone.now()

        response = self.get_response(request)

        # Calculate the request duration
        end_time = timezone.now()
        duration = end_time - start_time
        try:
            view_name = request.resolver_match.view_name
        except:
            view_name = None

        # Log the action in the database
        action = Action(
            user=request.user if request.user.is_authenticated else None,
            action_type=view_name if view_name else "Unknown",
            timestamp=start_time,
            url=request.get_full_path(),
            ip=self.get_client_ip(request),
            response_data=self.get_response_data(response),  # Capture response data here
            request_type=request.method,  # Capture request type (GET, POST, etc.)
            context_data=self.get_context_data(response),  # Capture context data here
            form_data=self.get_form_data(request),  # Capture form data here
            duration=str(duration.total_seconds())+"sec"
        )
        action.save()

        return response

    # Helper method to get client's IP address
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    # Helper method to get response data
    def get_response_data(self, response):
        try:
            return response.content.decode('utf-8')
        except Exception as e:
            return str(e)

    # Helper method to get context data
    def get_context_data(self, response):
        # Customize this method to capture context data based on your application's needs
        # For example, you can serialize the request context dictionary to JSON
        context_data = {}

        if hasattr(response, 'context_data'):
            # If your views store context data explicitly, you can capture it here
            context_data = response.context_data

        # Serialize the context_data dictionary to JSON
        return json.dumps(context_data, indent=4, default=str)

    # Helper method to get form data
    def get_form_data(self, request):
        # Customize this method to capture form data based on your application's needs
        # For example, you can serialize the request POST data to JSON
        data = {
            "post": request.POST,
            "get": request.GET,
            "data":request.data if "data" in request else None
        }
        return data