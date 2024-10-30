import base64
from django.utils import timezone
from datetime import timedelta
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .form import StudentRegistrationForm
import qrcode
from io import BytesIO
import cv2
import  numpy as np
from pyzbar.pyzbar import decode

from .models import Attendance, Student_record


# View to handle the registration form and QR code generation
def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()  # Save the student record to the database
            return redirect('registration_success', student_id=student.person_id)  # Redirect to the success page
    else:
        form = StudentRegistrationForm()

    return render(request, 'register_page.html', {'form': form})


# Success view to show QR options after registration
def registration_success(request, student_id):
    return render(request, 'success.html', {'student_id': student_id})



def generate_qr(request, student_id):
    # Generate the QR code from the student_id
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(student_id)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Save the image in memory
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Encode the image in base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Convert the image to a response and render it in a template
    return render(request, 'qr_code.html', {
        'student_id': student_id,
        'qr_code_image': image_base64,
    })


# View to download the QR code image
def download_qr(request, student_id):
    # Generate the QR code image again for download
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(student_id)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Save the image in memory for download
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Serve the image as a downloadable file
    response = HttpResponse(buffer, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename=qr_code_{student_id}.png'
    return response


def attendance_view(request):
    # Get all attendance records
    now = timezone.now()
    attendance_records = Attendance.objects.all()
    student_records = Student_record.objects.all()

    records_with_countdown = []
    students_in_attendance = []
    record_without_duplicates = []
    for record in attendance_records:

        for student in student_records:
            if record.person_id == student.person_id:
        # Calculate the time elapsed since arrival_time
                time_elapsed = now - record.arrival_time
                time_remaining = timedelta(hours=2) - time_elapsed

        # Only include records that haven't reached the 2-hour limit
                if time_remaining.total_seconds() > 0:
                    records_with_countdown.append({
                        'person_id': record.person_id,
                        'arrival_time': record.arrival_time,
                        'time_remaining': time_remaining,
                        'first_name': student.first_name,
                        'last_name': student.last_name,
                        'program_of_study': student.program_of_study,
                        'year_of_study': student.year_of_study,

                    })


        for student in student_records:
            if record.person_id == student.person_id:
                records_with_countdown.append({
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'program_of_study': student.program_of_study,
                    'year_of_study': student.year_of_study,

                })

        else:
            '''Delete records that are older than 2 hours
            #record.delete()
        '''
    for item in records_with_countdown:
        if item not in record_without_duplicates:
            record_without_duplicates.append(item)
    context = {
        'records': record_without_duplicates,
        'students': students_in_attendance,
    }

    return render(request, 'attendance2.html', context)

def delete_old_attendance():
    now = timezone.now()
    cutoff_time = now - timedelta(hours=2)
    Attendance.objects.filter(arrival_time__lt=cutoff_time).delete()


delete_old_attendance()

def display_registered_user(request):
    student_records = Student_record.objects.all()
    return render(request, 'userpage.html', {'students':student_records})


def index(request):
    return render(request, 'index.html')
def scanpage2(request):
    return render(request, 'scanpage2.html')


def scan_qr_code(request):
    if request.method == 'POST':
        # Decode JSON request
        data = json.loads(request.body)
        qr_data = data.get('qr_data')

        # Process the QR data (for example, store it or verify it)
        response_data = {
            'message': f'Successfully received QR code: {qr_data}'
        }

        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'}, status=400)
def scan_qrcode(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Assuming the QR code data is sent as JSON
            user_id = data.get('user_id')  # QR code should encode the user ID
            user = Student_record.objects.get(person_id=user_id)
        except (Student_record.DoesNotExist, KeyError):
            return JsonResponse({'status': 'error', 'message': 'Invalid QR code'}, status=400)

        today = timezone.now().date()
        attendance, created = Attendance.objects.get_or_create(user=user, date=today)

        if attendance.is_checked_in() and not attendance.is_checked_out():
            # Mark check-out
            attendance.check_out_time = timezone.now()
            attendance.save()
            return JsonResponse({'status': 'success', 'message': 'Checked out successfully'})
        elif not attendance.is_checked_in():
            # Mark check-in
            attendance.check_in_time = timezone.now()
            attendance.save()
            return JsonResponse({'status': 'success', 'message': 'Checked in successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Already checked out'}, status=400)

    return render(request, 'scanpage.html')


def scan_window(request):
    print('scan window open ')
    #cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap = cv2.VideoCapture(0)

    cap.set(3, 1280)  # Set width
    cap.set(4, 720)  # Set height

    barcode_data = None  # Store decoded QR code data

    while True:
        success, img = cap.read()
        if not success:
            break

        # Barcode and QR-code reading from live video footage
        for barcode in decode(img):
            barcode_data = barcode.data.decode('utf-8')
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            pts2 = barcode.rect
            # Draw text with decoded data (optional for debugging)
            cv2.putText(img, barcode_data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

            # Stop capturing and release the camera
            cap.release()
            cv2.destroyAllWindows()
            Attendance.objects.create(person_id=barcode_data)

            # Redirect to results page with barcode data
            return redirect('qrcode_results', data=barcode_data)

    cap.release()
    cv2.destroyAllWindows()
    return render(request, 'no_qrcode.html')

def qrcode_results(request, data):
    context = {'barcode_data': data}
    return render(request, 'qrcode_results.html', context)
# from the scan add the scan the list of students in attendance


