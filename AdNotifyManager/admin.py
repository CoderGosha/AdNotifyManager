from django.contrib import admin

# Register your models here.
from AdNotifyManager.models import QueryLink, Node, Subscriber, Goods


class QueryLinkAdmin(admin.ModelAdmin):
    model = QueryLink
    list_per_page = 10  # No of records per page
    list_display = ('query_link_type', 'name', 'node', 'data_expired')
    list_filter = ('node',)
    ordering = ('-data_create',)
    search_fields = ('name',)
    pass


class SubscriberAdmin(admin.ModelAdmin):
    model = Subscriber
    list_per_page = 10  # No of records per page
    list_display = ('name', 'query_link', 'subscriber_channel_type', 'channel_id')
    list_filter = ('name',)
    ordering = ('-data_create',)
    search_fields = ('name',)
    pass


class GoodsAdmin(admin.ModelAdmin):
    model = Goods
    list_per_page = 10  # No of records per page
    list_display = ('name', 'cost', 'locate', 'success')
    list_filter = ('query_link',)
    ordering = ('-data_create',)
    search_fields = ('name',)
    pass


class NodeAdmin(admin.ModelAdmin):
    model = Node
    list_per_page = 10  # No of records per page
    list_display = ('name', 'owner', 'is_active', 'last_connect', 'ip_address', 'request_count' )
    # list_filter = ('owner',)
    ordering = ('-last_connect',)
    search_fields = ('name',)

    def request_count(self, obj):
        return f"{obj.count_request}/{obj.count_request_error}"


admin.site.register(Node, NodeAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(QueryLink, QueryLinkAdmin)
