from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import RedirectView


admin.site.index_title = 'Social platform overview'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('social.urls')), 
    path('', RedirectView.as_view(url="social/")),  
] 
