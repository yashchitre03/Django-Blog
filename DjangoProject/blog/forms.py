from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, }),
        }


class ReportForm(forms.Form):
    CHOICES = (
        ('Bug', 'Bug'),
        ('Content', 'Inappropriate content'),
        ('Other', 'Other')
    )

    subject = forms.CharField(label='Subject', max_length=128, strip=True)
    category = forms.ChoiceField(label='Select a category', choices=CHOICES)
    message = forms.CharField(label='Issue', strip=True)
