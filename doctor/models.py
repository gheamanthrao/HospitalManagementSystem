from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=100, default="John Doe")
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=100, null=True)
    phoneNumber = models.CharField(max_length=20, null=True, validators=[RegexValidator("\d{10}")])
    email = models.EmailField(null=True)
    def __str__(self):
        return self.pk + " " + self.name

class Room(models.Model):
    roomType = [('w', "Ward"), ('o', 'Operation Theatre')]
    type = models.CharField(max_length=10, choices=roomType, default='w')
    available = models.BooleanField(default=False)

class Doctor(models.Model):
    name = models.CharField(max_length=100, default="Vijay")
    address = models.CharField(max_length=100, null=True)
    phoneNumber = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    department = models.CharField(max_length = 20)
    officeNumber = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,5}', message="Office number should be between 1 and 5 digits")])
    def __str__(self):
        return self.pk + " " + self.name

class Appointment(models.Model):
    patientID = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_booked')
    doctorID = models.ForeignKey(Doctor, related_name='doctor_assigned', on_delete=models.CASCADE)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField(null=True, blank=True)
    prescription = models.TextField(null=True, blank=True)
    priorityChoices = [
        (0, "Low"),
        (1, "Medium"),
        (2, "High")
    ]
    priority = models.IntegerField(choices=priorityChoices, default=0)
    appReport = models.FileField(null=True, blank=True)
    reportGenerationTime = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return str(self.pk) + " - " + str(self.patientID) + " - " + self.startTime

class Admission(models.Model):
    def _validate_room(value):
        if value.type != 'w':
            raise ValidationError('This room is not an admission ward')
    patientID = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_admitted')
    roomID = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='patient_admitted', validators=[_validate_room])
    startTime = models.DateTimeField()
    endTime = models.DateTimeField(null=True, blank=True)

class Test(models.Model):
    testName = models.CharField(max_length=50)
    patientID = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_tested')
    scheduledTime = models.DateTimeField()
    testReport = models.FileField()
    reportGenerationTime = models.DateTimeField()

class Operation(models.Model):
    def _validate_room(value):
        if value.type != 'o':
            raise ValidationError('This room is not suitable for operations.')
    opName = models.CharField(max_length=50)
    patientID = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_operated')
    doctorID = models.ManyToManyField(Doctor, related_name='doctors')
    opTheatre = models.ForeignKey(Room, related_name='where', validators=[_validate_room], on_delete=models.CASCADE)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    operationReport = models.FileField()
    reportGenerationTime = models.DateTimeField()