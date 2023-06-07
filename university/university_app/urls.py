"""library_app URL Configuration."""
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# register our REST views in router object
router.register(r'faculty', views.FacultyViewSet)
router.register(r'teacher', views.TeacherViewSet)
router.register(r'lesson', views.LessonViewSet)
router.register(r'mark', views.MarkViewSet)
router.register(r'hometask', views.HometaskViewSet)
router.register(r'group', views.GroupViewSet)


urlpatterns = [
    path('', views.custom_main, name='homepage'),
    path('profile/', views.profile_page, name='profile'),
    path('about/', views.about_page, name='about'),
    path('contacts/', views.contacts_page, name='contacts'),
    # CATALOG
    path('faculties/', views.FacultyListView.as_view(), name='faculties'),
    path('teachers/', views.TeacherListView.as_view(), name='teachers'),
    path('groups/', views.GroupListView.as_view(), name='groups'),
    path('lessons/', views.LessonListView.as_view(), name='lessons'),
    path('marks/', views.MarkListView.as_view(), name='marks'),
    path('hometasks/', views.HometaskListView.as_view(), name='hometasks'),
    # ENTITIES
    path('faculty/', views.faculty_view, name='faculty'),
    path('teacher/', views.teacher_view, name='teacher'),
    path('lesson/', views.lesson_view, name='lesson'),
    path('mark/', views.mark_view, name='mark'),
    path('hometask/', views.hometask_view, name='hometask'),
    path('group/', views.group_view, name='group'),
    # REST
    path('rest/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # auth
    path('accounts/', include('django.contrib.auth.urls')),
]
