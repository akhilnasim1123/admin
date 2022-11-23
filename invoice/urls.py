# Create your tests here.
from django.urls import path
from . import views

urlpatterns = [
    path('invoice/<int:id>',views.order_details_user_side,name='order_details'),
    path('pdf_view/<int:id>', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/<int:id>', views.DownloadPDF.as_view(), name="pdf_download"),


]
