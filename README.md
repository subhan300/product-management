# Project: core

## Overview

This Django project, named "core," consists of two apps: "accounts" and "maintenance." The "accounts" app is responsible for user management and authentication, while the "maintenance" app is used for managing maintenance requests, Kanban columns, messages, and more.


## Installation and Usage

Follow these steps to set up and run the project:

### Prerequisites

- Python 3.x installed on your system
- `pip` package manager installed

### 1. Clone the Repository

Clone this Git repository to your local machine using the following command:

```bash
git clone https://github.com/Tahir-Siddique/maintenance-system.git
```
### 2. Create a Virtual Environment
It's recommended to create a virtual environment for the project to isolate dependencies. Navigate to the project directory and create a virtual environment:

```bash
cd core
python -m venv venv
```
### 3. Activate the Virtual Environment
Activate the virtual environment:

- On Windows:
```bash
venv\Scripts\activate
```
- On macOS and Linux::
```bash
source venv/bin/activate
```
### 4. Install Dependencies
Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```
### 5. Apply Migrations
Apply database migrations to create the necessary database tables:

```bash
python manage.py migrate
```
### 6. Load Default Data
Load default data for kanban view:
```bash
python manage.py loaddata default_fixture.json
```
### 7. Create a Superuser
Create a superuser account to access the Django admin panel:
```bash
python manage.py createsuperuser
```
Follow the prompts to set an email, and password for the superuser account.

### 8. Run the Development Server
Start the Django development server:

```bash
python manage.py runserver
```
The server will start at http://127.0.0.1:8000/. You can access the admin panel at http://127.0.0.1:8000/admin/ and log in with the superuser account created earlier.

### 9. Access the Project
Access the project's dashboard and maintenance management features:

Dashboard: http://127.0.0.1:8000/
Maintenance: http://127.0.0.1:8000/maintenance/

## Apps

### 1. accounts

#### Models

- `CustomUser`: This model extends the Django `AbstractUser` and `PermissionsMixin` classes to provide custom user management. It includes fields such as email, role, profile_image, bio, phone, etc.

- `Action`: This model is used for logging user activities and includes fields like user, action_type, timestamp, url, ip, response_data, request_type, context_data, form_data, and duration.

#### Serializers

- `UserRegistrationSerializer`: A serializer for user registration, including fields for email, password, and role.

- `ShortUserSerializer`: A serializer for a shorter representation of the user, including first name, last name, role, and profile image.

- `UserSerializer`: A serializer for the complete user model, including all fields.

- `UserLoginSerializer`: A serializer for user login, including email and password.

- `ForgotPasswordSerializer`: A serializer for handling forgotten passwords, including an email field.

#### Views

- `UserLoginView`: A view for user login, handling GET and POST requests for authentication.

- `ForgotPasswordView`: A view for handling forgotten passwords, including sending reset links.

- `ProfileView`: A view for user profiles, handling GET and POST requests for updating profile information and changing passwords.

- `LogoutView`: A view for user logout, ensuring users are logged out when they access this view.

#### Middlewares

- `UpdateLastActivityMiddleware`: This middleware updates the `last_activity` field for authenticated users.

- `LogUserActivityMiddleware`: This middleware logs user actions, including view name, timestamp, URL, IP, response data, request type, context data, form data, and duration.

### 2. maintenance

#### Models

- `KanbanColumn`: This model represents Kanban columns used for organizing maintenance tasks. It includes fields like name, status_code, order, and color_class.

- `Image`: This model is used for storing images and is related to the "profile_image" field in the `CustomUser` model from the "accounts" app.

- `Maintenance`: This model represents maintenance requests, including fields like title, enquiryDate, user, problemImages, status, and active.

- `MaintenanceDetail`: This model contains details of maintenance issues, including problemTitle and problemDescription.

- `Message`: This model is used for storing messages related to maintenance requests.

#### Serializers

- `CreateMessageSerializer`: A serializer for creating messages associated with maintenance requests.

- `FullKanbanColumnSerializer`: A serializer for Kanban columns, used for organizing maintenance tasks.

- `MaintenanceSerializer`: A serializer for the `Maintenance` model, including related fields.

- `MessageSerializer`: A serializer for messages related to maintenance requests.

- `ShortKanbanSerializer`: A serializer for a shorter representation of Kanban columns.

#### Views

- `DashboardView`: A view for the project's dashboard, displaying maintenance tasks organized by Kanban columns.

- `MaintenanceView`: A view for managing maintenance requests, including creating and updating them.

- `DeleteMaintenanceView`: A view for deleting maintenance requests.

- `MaintenanceDetailView`: A view for retrieving details of a specific maintenance request.

- `KanbanView`: An API view for retrieving Kanban columns.

- `CreateMessageView`: An API view for creating messages related to maintenance requests.

- `MessageView`: An API view for retrieving messages related to a specific maintenance request.

- `AssignEmployeeView`: An API view for assigning employees to maintenance tasks.

- `MoveNextView`: An API view for moving maintenance tasks to the next Kanban column.

- `MovePreviousView`: An API view for moving maintenance tasks to the previous Kanban column.

- `MoveToView`: An API view for moving maintenance tasks to a specific Kanban column.

## Usage

You can use this project as a foundation for building a Django web application with user authentication, activity logging, and maintenance request management features. Customize and extend the apps and models as needed for your specific project requirements.

Please ensure you have Django and other required dependencies installed to run the project successfully.

## URLs

### Accounts App URLs

- Login: `/login/`
- Forgot Password: `/forgot-password/`
- Profile: `/profile/`
- Change Profile: `/profile/<str:key>/`
- Logout: `/logout/`

### Maintenance App URLs

- Maintenance Detail: `/api/maintenance_detail/<int:pk>/`
- Kanban Columns: `/api/kanban/`
- Create Message: `/api/messages/`
- Get Messages: `/api/messages/<int:pk>`
- Assign Employee: `/api/assignuser/`
- Move to Next Column: `/api/movenext/`
- Move to Previous Column: `/api/moveprevious/`
- Move to Specific Column: `/api/moveto/`

