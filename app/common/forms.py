from datetime import date
from pathlib import Path

from django import forms
from django.core.files.storage import default_storage

from .functions import get_extensions


class Form(forms.ModelForm):
    images_delete = forms.CharField(required=False, widget=forms.HiddenInput)
    images_upload = forms.FileField(required=False)
    images_upload.widget.attrs['multiple'] = True

    def clean(self):
        cd = super().clean()
        if self.errors:
            return cd
        cd['images'] = list(filter(None, cd['images'].split('\r\n')))
        self.xclean_images_delete()
        self.xclean_images_upload()
        cd['images'] = '\r\n'.join(cd['images'])
        return cd

    def delete_image(self, i):
        default_storage.delete(self.cleaned_data['images'][i])
        del self.cleaned_data['images'][i]

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        if instance.images:
            instance.images_list = instance.images.split('\r\n')
        return instance

    def upload_image(self, image):
        converter = {
            'jpeg/jpg/jpe/jfif': 'jpg',
            'png': 'png',
        }
        ext = converter.get(get_extensions(image.temporary_file_path()))
        if not ext:
            raise forms.ValidationError({'images_upload': 'Загружать можно только JPEG или PNG.'}, code='invalid')
        name = f'{date.today().strftime(self.UPLOAD_TO)}{Path(image.name).with_suffix(f'.{ext}')}'
        # The actual name of the stored file will be returned.
        name = default_storage.save(name, image)
        self.cleaned_data['images'] += [name]
        return name

    def xclean_images_delete(self):
        ids = self.cleaned_data.get('images_delete')
        if not ids:
            return None
        # sorted(reverse=True) для удаления элементов в обратном порядке.
        indexes = sorted(map(int, ids.split(',')), reverse=True)
        for i in indexes:
            self.delete_image(i)

    def xclean_images_upload(self):
        for image in self.files.getlist('images_upload'):
            self.upload_image(image)
