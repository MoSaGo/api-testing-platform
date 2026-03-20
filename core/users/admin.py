from django.contrib import admin
from .models import CustomUser, Project, Endpoint, RequestHistory,TestSuite, TestCase, TestRun


admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(Endpoint)
admin.site.register(RequestHistory)
admin.site.register(TestSuite)
admin.site.register(TestCase)
admin.site.register(TestRun)