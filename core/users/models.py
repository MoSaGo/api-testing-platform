from django.contrib.auth.models import AbstractUser
from django.db import models


"""Creamos un modelo de usuario personalizado heredando de AbstractUser
AbstractUser es una clase que proporciona Django para crear modelos de usuario personalizados
con campos predefinidos como username, password, first_name, last_name, email, etc.
Al heredar de esta clase, podemos agregar campos adicionales a nuestro modelo de usuario sin 
tener que reinventar la rueda en cuanto a la funcionalidad básica de autenticación y gestión de 
usuarios que Django ya proporciona.
"""
class CustomUser(AbstractUser):
    # Aquí podemos agregar campos extra si queremos, por ejemplo:
    bio = models.TextField(blank=True, null=True)
    #agregamos un campo de biografía que es opcional (blank=True, null=True), 
    # lo que significa que el campo puede estar vacío 

    def __str__(self):
        # Devuelve el username del usuario como representación de cadena del objeto en cada query
        return self.username

class Project(models.Model):
    # El modelo Project representa un proyecto que pertenece a un usuario (owner).
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="projects"
        #related_name="projects" establece una relación inversa en el modelo CustomUser 
        #para acceder a los proyectos que pertenecen a ese usuario
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Devuelve el nombre del proyecto como representación de cadena del objeto
        return self.name
    
class Endpoint(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="endpoints"
    )

    name = models.CharField(max_length=255)

    url = models.URLField()

    method = models.CharField(
        max_length=10,
        choices=[
            ("GET", "GET"),
            ("POST", "POST"),
            ("PUT", "PUT"),
            ("DELETE", "DELETE"),
        ]
    )

    headers = models.JSONField(blank=True, null=True)

    body = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.url}"

class RequestHistory(models.Model):

    endpoint = models.ForeignKey(
        Endpoint,
        on_delete=models.CASCADE,
        related_name="executions"
    )

    status_code = models.IntegerField()

    response = models.TextField()

    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.endpoint.name} - {self.status_code}"
    
class TestSuite(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="test_suites"
    )

    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TestCase(models.Model):

    test_suite = models.ForeignKey(
        TestSuite,
        on_delete=models.CASCADE,
        related_name="test_cases"
    )

    endpoint = models.ForeignKey(
        Endpoint,
        on_delete=models.CASCADE
    )

    expected_status = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.endpoint.name} - {self.expected_status}"

class TestRun(models.Model):

    test_suite = models.ForeignKey(
        TestSuite,
        on_delete=models.CASCADE,
        related_name="runs"
    )

    total = models.IntegerField()
    passed = models.IntegerField()
    failed = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Run {self.id} - {self.test_suite.name}"



    test_suite = models.ForeignKey(
        TestSuite,
        on_delete=models.CASCADE,
        related_name="runs"
    )

    total = models.IntegerField()
    passed = models.IntegerField()
    failed = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Run {self.id} - {self.test_suite.name}"

