from django import forms
from django.forms import TextInput
from .models import SearchTerm


class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchTerm
        fields = ['search_term']
        widgets = {
            'search_term': TextInput(
                attrs={'class': 'form-control', 'list': 'src', 'placeholder': 'Search any product here'
                       })
        }
        labels = {'search_term': '',
                  }

    def clean_search_term(self):
        query = self.cleaned_data.get('search_term')
        if not query:
            raise forms.ValidationError('Please Enter something')


class ContactForm(forms.Form):
    contact_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Your Name'}),
                                   required=True)
    contact_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Your Email'}),
                                     required=True)
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder': 'Your Feedback'}),
                              required=True,
                              )
