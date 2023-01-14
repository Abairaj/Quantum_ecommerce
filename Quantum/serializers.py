# from rest_framework import serializers
# from user.models import * 


# class UsersSerializers(serializers.Serializer):
#     model = users
#     first_name = serializers.CharField(max_length=100)
#     last_name  = serializers.CharField(max_length=100)
#     email      = serializers.EmailField(max_length=100,unique=True) 
#     mobile     = serializers.CharField(max_length=13,unique=True,null=True)
#     gender     = serializers.CharField(max_length=10, choices=GENDER_CHOICES, null=True,blank=False)
#     profile    = serializers.ImageField(upload_to='uploads/users_profile/',blank=True)
#     GSTIN      = serializers.CharField(max_length=15,unique=True,null=True)
#     otps       = serializers.CharField(max_length=10,blank=True,default=0)



#     date_joined     =serializers.DateTimeField(auto_now_add=True)
#     last_login      =serializers.DateTimeField(auto_now_add=True)
#     is_admin        =serializers.BooleanField(default=False)
#     is_staff        =serializers.BooleanField(default=False)
#     is_active       =serializers.BooleanField(default=True)
#     is_verified     =serializers.BooleanField(default=False)
#     otp_verified    =serializers.BooleanField(default=False)
#     is_superadmin   =serializers.BooleanField(default=False)


# class ChangePasswordSerializer(serializers.Serializer):
#     model = users

   