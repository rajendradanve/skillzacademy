from django import forms
from courses.models import Category, MainCategory, Course, CourseSchedule

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['main_category', 'friendly_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        main_categories = MainCategory.objects.all()
        friendly_names = [(m_c.id, m_c.get_friendly_name()) for m_c in main_categories]

        self.fields['main_category'].choices = friendly_names
        self.fields['friendly_name'].label = 'Enter Category Name'
        self.fields['friendly_name'].widget.attrs['required'] = 'required'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-dark rounded-0'
