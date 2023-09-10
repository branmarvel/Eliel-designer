from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, null=True)

class PersonManager(BaseUserManager):
    def create_user(self, nombre, password, correo_electronico, numero_telefono, es_disenador=False, estado=None):
        if not correo_electronico:
            raise ValueError('El correo electrónico es obligatorio')

        user = self.model(
            nombre=nombre,
            correo_electronico=self.normalize_email(correo_electronico),
            numero_telefono=numero_telefono,
            es_disenador=es_disenador,
            estado=estado,
        )

        user.set_password(password)  # Almacena la contraseña de forma segura
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre, password, correo_electronico, numero_telefono, es_disenador=False, estado=None):
        user = self.create_user(
            nombre=nombre,
            password=password,
            correo_electronico=correo_electronico,
            numero_telefono=numero_telefono,
            es_disenador=es_disenador,
            estado=estado,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Person(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    correo_electronico = models.EmailField(unique=True)
    numero_telefono = models.CharField(max_length=20)
    es_disenador = models.BooleanField(default=False)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = PersonManager()

    USERNAME_FIELD = 'correo_electronico'
    
    def __str__(self):
        return self.correo_electronico

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
class TipoDisigner(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

class Designer(models.Model):
    id = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    tipo_disenador = models.ForeignKey(TipoDisigner, on_delete=models.CASCADE)

class Invitado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    correo_electronico = models.CharField(max_length=255)
    numero_telefono = models.CharField(max_length=20)
    descripcion = models.TextField()

class Presupuesto(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    cliente = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    guest_request = models.ForeignKey(Invitado, on_delete=models.SET_NULL, null=True)

class Portfolio(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagenes = models.TextField()
    disenador = models.ForeignKey(Designer, on_delete=models.CASCADE)

class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    disenador = models.ForeignKey(Designer, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Person, on_delete=models.CASCADE)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_remitente = models.CharField(max_length=255)
    correo_electronico_remitente = models.CharField(max_length=255)
    asunto = models.CharField(max_length=255)
    contenido_mensaje = models.TextField()
    fecha_hora_envio = models.DateTimeField()
    conversacion = models.ForeignKey(Conversation, on_delete=models.CASCADE)

class PedidoPersonalizado(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    fecha_hora_creacion = models.DateTimeField()
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE)
    client = models.ForeignKey(Person, on_delete=models.CASCADE)
