from django.urls import path

from .views import UploadWardrobe, SuggestOutfitView ,RegisterView, LoginView

urlpatterns = [
    path('upload-wardrobe/<int:id>/', UploadWardrobe.as_view(), name='upload_wardrobe'),
    path('upload-wardrobe/', UploadWardrobe.as_view()),
    path('suggest-outfit/', SuggestOutfitView.as_view()),
    path('api/register/', RegisterView.as_view()),
    path('api/login/', LoginView.as_view()),
]