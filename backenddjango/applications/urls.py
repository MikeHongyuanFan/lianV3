from django.urls import path
from .views.pdf_generation import GenerateFilledFormView

urlpatterns = [
    # Generate filled PDF form
    path('<int:application_id>/generate-pdf/', GenerateFilledFormView.as_view(), name='application-generate-pdf'),
]
