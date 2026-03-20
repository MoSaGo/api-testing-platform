import requests
from rest_framework.response import Response
from rest_framework import generics
from .serializers import UserRegisterSerializer
from .models import CustomUser, Project, Endpoint, RequestHistory, TestSuite, TestCase, TestRun
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProjectSerializer
from .serializers import EndpointSerializer
from .serializers import RequestHistorySerializer
from .serializers import TestSuiteSerializer
from .serializers import TestCaseSerializer
from .serializers import TestRunSerializer
from django_filters.rest_framework import DjangoFilterBackend


#solo permite crear nuevos usuarios, no permite listar, actualizar o eliminar usuarios existentes
class UserRegisterView(generics.CreateAPIView):
    #queryset define el conjunto de datos sobre el que operará la vista, en este caso, 
    # obtiene todos los objetos CustomUser 
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

class ProfileView(APIView):
    #permite solo a los usuarios autenticados acceder a la vista
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })

class ProjectCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #filtra los proyectos para devolver solo aquellos que pertenecen al usuario autenticado
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        #asigna el usuario autenticado como propietario del proyecto al crear un nuevo proyecto
        serializer.save(owner=self.request.user)

class EndpointView(generics.ListCreateAPIView):

    serializer_class = EndpointSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Endpoint.objects.filter(project__owner=self.request.user)
    
class ExecuteEndpointView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, endpoint_id):

        try:
            endpoint = Endpoint.objects.get(
                id=endpoint_id,
                project__owner=request.user
            )
        except Endpoint.DoesNotExist:
            return Response({"error": "Endpoint not found"}, status=404)

        try:
            #realiza la solicitud HTTP utilizando la biblioteca requests, pasando el método, URL 
            #y headers del endpoint, así como el cuerpo de la solicitud si está presente
            response = requests.request(
                method=endpoint.method,
                url=endpoint.url,
                headers=endpoint.headers,
                json=endpoint.body
            )
            # guardar historial
            RequestHistory.objects.create(
                endpoint=endpoint,
                status_code=response.status_code,
                response=response.text
            )

            return Response({
                "status_code": response.status_code,
                "response": response.text
            })

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=500)
        
class RequestHistoryView(generics.ListAPIView):

    serializer_class = RequestHistorySerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status_code", "endpoint"]

    ordering_fields = ["executed_at", "status_code"]
    ordering = ["-executed_at"]

    def get_queryset(self):
        return RequestHistory.objects.filter(
            endpoint__project__owner=self.request.user
        ).order_by("-executed_at")
    
class HealthCheckView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({
            "status": "ok",
            "service": "api-testing-platform"
        })

class TestSuiteView(generics.ListCreateAPIView):

    serializer_class = TestSuiteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TestSuite.objects.filter(
            project__owner=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save()

class TestCaseView(generics.ListCreateAPIView):

    serializer_class = TestCaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TestCase.objects.filter(
            test_suite__project__owner=self.request.user
        )

class RunTestSuiteView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, suite_id):

        try:
            suite = TestSuite.objects.get(
                id=suite_id,
                project__owner=request.user
            )
        except TestSuite.DoesNotExist:
            return Response({"error": "TestSuite not found"}, status=404)

        results = []

        for test in suite.test_cases.all():

            try:
                response = requests.request(
                    method=test.endpoint.method,
                    url=test.endpoint.url,
                    headers=test.endpoint.headers,
                    json=test.endpoint.body
                )

                passed = response.status_code == test.expected_status
                status = "PASSED" if passed else "FAILED"

                results.append({
                    "name": test.endpoint.name,
                    "status": status,
                    "expected": test.expected_status,
                    "actual": response.status_code
                })

            except Exception as e:
                results.append({
                    "name": test.endpoint.name,
                    "status": "FAILED",
                    "error": str(e)
                })

        total = len(results)
        passed_count = sum(1 for r in results if r.get("status") == "PASSED")

        # guardar ejecución
        TestRun.objects.create(
            test_suite=suite,
            total=total,
            passed=passed_count,
            failed=total - passed_count
        )

        success_rate = int((passed_count / total) * 100) if total > 0 else 0

        return Response({
            "summary": {
                "total": total,
                "passed": passed_count,
                "failed": total - passed_count,
                "success_rate": f"{success_rate}%"
            },
            "tests": results
        })
    
class TestRunView(generics.ListAPIView):

    serializer_class = TestRunSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TestRun.objects.filter(
            test_suite__project__owner=self.request.user
        ).order_by("-created_at")

