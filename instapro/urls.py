from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from instapro import settings

admin.site.site_header ='$ SUPER SPTECH INSTAPRO+ ??? '
admin.site.site_title = 'PAL SAHAB '
admin.site.index_title = '??? ... SUPER SPTECH INSTAPRO+ FOR SPTECH PAL .... ???'

urlpatterns = [
    path('sptech/', admin.site.urls),
    path('social/', include('social.urls')), 
    path('', RedirectView.as_view(url="social/")),  
      
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
