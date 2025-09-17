from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    empresa = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario_acceso = models.CharField(max_length=50, unique=True)
    contrasena_acceso = models.CharField(max_length=128)

    def hash_password(self, raw_password):
        self.contrasena_acceso = make_password(raw_password)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.contrasena_acceso)

    def check_password(self, raw_password):
        return self.verify_password(raw_password)

    @classmethod
    def create_user_secure(cls, usuario_acceso, password, nombre, email, telefono='', empresa=''):
        cliente = cls(
            usuario_acceso=usuario_acceso,
            nombre=nombre,
            email=email,
            telefono=telefono,
            empresa=empresa
        )
        cliente.hash_password(password)
        cliente.save()
        return cliente

    def save(self, *args, **kwargs):
        if self.contrasena_acceso and not self.contrasena_acceso.startswith(('pbkdf2_', 'bcrypt', 'argon2')):
            if not self.pk or Cliente.objects.filter(pk=self.pk).first().contrasena_acceso != self.contrasena_acceso:
                self.contrasena_acceso = make_password(self.contrasena_acceso)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

