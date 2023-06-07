"File with consts for university_app."
from os.path import join

# Faculty, Group, (Subject), Teacher, Lesson, (Student), Mark, Hometask

TEMPLATE_MAIN = 'index.html'
TEMPLATE_PROFILE = 'pages/profile.html'
TEMPLATE_ABOUT = 'pages/about.html'
TEMPLATE_CONTACTS = 'pages/contacts.html'

CATALOG = 'catalog'
FACULTIES_CATALOG = join(CATALOG, 'faculties.html')
GROUPS_CATALOG = join(CATALOG, 'groups.html')
TEACHERS_CATALOG = join(CATALOG, 'teachers.html')
LESSONS_CATALOG = join(CATALOG, 'lessons.html')
MARKS_CATALOG = join(CATALOG, 'marks.html')
HOMETASKS_CATALOG = join(CATALOG, 'hometasks.html')
ADD_MARK = join(CATALOG, 'add_mark.html')

ENTITIES = 'entities'
FACULTY_ENTITY = join(ENTITIES, 'faculty.html')
GROUP_ENTITY = join(ENTITIES, 'group.html')
TEACHER_ENTITY = join(ENTITIES, 'teacher.html')
LESSON_ENTITY = join(ENTITIES, 'lesson.html')
MARK_ENTITY = join(ENTITIES, 'mark.html')
HOMETASK_ENTITY = join(ENTITIES, 'hometask.html')

PAGINATE_THRESHOLD = 20

SAFE_METHODS = 'GET', 'HEAD', 'OPTIONS', 'PATCH'
UNSAFE_METHODS = 'POST', 'PUT', 'DELETE'

CHARS_DEFAULT = 50
EMAIL_DEFAULT_LEN = 256


DECIMAL_PLACES = 2
DECIMAL_MAX_DIGITS = 10


MARK_CHOICES = [('', ''), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
PRESENCE_CHOICES = [('', ''), ('Н', 'Н')]
