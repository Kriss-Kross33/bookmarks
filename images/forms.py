from django import forms
from django.utils.text import slugify
from django.core.files.base import ContentFile

from .models import Image
from urllib import request

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The URL does not match valid image' \
        ' extensions')
        return url

    def save(self, force_insert=False, force_update=False, commit=False):
        # create a new image instance
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        # download the image from the given url
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()
        return image