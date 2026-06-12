from django.db import models
from django.contrib.auth.models import User
from PIL import Image



# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)




from django.db import models
from django.contrib.auth.models import User

class Case(models.Model):

    CASE_TYPE = (
        ('Missing', 'Missing'),
        ('Criminal', 'Criminal'),
    )

    STATUS = (
        ('Pending', 'Pending'),
        ('Found', 'Found'),
        ('Arrested', 'Found'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    case_type = models.CharField(max_length=20, choices=CASE_TYPE)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')

    image = models.ImageField(upload_to='uploads/')
    detected_image = models.ImageField(upload_to='detected/', blank=True, null=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name












class AdminUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username












class PerformanceMetrics(models.Model):
    date = models.DateField(auto_now_add=True)
    total_cases = models.IntegerField(default=0)
    pending_cases = models.IntegerField(default=0)
    resolved_cases = models.IntegerField(default=0)
    detection_accuracy = models.FloatField(default=0.0)
    avg_resolution_time = models.FloatField(default=0.0)  # in hours
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"Metrics for {self.date}"
