# attendance/urls.py
from django.urls import path
from .api import api
from .views import register_student,generate_qr, download_qr, registration_success,attendance_view, scan_qr_code, index, scan_qrcode, scanpage2,scan_window,qrcode_results, display_registered_user

urlpatterns = [
    path('api/', api.urls),  # Connect Ninja API routes
    path('register/', register_student, name='register_student'),
    path('registration-success/<int:student_id>/', registration_success, name='registration_success'),
    path('qr/<int:student_id>/', generate_qr, name='generate_qr'),  # QR code display page
    path('qr/<int:student_id>/download/', download_qr, name='download_qr'),
    path('',attendance_view, name='attendance_view'),
    path('scan/', index, name='scan_qr_code'),
    path('scan_page/', scan_qrcode, name ='scan_qrcode'),
    path('registered_user/', display_registered_user, name='registered_user'),
    path('scn/', scan_window, name='scan_window'),
    path('qrcode_results/', qrcode_results, name='qrcode_results'),
    path('qrcode_results/<str:data>/', qrcode_results, name='qrcode_results'),


]
