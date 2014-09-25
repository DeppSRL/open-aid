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
    recipient = serializers.HyperlinkedRelatedField(read_only=True, view_name='recipient-detail', lookup_field='code')
    activities = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='activity-detail')

    class Meta:
        model = Project
        fields = ('crsid', 'url', 'start_year', 'end_year', 'recipient', 'activities')


class ActivitySerializer(TranslatedModelSerializer):
    project = serializers.HyperlinkedRelatedField(read_only=True, view_name='project-detail')

    recipient = serializers.HyperlinkedRelatedField(read_only=True, view_name='recipient-detail', lookup_field='code')
    channel = serializers.HyperlinkedRelatedField(read_only=True, view_name='channel-detail', lookup_field='code')
    aid_type = serializers.HyperlinkedRelatedField(read_only=True, view_name='aidtype-detail', lookup_field='code')
    agency = serializers.HyperlinkedRelatedField(read_only=True, view_name='agency-detail', lookup_field='code')
    finance_type = serializers.HyperlinkedRelatedField(read_only=True, view_name='financetype-detail', lookup_field='code')
    # donor = serializers.HyperlinkedRelatedField(read_only=True, view_name='donor-detail')
    sector = serializers.HyperlinkedRelatedField(read_only=True, view_name='sector-detail', lookup_field='code')

    markers = MarkersSerializer()

    class Meta:
        model = Activity


class ProjectDetailSerializer(TranslatedModelSerializer):
    recipient = serializers.HyperlinkedRelatedField(read_only=True, view_name='recipient-detail', lookup_field='code')
    activities = ActivitySerializer(many=True)

    class Meta:
        model = Project
        fields = ('crsid', 'url', 'start_year', 'end_year', 'recipient', 'activities')