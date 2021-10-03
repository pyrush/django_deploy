from django.urls import path

from . import views


app_name = "image"

urlpatterns = [
    path("upload/",
         views.UploadImage.as_view(),
         name="upload_image_url"
         ),

    path("celery_test/",
         views.test,
         name="celery_test_url"
         )
]
