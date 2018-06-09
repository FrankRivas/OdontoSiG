from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class Paciente(models.Model):
    Edad = models.IntegerField(null=False)
    Sexo = models.CharField(max_length=1, null=False)
    Residencia = models.CharField(max_length=1, null=False)
    FechaConsul = models.DateField(null=False)

class Pieza(models.Model):
    Posicion = models.IntegerField(null=False)
    EstOMS = models.CharField(max_length=50)
    EstICDAS = models.CharField(max_length=50)
    Paciente = models.ForeignKey(Paciente)

class Carie(models.Model):
    Descripcion = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.Descripcion

class Tratamiento(models.Model):
    Caries = models.ForeignKey(Carie)
    NomTratam = models.CharField(max_length=255, null=False)
    CodDental = models.IntegerField(null=False)

    def __str__(self):
        return self.NomTratam

class Superficie(models.Model):
    Paciente = models.ForeignKey(Paciente)
    Tratamiento = models.ForeignKey(Tratamiento)
    Posicion = models.IntegerField(null=False)
    CodSuper = models.IntegerField(null=False)
    NomSuper = models.CharField(max_length=255, null=False)
    EstICDAS = models.CharField(max_length=50)
    EstOMS = models.CharField(max_length=50)
    CodCar = models.IntegerField()

class HistorialOdonto(models.Model):
    Paciente = models.ForeignKey(Paciente)
    EvalSistem = models.CharField(max_length=50, null=False)
    FrecCepilla = models.IntegerField(null=False)
    HabitosBucal = models.CharField(max_length=255,null=False)

    def __str__(self):
        return self.EvalSistem



class Accion(models.Model):
    NombreAccion = models.CharField(max_length=150, null=False)
    InfoControl = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.NombreAccion

class Bitacora(models.Model):
    Usuario = models.ForeignKey(User, null=False)
    Accion = models.ForeignKey(Accion, null=False)
    FechaAccion = models.DateField(null=False,default=now)
    Afectado = models.CharField(max_length=50,null=True)
