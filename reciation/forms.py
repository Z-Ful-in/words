"""forms.py
This file contains the forms for the recitation app."""

from django import forms
from .models import Word

# Create a form for the Word model

class ShowWordForm(forms.ModelForm):
    word=forms.CharField(max_length=100)
    meaning=forms.CharField(max_length=100)
    example=forms.CharField(max_length=100, required=False)

    def clean_word(self):
        word=self.cleaned_data['word']
        exist = Word.objects.filter(word=word)
        if exist:
            raise forms.ValidationError('This word already exists')
        return word

    def __str__(self):
        return self.word
    class Meta:
        model=Word
        fields=['word', 'meaning', 'example']
    