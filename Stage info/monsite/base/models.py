from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, gender, interet, latitude, longitude, age, password=None, last_name=None, first_name=None, **extra_fields):
        """
        Create and return a regular user with an email, username and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, last_name=last_name, gender=gender, interet=interet, latitude=latitude, age=age, longitude = longitude, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, first_name='Super', last_name='User', gender='Autre', interet='Autre', latitude=0.0, longitude=0.0, age=18, **extra_fields):
        """
        Create and return a superuser with an email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            interet=interet,
            age=age,
            latitude=latitude,
            longitude=longitude,
            **extra_fields
        )

class CustomUser(AbstractUser):
    
    GENDER_CHOICES = [
    ('Homme', 'Homme'),
    ('Femme', 'Femme'),
    ('Autre', 'Autre'),
]

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)

    INTEREST_CHOICES = [
    ('Homme', 'Homme'),
    ('Femme', 'Femme'),
    ('Both', 'Both'),
]
    interet = models.CharField(max_length=20, choices=INTEREST_CHOICES, blank=True, null=True)
    latitude = models.FloatField(max_length=20)
    longitude = models.FloatField(max_length=20)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    age = models.IntegerField()

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Utilisateur personnalisé'
        verbose_name_plural = 'Utilisateurs personnalisés'

    def __str__(self):
        return self.username

    groups = models.ManyToManyField('auth.Group', related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_user_permissions', blank=True)

class Note(models.Model):
    emitter = models.ForeignKey(CustomUser, related_name='emitted_notes', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_notes', on_delete=models.CASCADE)
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emitter} {'liked' if self.is_like else 'disliked'} {self.receiver}"
    
