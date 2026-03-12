from netbox.views import generic
from utilities.views import register_model_view

from . import filtersets, forms, models, tables


@register_model_view(models.Proxy)
class ProxyView(generic.ObjectView):
    queryset = models.Proxy.objects.all()


@register_model_view(models.Proxy, "list", path="")
class ProxyListView(generic.ObjectListView):
    queryset = models.Proxy.objects.all()
    table = tables.ProxyTable
    filterset = filtersets.ProxyFilterSet
    filterset_form = forms.ProxyFilterForm


@register_model_view(models.Proxy, "add")
class ProxyEditView(generic.ObjectEditView):
    queryset = models.Proxy.objects.all()
    form = forms.ProxyForm


@register_model_view(models.Proxy, "delete")
class ProxyDeleteView(generic.ObjectDeleteView):
    queryset = models.Proxy.objects.all()


@register_model_view(models.Proxy, "bulk_import")
class ProxyBulkImportView(generic.BulkImportView):
    queryset = models.Proxy.objects.all()
    model_form = forms.ProxyImportForm


@register_model_view(models.Proxy, "bulk_edit")
class ProxyBulkEditView(generic.BulkEditView):
    queryset = models.Proxy.objects.all()
    filterset = filtersets.ProxyFilterSet
    table = tables.ProxyTable
    form = forms.ProxyForm


@register_model_view(models.Proxy, "bulk_delete")
class ProxyBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Proxy.objects.all()
    filterset = filtersets.ProxyFilterSet
    table = tables.ProxyTable
