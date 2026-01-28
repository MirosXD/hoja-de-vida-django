from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import RegexValidator

# Validador para asegurar exactamente 10 dígitos numéricos
telefono_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="El número debe tener exactamente 10 dígitos numéricos."
)

# ======================================================
# DATOS PERSONALES
# ======================================================
class DatosPersonales(models.Model):
    idperfil = models.AutoField(primary_key=True)
    descripcionperfil = models.CharField(max_length=50, blank=True, null=True)
    perfilactivo = models.IntegerField(default=1, blank=True, null=True)
    apellidos = models.CharField(max_length=60, blank=True, null=True)
    nombres = models.CharField(max_length=60, blank=True, null=True)
    nacionalidad = models.CharField(max_length=20, blank=True, null=True)
    lugarnacimiento = models.CharField(max_length=60, blank=True, null=True)
    fechanacimiento = models.DateField(blank=True, null=True)
    
    # Cédula con validación estricta
    numerocedula = models.CharField(unique=True, max_length=10, validators=[telefono_validator])
    
    # SEXO: Ahora como desplegable (Masculino/Femenino)
    OPCIONES_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    sexo = models.CharField(
        db_column='sexo', 
        max_length=1, 
        choices=OPCIONES_SEXO,
        blank=True, 
        null=True,
        verbose_name="Sexo"
    )
    
    estadocivil = models.CharField(max_length=50, blank=True, null=True)
    
    # LICENCIA: Ahora solo con Si y No (Sin Talvez)
    OPCIONES_LICENCIA = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]
    licenciaconducir = models.CharField(
        db_column='licenciaconducir', 
        max_length=10, 
        blank=True, 
        null=True,
        choices=OPCIONES_LICENCIA,
        verbose_name="¿Tiene licencia de conducir?"
    )
    
    # TELÉFONOS con validación de 10 dígitos
    telefonoconvencional = models.CharField(max_length=10, validators=[telefono_validator], blank=True, null=True)
    telefonofijo = models.CharField(max_length=10, validators=[telefono_validator], blank=True, null=True)
    
    direcciontrabajo = models.CharField(max_length=50, blank=True, null=True)
    direcciondomiciliaria = models.CharField(max_length=50, blank=True, null=True)
    sitioweb = models.CharField(max_length=60, blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def clean(self):
        # Validación extra de seguridad: Longitud exacta 10
        campos_validar = {
            'numerocedula': self.numerocedula,
            'telefonoconvencional': self.telefonoconvencional,
            'telefonofijo': self.telefonofijo
        }
        for campo, valor in campos_validar.items():
            if valor and len(str(valor)) != 10:
                raise ValidationError({campo: "Error: Este campo debe tener exactamente 10 dígitos."})
            
        if self.fechanacimiento and self.fechanacimiento > timezone.now().date():
            raise ValidationError({'fechanacimiento': "Error: La fecha de nacimiento no puede ser futura."})

    class Meta:
        managed = False
        db_table = 'datospersonales'
        verbose_name = "Datos Personales"
        verbose_name_plural = "Datos Personales"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

# ======================================================
# EXPERIENCIA LABORAL
# ======================================================
class ExperienciaLaboral(models.Model):
    idexperiencialaboral = models.AutoField(primary_key=True)
    cargodesempenado = models.CharField(max_length=100, blank=True, null=True)
    nombrempresa = models.CharField(max_length=50, blank=True, null=True)
    fechainiciogestion = models.DateField(blank=True, null=True)
    fechafingestion = models.DateField(blank=True, null=True)
    descripcionfunciones = models.CharField(max_length=100, blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(upload_to='certificados_laborales/', blank=True, null=True)
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)

    def clean(self):
        if self.fechainiciogestion and self.fechafingestion:
            if self.fechainiciogestion > self.fechafingestion:
                raise ValidationError("Error: La fecha de inicio no puede ser posterior a la de fin.")
        
        if self.perfil.fechanacimiento and self.fechainiciogestion:
            if self.fechainiciogestion < self.perfil.fechanacimiento:
                raise ValidationError("Error: No puedes registrar experiencia laboral anterior a tu fecha de nacimiento.")

    class Meta:
        managed = False
        db_table = 'experiencialaboral'

# ======================================================
# PRODUCTOS LABORALES
# ======================================================
class ProductosLaborales(models.Model):
    idproductoslaborales = models.AutoField(primary_key=True)
    nombreproducto = models.CharField(max_length=100, blank=True, null=True)
    fechaproducto = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    foto_producto = models.ImageField(upload_to='productos_laborales/', blank=True, null=True)
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)

    def clean(self):
        if self.fechaproducto and self.fechaproducto > timezone.now().date():
            raise ValidationError("Error: La fecha del producto no puede ser futura.")

    class Meta:
        managed = False
        db_table = 'productoslaborales'

# ======================================================
# RECONOCIMIENTOS
# ======================================================
class Reconocimientos(models.Model):
    idreconocimiento = models.AutoField(primary_key=True)
    tiporeconocimiento = models.CharField(max_length=100, blank=True, null=True)
    fechareconocimiento = models.DateField(blank=True, null=True)
    descripcionreconocimiento = models.CharField(max_length=100, blank=True, null=True)
    institucioncertificado = models.CharField(max_length=150, blank=True, null=True)
    fotocertificado = models.ImageField(upload_to='reconocimientos_fotos/', blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(upload_to='reconocimientos_docs/', blank=True, null=True)
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)

    def clean(self):
        if self.fechareconocimiento and self.fechareconocimiento > timezone.now().date():
            raise ValidationError("Error: El reconocimiento no puede tener una fecha futura.")

    class Meta:
        managed = False
        db_table = 'reconocimientos'

# ======================================================
# CURSOS REALIZADOS
# ======================================================
class CursosRealizados(models.Model):
    idcursorealizado = models.AutoField(primary_key=True)
    nombrecurso = models.CharField(max_length=100, blank=True, null=True)
    fechainicio = models.DateField(blank=True, null=True)
    fechafin = models.DateField(blank=True, null=True)
    totalhoras = models.IntegerField(blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.ImageField(upload_to='cursos_certificados/', blank=True, null=True)
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)

    def clean(self):
        if self.fechainicio and self.fechafin:
            if self.fechainicio > self.fechafin:
                raise ValidationError("Error: La fecha de fin del curso no puede ser anterior al inicio.")
        if self.totalhoras is not None and self.totalhoras < 0:
            raise ValidationError("Error: El total de horas no puede ser negativo.")

    class Meta:
        managed = False
        db_table = 'cursosrealizados'

# ======================================================
# PRODUCTOS ACADÉMICOS
# ======================================================
class ProductosAcademicos(models.Model):
    idproductoacademico = models.AutoField(primary_key=True)
    nombreproducto = models.CharField(max_length=100, blank=True, null=True)
    fechaproducto = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    foto_producto = models.ImageField(upload_to='productos_academicos/', blank=True, null=True)
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)

    def clean(self):
        if self.fechaproducto and self.fechaproducto > timezone.now().date():
            raise ValidationError("Error: La fecha del producto académico no puede ser futura.")

    class Meta:
        managed = False
        db_table = 'productosacademicos'

# ======================================================
# VENTA GARAGE
# ======================================================
class VentaGarage(models.Model):
    idventagarage = models.AutoField(primary_key=True)
    nombreproducto = models.CharField(max_length=100, blank=True, null=True)
    estadoproducto = models.CharField(max_length=40, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    valordelbien = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='venta_garage/', blank=True, null=True)
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)

    def clean(self):
        if self.valordelbien is not None and self.valordelbien < 0:
            raise ValidationError("Error: El valor del bien no puede ser negativo.")

    class Meta:
        managed = False
        db_table = 'ventagarage'