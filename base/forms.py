from django import forms

from .models import Famili, Product, Composition, ProductMedia

# class PasswordConfirmationForm(forms.Form):
#     password = forms.CharField(widget=forms.PasswordInput)

#     def clean_password(self):
#         password = self.cleaned_data['password']
#         if password != 'tajnehaslo123':
#             raise forms.ValidationError("Niepoprawne hasło.")
#         return password


class FamiliForm(forms.ModelForm):
    class Meta:
        model = Famili
        fields = ['name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['check_prev', 'name', 'rows', 'cols', 'img_width', 'img_height']

class CompositionForm(forms.ModelForm):
    class Meta:
        model = Composition
        fields = ['check_prev', 'name', 'is_change_down_flag', 'phase']
        

class ProductMediaForm(forms.ModelForm):
    class Meta:
        model = ProductMedia
        fields = ['image_none', 'image_true', 'image_false', 'image_other']