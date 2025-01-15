from django.db import models


class Advertisement(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        choices=[
            ("sold", "sold"),
            ("pending", "pending"),
            ("canceled", "canceled"),
            ("new", "new"),
            ("ongoing", "ongoing"),
        ],
        max_length=10,
        default="new",
    )
    image = models.ImageField(upload_to="advertisements", null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(
        "accounts.user", on_delete=models.CASCADE, related_name="advertisements"
    )
