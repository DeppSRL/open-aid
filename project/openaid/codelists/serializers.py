from .models import Recipient, Donor, Agency, Channel, FinanceType, AidType, Sector
from ..serializers import TranslatedModelSerializer


class RecipientSerializer(TranslatedModelSerializer):

    class Meta:
        model = Recipient


class DonorSerializer(TranslatedModelSerializer):

    class Meta:
        model = Donor


class AgencySerializer(TranslatedModelSerializer):

    class Meta:
        model = Agency


class ChannelSerializer(TranslatedModelSerializer):

    class Meta:
        model = Channel


class FinanceTypeSerializer(TranslatedModelSerializer):

    class Meta:
        model = FinanceType


class AidTypeSerializer(TranslatedModelSerializer):

    class Meta:
        model = AidType


class SectorSerializer(TranslatedModelSerializer):

    class Meta:
        model = Sector
