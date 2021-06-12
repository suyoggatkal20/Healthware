from django.contrib import auth
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from accounts.views import *
from accounts.views import Abc
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()
router.register('User', UserViewSet, 'User')
router.register('Person', PersonViewSet, 'Person')
router.register('Patient', PatientViewSet, 'Patient')
router.register('Doctor', DoctorViewSet, 'Doctor')
router.register('Address', AddressViewSet, 'Address')
router.register('Phone', PhoneViewSet, 'Phone')
router.register('EmergencyContact',
                EmergencyContactViewSet, 'EmergencyContact')
router.register('Email', EmailViewSet, 'Email')
router.register('Allergies', AllergiesViewSet, 'Allergies')
router.register('PastDiseases', PastDiseasesViewSet, 'PastDiseases')
router.register('Other', OtherViewSet, 'Other')
router.register('Addictions', AddictionsViewSet, 'Addictions')
router.register('Weight', WeightViewSet, 'Weight')
router.register('Height', HeightViewSet, 'Height')
router.register('Cholesterol', CholesterolViewSet, 'Cholesterol')
router.register('BloodPressure', BloodPressureViewSet, 'BloodPressure')
router.register('Glocose', GlocoseViewSet, 'Glocose')
router.register('Rating', RatingViewSet, 'Rating')
router.register('Break', BreakViewSet, 'Break')
# router.register('Appointment', AppointmentViewSet, 'Appointment')
router.register('Prescription', PrescriptionViewSet, 'Prescription')
router.register('MedicineDeatils',
                MedicineDetailsViewSet, 'MedicineDeatils')
urlpatterns = [
    path('', include(router.urls)),
    path('tables', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create_doctor/', CreateDoctor.as_view()),
    path('create_patient/', CreatePatient.as_view()),
    path('VerifyEmail/', VerifyEmail.as_view()),
    
    
]
