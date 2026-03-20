from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProfileView, ProjectCreateView, UserRegisterView, EndpointView
from .views import ExecuteEndpointView, RequestHistoryView, HealthCheckView, TestSuiteView 
from .views import TestCaseView, RunTestSuiteView, TestRunView



urlpatterns = [
    #definimos la ruta para el registro de usuarios, utilizando la vista UserRegisterView
    path('register/', UserRegisterView.as_view(), name='user-register'),
    #definimos las rutas para la obtención y refresco de tokens JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('projects/', ProjectCreateView.as_view(), name='projects'),
    path('endpoints/', EndpointView.as_view(), name='endpoints'),
    path('endpoints/<int:endpoint_id>/execute/',ExecuteEndpointView.as_view(),
         name='execute-endpoint'
        ),
    path('history/', RequestHistoryView.as_view(), name='request-history'),
    path("health/", HealthCheckView.as_view(), name="health"),
    path("testsuites/", TestSuiteView.as_view(), name="testsuites"),
    path("testcases/", TestCaseView.as_view(), name="testcases"),
    path('testsuites/<int:suite_id>/run/', RunTestSuiteView.as_view(), name='run-testsuite'),
    path('testruns/', TestRunView.as_view(), name='testruns'),

]