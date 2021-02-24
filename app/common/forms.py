from datetime import date

from django import forms
from django.core.files.storage import default_storage


class DocumentForm(forms.ModelForm):
    images = forms.CharField(required=False, widget=forms.Textarea)
    images_delete = forms.CharField(required=False, widget=forms.HiddenInput)
    images_upload = forms.FileField(required=False)
    images_upload.widget.attrs['multiple'] = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.initial |= self.instance.document
            self.initial['images'] = '\r\n'.join(self.instance.images)

    def clean(self):
        cd = super().clean()
        if self.errors:
            return cd
        self.xclean_images_delete()
        self.xclean_images_upload()
        return cd

    def clean_images(self):
        self.cleaned_data['images'] = list(filter(None, self.cleaned_data['images'].split('\r\n')))
        return self.cleaned_data['images']

    def delete_image(self, i):
        default_storage.delete(self.cleaned_data['images'][i])
        del self.cleaned_data['images'][i]

    def save(self, *args, **kwargs):
        for k, v in self.cleaned_data.items():
            # В форме могут быть дополнительные поля.
            if hasattr(self.instance, k):
                setattr(self.instance, k, v)
                if type(v) in [bool, int, list, str]:
                    if v:
                        self.instance.document[k] = v
                    elif k in self.instance.document:
                        del self.instance.document[k]
        return super().save(*args, **kwargs)

    def upload_image(self, image):
        name = f'{date.today().strftime(self.UPLOAD_TO)}{image.name}'
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
