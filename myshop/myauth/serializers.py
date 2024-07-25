from typing import Dict

from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """ Serializer for Profile class """
    avatar = serializers.SerializerMethodField(method_name="get_avatar")

    class Meta:
        model = Profile
        fields = "fullName", "email", "phone", "avatar"

    @staticmethod
    def get_avatar(obj: Profile) -> Dict:
        if obj.avatar:
            return {"src": obj.avatar.url, "alt": obj.avatar.name}
        else:
            return {}
