from django.db import models
from django.utils import timezone



class Student(models.Model):
    
    PROGAMMING = 'PR'
    NETWORKING = 'NT'
    PCTECH = 'PC'
    COURSE_CHOICES = (
        (PROGAMMING, 'Programming'),
        (NETWORKING, 'Networking'),
        (PCTECH, 'PC Technichian'),
    )
    
    createdby = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    icnum = models.CharField('ID Number',max_length=12,unique=True,blank=False,null=False)
    # name = models.TextField()
    name = models.CharField('Name',max_length=300)
    course = models.CharField('Courserwork',max_length=2,choices=COURSE_CHOICES,default=PCTECH,)
    created_date = models.DateTimeField('Created Date',default=timezone.now)

    def __str__(self):
        return self.icnum
# Create your models here.
