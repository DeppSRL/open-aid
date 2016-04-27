from .models import Recipient, Donor, Agency, Channel, FinanceType, AidType, Sector
from ..serializers import TranslatedModelSerializer


class CodeListMeta:
    lookup_field = 'code'

class TreeCodeListMeta(CodeListMeta):
    exclude = ('id', 'lft', 'rght', 'tree_id', 'level')


class RecipientSerializer(TranslatedModelSerializer):

    class Meta(TreeCodeListMeta):
        model = Recipient


class DonorSerializer(TranslatedModelSerializer):

    class Meta(CodeListMeta):
        model = Donor


class AgencySerializer(TranslatedModelSerializer):

    class Meta(CodeListMeta):
        model = Agency
        exclude = ('donor', )


class ChannelSerializer(TranslatedModelSerializer):

    class Meta(TreeCodeListMeta):
        model = Channel


class FinanceTypeSerializer(TranslatedModelSerializer):

    class Meta(TreeCodeListMeta):
        model = FinanceType


class AidTypeSerializer(TranslatedModelSerializer):

    class Meta(TreeCodeListMeta):
        model = AidType


class SectorSerializer(TranslatedModelSerializer):

    class Meta(TreeCodeListMeta):
        model = Sector
