from rest_framework import serializers

from AdNotifyManager.models import Goods, QueryLink


class GoodsRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ['name', 'cost', 'description', 'locate', 'query_link', 'external_id', 'goods_url']
        extra_kwargs = {'description': {'required': False,
                                        'allow_blank': True},
                        'external_id': {'required': True,
                                        'allow_blank': False},
                        'goods_url': {'required': True,
                                      'allow_blank': False},
                        }

    def create(self, validated_data):
        return Goods.objects.create(**validated_data)


class QueryLinkItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryLink
        fields = ['id', 'query_link_type', 'url', 'filter_locate', 'name']
