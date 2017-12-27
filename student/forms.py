from django import forms
from .models import Student
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        # self.helper.layout.append(Submit('save', 'save'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout.append(Submit('submit_change', 'Submit', css_class="btn-primary"))
        self.helper.layout.append(HTML('<a class="btn btn-primary" href={% url "student_home" %}>Reset</a>'))

    # Verify IC number is in XXXXXXXXXX format
    def clean_icnum(self):
        data = self.cleaned_data['icnum']
        # if Student.objects.filter(icnum=data):
        #     raise forms.ValidationError(data + " is already exist!") 
        # elif len(data) is not 12:
        if len(data) is not 12:
            raise forms.ValidationError("IC must be 12 number characters long!")
        elif not data.isnumeric():
            raise forms.ValidationError("IC must be all number!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

    class Meta:
        model = Student
        fields = ('icnum', 'name', 'course',)


class SearchForm(forms.Form):
    search = forms.CharField(label="Please Enter a Keyword")
    select_buttons = forms.ChoiceField(
        label='Select a Field to Lookup',
        choices = (
            ('name', "Name"), 
            ('icnum', "ID/IC Number"),
            ('course', "Course")
        ),
        widget = forms.Select,
        initial = 'name',
    )
    # Uni-form
    helper = FormHelper()
    # helper.form_class = 'form-inline'
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('search', css_class='input-xlarge'),
        Field('select_buttons', css_class='input-xlarge'),
        FormActions(
            Submit('submit_change', 'Search', css_class="btn-primary"),
            # Submit('cancel', 'Reset'),
            HTML('<a class="btn btn-warning" href={% url "student_home" %}>Reset</a>'),
        )
    )



class MessageForm(forms.Form):
    text_input = forms.CharField()

    textarea = forms.CharField(
        widget = forms.Textarea(),
    )

    radio_buttons = forms.ChoiceField(
        choices = (
            ('option_one', "Option one is this and that be sure to include why it's great"), 
            ('option_two', "Option two can is something else and selecting it will deselect option one")
        ),
        widget = forms.RadioSelect,
        initial = 'option_two',
    )

    checkboxes = forms.MultipleChoiceField(
        choices = (
            ('option_one', "Option one is this and that be sure to include why it's great"), 
            ('option_two', 'Option two can also be checked and included in form results'),
            ('option_three', 'Option three can yes, you guessed it also be checked and included in form results')
        ),
        initial = 'option_one',
        widget = forms.CheckboxSelectMultiple,
        help_text = "<strong>Note:</strong> Labels surround all the options for much larger click areas and a more usable form.",
    )

    appended_text = forms.CharField(
        help_text = "Here's more help text"
    )

    prepended_text = forms.CharField()

    prepended_text_two = forms.CharField()

    multicolon_select = forms.MultipleChoiceField(
        choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')),
    )

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('text_input', css_class='input-xlarge'),
        Field('textarea', rows="3", css_class='input-xlarge'),
        'radio_buttons',
        Field('checkboxes', style="background: #FAFAFA; padding: 10px;"),
        AppendedText('appended_text', '.00'),
        PrependedText('prepended_text', '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
        PrependedText('prepended_text_two', '@'),
        'multicolon_select',
        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
        )
    )