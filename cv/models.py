from django.db import models

class DatosPersonales(models.Model):
    idperfil = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100)
    descripcionperfil = models.TextField()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class ExperienciaLaboral(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100)
    nombreempresa = models.CharField(max_length=100)
    fechainicio = models.DateField()
    fechafin = models.DateField(null=True, blank=True)
    trabajaactualmente = models.BooleanField(default=False)
    descripcionresponsabilidades = models.TextField()
    activarparaqueseveaenfront = models.BooleanField(default=True)

class CursosRealizados(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombrecurso = models.CharField(max_length=200)
    institucion = models.CharField(max_length=200)
    numerodehoras = models.IntegerField()
    activarparaqueseveaenfront = models.BooleanField(default=True)

# Agrega estas clases si las usas en tu views.py, de lo contrario darán error de importación
class Reconocimientos(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    activarparaqueseveaenfront = models.BooleanField(default=True)

class ProductosAcademicos(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    activarparaqueseveaenfront = models.BooleanField(default=True)

class ProductosLaborales(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)

class VentaGarage(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombreproducto = models.CharField(max_length=100)
    estadoproducto = models.CharField(max_length=50)
    valordelbien = models.DecimalField(max_digits=10, decimal_places=2)
    activarparaqueseveaenfront = models.BooleanField(default=True)