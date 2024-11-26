from django.contrib.auth.models import User
from django.db import models

class Racer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    team_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    car_description = models.TextField(blank=True)
    experience = models.IntegerField(default=0)
    class_choices = [
        ('F1', 'Formula 1'),
        ('F2', 'Formula 2'),
        ('F3', 'Formula 3'),
        ('Rally', 'Rally'),
        ('Moto', 'Moto'),
        ('Karting', 'Karting'),
    ]
    class_type = models.CharField(max_length=10, choices=class_choices)
    birth_date = models.DateField()
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.jpg')

    def __str__(self):
        return self.full_name

class Race(models.Model):
    registered_racers = models.ManyToManyField(Racer, blank=True, related_name='registered_races')
    name = models.CharField(max_length=200)
    race_class = models.CharField(max_length=10, choices=Racer.class_choices)
    date = models.DateTimeField()
    age_limit = models.IntegerField(default=18)
    description = models.TextField()
    location = models.TextField()
    image = models.ImageField(upload_to='race_photos/', default='race_photos/default_race.jpg')
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class RaceRegistration(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

class Result(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    result_time = models.DurationField()

    def __str__(self):
        return f"{self.racer.full_name} - {self.race.name}"

class Comment(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    comment_type_choices = [
        ('question', 'Question'),
        ('review', 'Review'),
        ('collaboration', 'Collaboration'),
    ]
    comment_type = models.CharField(max_length=20, choices=comment_type_choices)
    rating = models.IntegerField(null=True, blank=True)  # Только для отзывов
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.race.name}"
