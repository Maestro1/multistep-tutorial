from django.urls import path, include, re_path
#from . import views
from membership.views import ApplicationWizardView,home
app_name='multistepapp'


urlpatterns = [
    path('user-application/',ApplicationWizardView.as_view(),name='registration'),
    path('',home,name='home'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
