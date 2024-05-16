from django.db import models

# Create your models here.


class Company(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=50, null=True, blank=True)
	phone = models.CharField(max_length=50, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	logo = models.ImageField(upload_to='images', blank=True, null=True)
	active = models.BooleanField(default=True)
	owner = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name="company_owner")

	
	class Meta:
		verbose_name_plural = "Companies"

	def __str__(self):
		return self.name

class Building(models.Model):
	name = models.CharField(max_length=250)
	company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="building_company")
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.name
	

class Unit(models.Model):
	name = models.CharField(max_length=250)
	building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="unit_building")
	temporary_assigned_resource = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name="temporary_assigned")

	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name
	
class Room(models.Model):
	room_no = models.CharField(max_length=250)
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="room_unit")
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.room_no

class MaintenanceItem(models.Model):
	name = models.CharField(max_length=250)
	company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="maintenance_item_company", null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Issue(models.Model):
	title = models.CharField(max_length=250)
	maintenance_item = models.ForeignKey(MaintenanceItem, null=True, blank=True, on_delete=models.CASCADE, related_name='maintenance_issue')
	def __str__(self):
		return self.title
	
class IssueDetails(models.Model):
	details = models.TextField(max_length=250)
	
	def __str__(self):
		return self.details[:15] + "..."
	
	
class Image(models.Model):
	image = models.ImageField(upload_to='images', blank=True, null=True)
	alt = models.CharField(max_length=50, blank=True, null=True)
	company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="image_company", null=True, blank=True)

	def __str__(self) -> str:
		return str(self.alt)

class KanbanColumn(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="kanban_column_company")
	name = models.CharField(max_length=50)
	status_code = models.CharField(max_length=50)
	status_description = models.TextField(default="No Description Provided")
	order = models.IntegerField()
	color_class = models.CharField(max_length=50, default="danger", null=True, blank=True) 
	icon = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="kanban_column_icon", null=True, blank=True)
	
	def __str__(self):
		return self.name
	

class MaintenanceRequest(models.Model):
	enquiryDate = models.DateTimeField(auto_now_add=True)
	end_date = models.DateTimeField(default=None, null=True, blank=True)
	request_type = models.CharField(max_length=50, default=None, null=True, blank=True)
	request_title = models.CharField(null=True, blank=True, max_length=150)
	cancel_reason = models.TextField(null=True, blank=True, default=None)
	user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='maintenance_user', null=True)
	building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="maintenance_building")
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="maintenance_unit")
	room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="maintenance_room")
	maintenance_item = models.ForeignKey(MaintenanceItem, on_delete=models.CASCADE, null=True, blank=True, related_name="maintenance_item")
	issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="issue", null=True, blank=True)
	issue_details = models.CharField(max_length=500, null=True, blank=True)
	status = models.ForeignKey(KanbanColumn, on_delete=models.CASCADE, related_name="maintenance_request_item", null=True, blank=True)
	company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='maintenance_company')
	is_deleted = models.BooleanField(default=False)
	problemImage = models.ManyToManyField(Image, blank=True)

	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.enquiryDate)

	def move_to_next_status(self):
		assign_column = KanbanColumn.objects.filter(order=self.status.order+1).first()
		if assign_column:
			self.status = assign_column
			self.save()
		previous_column = KanbanColumn.objects.filter(order=assign_column.order-1).first()
		return previous_column, KanbanColumn.objects.filter(order=self.status.order+1).first()
	
	def move_to_previous_status(self):
		next_column = self.status
		assign_column = KanbanColumn.objects.filter(order=self.status.order-1).first()
		if assign_column:
			self.status = assign_column
			self.save()
		return KanbanColumn.objects.filter(order=self.status.order-1).first(), next_column
	
	def get_assigned_employess(self):
		assigned_req_users = MaintenanceAssigning.objects.filter(maintenance__id=self.id)
		return assigned_req_users


class MaintenanceDetail(models.Model):
	maintenance = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE, related_name="maintenance_detail")
	problemTitle = models.CharField(max_length = 50)
	problemDescription = models.TextField(blank=True)

	def _str_(self):
		return self.problemTitle

class Message(models.Model):
	message = models.TextField()
	attachment = models.FileField(upload_to='maintenance-attachments', blank=True, null=True)
	maintenance = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE, related_name="maintenance_messages")
	user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return self.user.first_name + " " + self.user.last_name + " " + self.message[:10] + "..."


class MaintenanceAssigning(models.Model):
	maintenance = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE, related_name="maintenance_assigning")
	user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    recipient = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    message = models.TextField()
    is_seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.message