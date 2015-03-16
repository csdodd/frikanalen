# Copyright (c) 2012-2013 Benjamin Bruheim <grolgh@gmail.com>
# This file is covered by the LGPLv3 or later, read COPYING for details.
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from fk.models import AsRun
from fk.models import Category
from fk.models import Organization
from fk.models import Scheduleitem
from fk.models import Video
from fk.models import VideoFile


User = get_user_model()


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = (
            "id",
            "video",
            "format",
            "filename",
            "old_filename"
            )


class VideoSerializer(serializers.ModelSerializer):
    editor = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())
    organization = serializers.SlugRelatedField(
        slug_field='name', queryset=Organization.objects.all())
    categories = serializers.SlugRelatedField(
        slug_field='name', many=True, queryset=Category.objects.all())

    class Meta:
        model = Video
        fields = (
            "id",
            "name",
            "header",
            "description",
            "editor",
            "organization",
            "duration",
            #'videofiles',
            "categories",
            "has_tono_records",
            "publish_on_web",
            "is_filler",
            "ref_url",
            )


class ScheduleitemSerializer(serializers.ModelSerializer):
    video = VideoSerializer(required=False, read_only=True)
    video_id = serializers.HyperlinkedRelatedField(
        source="video", view_name="api-video-detail", required=False,
        queryset=Video.objects.all())

    class Meta:
        model = Scheduleitem
        fields = (
            "id",
            "default_name",
            "video_id",
            "video",
            "schedulereason",
            "starttime",
            "duration"
            )


class AsRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsRun


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
