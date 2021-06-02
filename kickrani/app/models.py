from django.db import models

# Create your models here.
class Kickrani(models.Model):
    kickId = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=250, null=True)
    helmet = models.IntegerField(default=0, null=True)
    person = models.IntegerField(default=0, null=True)
    image = models.CharField(max_length=250, null=True)
    #image = models.ImageField(upload_to='image')
    datetime = models.CharField(max_length=250, null=True)
    location = models.CharField(max_length=250, null=True)
    num_brand = models.IntegerField(default=0, null=True)
    violation= models.IntegerField(default=0, null=True) # 1: 2인이상 탑승 위반, 2: 헬멧 미착용 위반, 3: 2인이상 및 헬멧 위반

class Rider(models.Model):
    riderId = models.AutoField(primary_key=True)
    kickId = models.ForeignKey(Kickrani, on_delete=models.CASCADE)
    riderLocation = models.CharField(max_length=250, null=True)
    riderPercentage=models.FloatField(default=0, null=True)

class Violation(models.Model):
    violationId=models.AutoField(primary_key=True)
    riderId=models.ForeignKey(Rider, on_delete=models.CASCADE)
    helmetLocation= models.CharField(max_length=250, null=True)
    personLocation= models.CharField(max_length=250, null=True)
    personPercentage= models.FloatField(max_length=250, null=True)