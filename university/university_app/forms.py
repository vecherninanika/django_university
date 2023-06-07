from django.forms import ModelForm, Select
from .models import Mark, Lesson, Student


class AddMarkForm(ModelForm):
    def __init__(self, lesson, *args, **kwargs):
        super(AddMarkForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.filter(
            group__in=lesson.groups.all())
        self.fields['lesson'].queryset = Lesson.objects.filter(id=lesson.id)

    class Meta:
        model = Mark
        fields = ['mark', 'presence', 'student', 'lesson']

        # some design
        widgets = {
            'mark': Select(attrs={'class': 'form-control'}),
            'presence': Select(attrs={'class': 'form-control'}),
            'student': Select(attrs={'class': 'form-control'}),
            'lesson': Select(attrs={'class': 'form-control'})
        }
