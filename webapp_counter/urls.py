from django.urls import path, include
from . views import frequency, result, homepage
urlpatterns = [
    path('', homepage, name='homepage'),
    path('frequency/', frequency, name='frequency-form'),
    path('result/<int:url_id>', result, name='result')
]
