# from django import forms
# from .models import EditdownUserProfile, Photo
# from django.contrib.auth.models import User
# 
# from mezzanine.accounts.forms import ProfileForm
# 
# # class EditdownUserProfile(forms.ModelForm):
# # 
# #     class Meta:
# #         model = EditdownUserProfile
# #         fields = [
# #             'first_name',
# #             'last_name',
# #             # 'email', 
# #             'profile_photo',
# #             'bio'
# #             ]
# #         exclude = ('password1', 'password2', 'date_account_created')
# #         # widgets = {
# #         #     'country': forms.HiddenInput()
# #         # }
# 
# 
# class PhotoUploadModelForm(forms.ModelForm):
# 
#     class Meta:
#         model = Photo
#         fields = ['file']