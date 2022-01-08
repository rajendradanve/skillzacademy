from django import forms
from .models import Category, MainCategory, Course, CourseSchedule


class AddCourse(forms.ModelForm):
    class Meta:
        model = Course
        model2 = CourseSchedule
        fields = ['category', 'title', 'description', 'prerequisite', 'learning_objectives', 'for_whom', 'instructor_info', 'number_of_lectures', 'price']


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
        self.fields['friendly_name'].widget.attrs['minlength'] = 4
        self.fields['friendly_name'].widget.attrs['maxlength'] = 100
        

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-dark rounded-1'


class MainCategoryForm(forms.ModelForm):
    class Meta:
        model = MainCategory
        fields = ['friendly_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['friendly_name'].label = 'Enter Main Category Name'
        self.fields['friendly_name'].widget.attrs['required'] = 'required'
        self.fields['friendly_name'].widget.attrs['minlength'] = 4
        self.fields['friendly_name'].widget.attrs['maxlength'] = 100
        self.fields['friendly_name'].widget.attrs['class'] = 'border-dark rounded-1'


class UpdateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['friendly_name', 'main_category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        main_categories = MainCategory.objects.all()
        friendly_names = [(m_c.id, m_c.get_friendly_name()) for m_c in main_categories]

        self.fields['main_category'].choices = friendly_names
        self.fields['main_category'].label = "Update Main Category"
        self.fields['friendly_name'].label = 'Update Category Name'
        self.fields['friendly_name'].widget.attrs['required'] = 'required'
        self.fields['friendly_name'].widget.attrs['minlength'] = 4
        self.fields['friendly_name'].widget.attrs['maxlength'] = 100

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-dark rounded-1'
