from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100, unique=True)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    location = models.TextField()
    age = models.IntegerField()
    prefered_language = models.CharField(max_length=100, default="English")
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "phone_number",
        "location",
        "age",
        "id",
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Administrator(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    first_mame = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    rating = models.FloatField()
    phone_numbers = models.JSONField(default=list)
    join_date = models.DateField()
    agent_type = models.CharField(max_length=100)
    first_prefered_language = models.CharField(max_length=100)
    second_prefered_language = models.CharField(max_length=100)
    third_prefered_language = models.CharField(max_length=100)
    admin = models.BooleanField(default=False)
    on_duty = models.BooleanField()
    password = models.CharField(max_length=100)
    email = models.EmailField()
    groups = models.ManyToManyField(
        Group,
        related_name="satim_admin_groups",  # Unique related name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="satim_admin_permissions",  # Unique related name
        blank=True,
    )
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "phone_number",
        "age",
        "id",
        "rating",
        "join_date",
        "agent_type",
        "first_prefered_language",
        "second_prefered_language",
        "third_prefered_language",
        "on_duty",
        "password",
        "email",
    ]

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class call(models.Model):
    id = models.BigAutoField(primary_key=True)

    agent = models.ForeignKey(Administrator, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field="first_name")
    call_date = models.DateField()
    call_duration = models.FloatField()
    call_type = models.CharField(max_length=100)
    call_rating = models.FloatField()
    call_feedback = models.TextField()
    REQUIRED_FIELDS = [
        "user",
        "agent",
        "call_date",
        "call_duration",
        "call_type",
        "call_rating",
        "call_feedback",
        "id",
    ]

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.agent.first_name} {self.agent.last_name}"


class order(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    call = models.ForeignKey(call, on_delete=models.CASCADE)
    agent = models.ForeignKey(Administrator, on_delete=models.CASCADE)
    description = models.TextField()
    REQUIRED_FIELDS = [
        "user",
        "call",
        "order_date",
        "order_status",
        "order_feedback",
        "id",
        "agent",
    ]

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.call.call_date} {self.order_date}"
