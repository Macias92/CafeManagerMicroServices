from authx.utils import fetch_service_data

from rest_framework.serializers import (
    ModelSerializer,
    CharField,
)
from django.utils.translation import ugettext_lazy as _

from .models import PurchaseOrder


class ListPurchaseOrderSerializer(ModelSerializer):
    status = CharField(source='get_status_display')

    class Meta:
        model = PurchaseOrder
        fields = ["status", "order_number"]


class PurchaseOrderSerializer(ModelSerializer):
    def to_representation(self, instance):
        api_url = self.context['api_url']
        ret = super().to_representation(instance)
        new_items = list()

        for item in ret['items']:
            fetched_items = fetch_service_data(
                item, api_url)
            new_items.append(fetched_items)

        ret['items'] = new_items
        return ret

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
