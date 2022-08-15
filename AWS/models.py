from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class TrackingInformation(BaseModel):
    patient = models.ForeignKey('Patient',on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    def __str__(self):
        return seld.id,self.patient,self.latitude,self.longitude


class Patient(BaseModel):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length = 15)
    age = models.IntegerField()
    aadhar_no = models.IntegerField(null = True)
    address = models.CharField(max_length = 50)
    email = models.CharField(max_length=50, null = True)
    safe_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    safe_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    mac_address = models.CharField(max_length = 20,null = True)
    doctor = models.ForeignKey('Doctor',on_delete=models.CASCADE)
    safe_distance = models.DecimalField(max_digits=12, decimal_places=6,null = True)
    def __str__(self):
        return self.id,self.name,self.gender,self.age,self.address,self.email,self.safe_latitude,self.safe_longitude


class Kins(BaseModel):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length = 50)
    email = models.CharField(max_length=50,null = True)
    mobile = models.CharField(max_length=30)
    patient = models.ForeignKey('Patient',on_delete=models.CASCADE)
    def __str__(self):
        return self.id,self.name,self.address,self.email,self.mobile,self.patient

class Doctor(BaseModel):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50,null = True)
    mobile = models.CharField(max_length=30)
    hospital = models.ForeignKey('Hospital',on_delete=models.CASCADE,null = True)
    def __str__(self):
        return self.id,self.name,self.email,self.mobile


class HealtParameter(BaseModel):
    pulse = models.IntegerField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    aclmtr_x  = models.FloatField()
    aclmtr_y  =models.FloatField()
    aclmtr_z = models.FloatField()
    patient = models.ForeignKey('Patient',on_delete=models.CASCADE)
    def __str__(self):
        return self.id,self.pulse,self.temperature,self.humidity,self.aclmtr_x,self.aclmtr_y,self.aclmtr_z,self.patient
class Hospital(BaseModel):
    name = models.CharField(max_length = 50)
    address = models.CharField(max_length = 50)
    contact = models.CharField(max_length = 15)