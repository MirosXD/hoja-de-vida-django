from django.db import models


# ======================================================
# DATOS PERSONALES
# ======================================================
class DatosPersonales(models.Model):
    SEXO_H = "H"
    SEXO_M = "M"
    SEXO_CHOICES = [
        (SEXO_H, "Hombre"),
        (SEXO_M, "Mujer"),
    ]

    idperfil = models.AutoField("ID del perfil", primary_key=True)

    descripcionperfil = models.CharField(
        "Descripción del perfil", max_length=50, blank=True, null=True
    )
    perfilactivo = models.IntegerField("Perfil activo", blank=True, null=True)

    apellidos = models.CharField("Apellidos", max_length=60, blank=True, null=True)
    nombres = models.CharField("Nombres", max_length=60, blank=True, null=True)

    nacionalidad = models.CharField("Nacionalidad", max_length=20, blank=True, null=True)
    lugarnacimiento = models.CharField(
        "Lugar de nacimiento", max_length=60, blank=True, null=True
    )
    fechanacimiento = models.DateField(
        "Fecha de nacimiento", blank=True, null=True
    )

    numerocedula = models.CharField(
        "Número de cédula", max_length=10, unique=True
    )
    sexo = models.CharField(
        "Sexo", max_length=1, choices=SEXO_CHOICES, blank=True, null=True
    )

    estadocivil = models.CharField(
        "Estado civil", max_length=50, blank=True, null=True
    )
    licenciaconducir = models.CharField(
        "Licencia de conducir", max_length=6, blank=True, null=True
    )

    telefonoconvencional = models.CharField(
        "Teléfono convencional", max_length=15, blank=True, null=True
    )
    telefonofijo = models.CharField(
        "Teléfono fijo", max_length=15, blank=True, null=True
    )

    direcciontrabajo = models.CharField(
        "Dirección de trabajo", max_length=50, blank=True, null=True
    )
    direcciondomiciliaria = models.CharField(
        "Dirección domiciliaria", max_length=50, blank=True, null=True
    )

    sitioweb = models.CharField(
        "Sitio web", max_length=60, blank=True, null=True
    )
    foto = models.ImageField(
        "Foto", upload_to="fotos/", blank=True, null=True
    )

    class Meta:
        db_table = "datospersonales"
        verbose_name = "Datos personales"
        verbose_name_plural = "Datos personales"

    def __str__(self):
        return (
            f"{self.apellidos or ''} {self.nombres or ''}".strip()
            or f"Perfil {self.idperfil}"
        )


# ======================================================
# EXPERIENCIA LABORAL
# ======================================================
class ExperienciaLaboral(models.Model):
    idexperiencialaboral = models.AutoField(
        "ID experiencia laboral", primary_key=True
    )

    perfil = models.ForeignKey(
        DatosPersonales,
        verbose_name="Perfil",
        on_delete=models.CASCADE,
        related_name="experiencias_laborales",
    )

    cargodesempenado = models.CharField(
        "Cargo desempeñado", max_length=100, blank=True, null=True
    )
    nombrempresa = models.CharField(
        "Nombre de la empresa", max_length=50, blank=True, null=True
    )

    fechainiciogestion = models.DateField(
        "Fecha de inicio", blank=True, null=True
    )
    fechafingestion = models.DateField(
        "Fecha de fin", blank=True, null=True
    )

    descripcionfunciones = models.CharField(
        "Descripción de funciones", max_length=100, blank=True, null=True
    )

    activarparaqueseveaenfront = models.BooleanField(
        "Mostrar en la hoja de vida", default=True
    )
    rutacertificado = models.CharField(
        "Ruta del certificado", max_length=100, blank=True, null=True
    )

    class Meta:
        db_table = "experiencialaboral"
        verbose_name = "Experiencia laboral"
        verbose_name_plural = "Experiencias laborales"

    def __str__(self):
        return f"{self.cargodesempenado or ''} - {self.nombrempresa or ''}".strip()


# ======================================================
# RECONOCIMIENTOS
# ======================================================
class Reconocimiento(models.Model):
    TIPO_ACADEMICO = "Académico"
    TIPO_PUBLICO = "Público"
    TIPO_PRIVADO = "Privado"
    TIPO_CHOICES = [
        (TIPO_ACADEMICO, "Académico"),
        (TIPO_PUBLICO, "Público"),
        (TIPO_PRIVADO, "Privado"),
    ]

    idreconocimiento = models.AutoField(
        "ID reconocimiento", primary_key=True
    )

    perfil = models.ForeignKey(
        DatosPersonales,
        verbose_name="Perfil",
        on_delete=models.CASCADE,
        related_name="reconocimientos",
    )

    tiporeconocimiento = models.CharField(
        "Tipo de reconocimiento",
        max_length=100,
        choices=TIPO_CHOICES,
        blank=True,
        null=True,
    )
    fechareconocimiento = models.DateField(
        "Fecha de reconocimiento", blank=True, null=True
    )
    descripcionreconocimiento = models.CharField(
        "Descripción", max_length=100, blank=True, null=True
    )

    institucioncertificado = models.CharField(
        "Institución del certificado", max_length=150, blank=True, null=True
    )
    fotocertificado = models.ImageField(
        "Foto del certificado",
        upload_to="certificados/reconocimientos/",
        blank=True,
        null=True,
    )

    activarparaqueseveaenfront = models.BooleanField(
        "Mostrar en la hoja de vida", default=True
    )
    rutacertificado = models.CharField(
        "Ruta del certificado", max_length=100, blank=True, null=True
    )

    class Meta:
        db_table = "reconocimientos"
        verbose_name = "Reconocimiento"
        verbose_name_plural = "Reconocimientos"

    def __str__(self):
        return f"{self.tiporeconocimiento or 'Reconocimiento'} - {self.perfil_id}"


# ======================================================
# CURSOS REALIZADOS
# ======================================================
class CursoRealizado(models.Model):
    idcursorealizado = models.AutoField(
        "ID curso realizado", primary_key=True
    )

    perfil = models.ForeignKey(
        DatosPersonales,
        verbose_name="Perfil",
        on_delete=models.CASCADE,
        related_name="cursos_realizados",
    )

    nombrecurso = models.CharField(
        "Nombre del curso", max_length=100, blank=True, null=True
    )
    fechainicio = models.DateField(
        "Fecha de inicio", blank=True, null=True
    )
    fechafin = models.DateField(
        "Fecha de fin", blank=True, null=True
    )
    totalhoras = models.IntegerField(
        "Total de horas", blank=True, null=True
    )

    activarparaqueseveaenfront = models.BooleanField(
        "Mostrar en la hoja de vida", default=True
    )
    rutacertificado = models.CharField(
        "Ruta del certificado", max_length=100, blank=True, null=True
    )

    class Meta:
        db_table = "cursosrealizados"
        verbose_name = "Curso realizado"
        verbose_name_plural = "Cursos realizados"

    def __str__(self):
        return self.nombrecurso or f"Curso {self.idcursorealizado}"


# ======================================================
# PRODUCTO ACADÉMICO
# ======================================================
class ProductoAcademico(models.Model):
    idproductoacademico = models.AutoField(
        "ID producto académico", primary_key=True
    )

    perfil = models.ForeignKey(
        DatosPersonales,
        verbose_name="Perfil",
        on_delete=models.CASCADE,
        related_name="productos_academicos",
    )

    nombreproducto = models.CharField(
        "Nombre del producto", max_length=100, blank=True, null=True
    )
    fechaproducto = models.DateField(
        "Fecha del producto", blank=True, null=True
    )
    descripcion = models.CharField(
        "Descripción", max_length=100, blank=True, null=True
    )

    activarparaqueseveaenfront = models.BooleanField(
        "Mostrar en la hoja de vida", default=True
    )

    class Meta:
        db_table = "productosacademicos"
        verbose_name = "Producto académico"
        verbose_name_plural = "Productos académicos"

    def __str__(self):
        return self.nombreproducto or f"Producto Acad. {self.idproductoacademico}"


# ======================================================
# PRODUCTO LABORAL
# ======================================================
class ProductoLaboral(models.Model):
    idproductoslaborales = models.AutoField(
        "ID producto laboral", primary_key=True
    )

    perfil = models.ForeignKey(
        DatosPersonales,
        verbose_name="Perfil",
        on_delete=models.CASCADE,
        related_name="productos_laborales",
    )

    nombreproducto = models.CharField(
        "Nombre del producto", max_length=100, blank=True, null=True
    )
    fechaproducto = models.DateField(
        "Fecha del producto", blank=True, null=True
    )
    descripcion = models.CharField(
        "Descripción", max_length=100, blank=True, null=True
    )

    activarparaqueseveaenfront = models.BooleanField(
        "Mostrar en la hoja de vida", default=True
    )

    class Meta:
        db_table = "productoslaborales"
        verbose_name = "Producto laboral"
        verbose_name_plural = "Productos laborales"

    def __str__(self):
        return self.nombreproducto or f"Producto Lab. {self.idproductoslaborales}"


# ======================================================
# VENTA GARAGE
# ======================================================
class VentaGarage(models.Model):
    ESTADO_BUENO = "Bueno"
    ESTADO_REGULAR = "Regular"
    ESTADO_CHOICES = [
        (ESTADO_BUENO, "Bueno"),
        (ESTADO_REGULAR, "Regular"),
    ]

    idventagarage = models.AutoField(
        "ID venta garage", primary_key=True
    )

    perfil = models.ForeignKey(
        DatosPersonales,
        verbose_name="Perfil",
        on_delete=models.CASCADE,
        related_name="venta_garage",
    )

    nombreproducto = models.CharField(
        "Nombre del producto", max_length=100, blank=True, null=True
    )
    estadoproducto = models.CharField(
        "Estado del producto",
        max_length=40,
        choices=ESTADO_CHOICES,
        blank=True,
        null=True,
    )
    descripcion = models.CharField(
        "Descripción", max_length=100, blank=True, null=True
    )

    valordelbien = models.DecimalField(
        "Valor del bien", max_digits=5, decimal_places=2, blank=True, null=True
    )
    activarparaqueseveaenfront = models.BooleanField(
        "Mostrar en la hoja de vida", default=True
    )

    class Meta:
        db_table = "ventagarage"
        verbose_name = "Venta garage"
        verbose_name_plural = "Venta garage"

    def __str__(self):
        return self.nombreproducto or f"Item {self.idventagarage}"
