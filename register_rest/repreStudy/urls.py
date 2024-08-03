from django.urls import path, include

urlpatterns = [
    path('representante/', include('repreStudy.representante_urls')),
    path('alumno/', include('repreStudy.alumno_urls')),
]
