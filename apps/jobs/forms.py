from django import forms
from .models import Job, Application


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'company', 'location', 'salary', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'full_name', 'father_name', 'email', 'contact_number',
            'date_of_birth', 'address', 'resume', 'cover_letter',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'cover_letter': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Write your cover letter (max 250 words)...'
            }),
        }

    def clean_cover_letter(self):
        text = self.cleaned_data['cover_letter']
        word_count = len(text.split())
        if word_count > 250:
            raise forms.ValidationError(
                f"Cover letter must be under 250 words. You wrote {word_count} words."
            )
        return text