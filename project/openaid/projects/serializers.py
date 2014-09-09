from rest_framework import serializers
from ..serializers import TranslatedModelSerializer
from .models import Project, Activity, Markers


class MarkersSerializer(TranslatedModelSerializer):

    class Meta:
        model = Markers


class ProjectSerializer(TranslatedModelSerializer):

    activities = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='activity-detail')

    class Meta:
        model = Project


class ActivitySerializer(TranslatedModelSerializer):

    project = serializers.HyperlinkedRelatedField(read_only=True, view_name='project-detail')

    recipient = serializers.HyperlinkedRelatedField(read_only=True, view_name='recipient-detail')
    channel = serializers.HyperlinkedRelatedField(read_only=True, view_name='channel-detail')
    aid_type = serializers.HyperlinkedRelatedField(read_only=True, view_name='aidtype-detail')
    agency = serializers.HyperlinkedRelatedField(read_only=True, view_name='agency-detail')
    finance_type = serializers.HyperlinkedRelatedField(read_only=True, view_name='financetype-detail')
    # donor = serializers.HyperlinkedRelatedField(read_only=True, view_name='donor-detail')
    sector = serializers.HyperlinkedRelatedField(read_only=True, view_name='sector-detail')

    markers = MarkersSerializer()

    class Meta:
        model = Activity