from rest_framework import serializers
from .models import CustomUser
from .models import Project
from .models import Endpoint
from .models import RequestHistory
from .models import TestSuite
from .models import TestCase
from .models import TestRun


class UserRegisterSerializer(serializers.ModelSerializer):
    #significa que el campo password solo se usará para escribir, no se incluirá en las
    #respuestas json de la API, para proteger la información sensible del usuario
    password = serializers.CharField(write_only=True)

    class Meta:
        #meta especifica el modelo y los campos que esperas recibir
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'bio')

    #crea una nueva instancia de CustomUser utilizando los datos validados
    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],    
            email=validated_data['email'],
            bio=validated_data.get('bio', '')
        )
        #hashea la contraseña antes de guardarla en la base de datos
        user.set_password(validated_data['password'])
        #guarda el nuevo usuario en la base de datos
        user.save()
        return user

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ["id", "name", "description", "created_at"]

class EndpointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Endpoint
        fields = [
            "id",
            "project",
            "name",
            "url",
            "method",
            "headers",
            "body",
            "created_at"
        ]
        def validate_project(self, project):
            user = self.context["request"].user

            if project.owner != user:
                raise serializers.ValidationError("You cannot use a project that is not yours.")

            return project

class RequestHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestHistory
        fields = [
            "id",
            "endpoint",
            "status_code",
            "response",
            "executed_at"
        ]

class TestSuiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestSuite
        fields = ["id", "project", "name", "created_at"]
    
class TestCaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestCase
        fields = [
            "id",
            "test_suite",
            "endpoint",
            "expected_status",
            "created_at"
        ] 

class TestRunSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestRun
        fields = [
            "id",
            "test_suite",
            "total",
            "passed",
            "failed",
            "created_at"
        ]
        
    
