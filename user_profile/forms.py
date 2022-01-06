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
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-dark rounded-0'
            if field == 'friendly_name':
                self.fields[field].label = 'Enter Category Name'
                