from rest_framework import serializers
from ..serializers import TranslatedModelSerializer
from .models import Project, Activity, Markers


class MarkersSerializer(TranslatedModelSerializer):

    class Meta:
        model = Markers
        fields = (
            'biodiversity', 'climate_adaptation', 'climate_mitigation', 'desertification',
            'environment', 'gender', 'pd_gg', 'trade', )


class ProjectSerializer(TranslatedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='project-detail')
    activities = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='activity-detail')

    class Meta:
        model = Project


class ActivitySerializer(TranslatedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='activity-detail')
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


class ProjectDetailSerializer(TranslatedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='project-detail')
    activities = ActivitySerializer(many=True)

    class Meta:
        model = Project