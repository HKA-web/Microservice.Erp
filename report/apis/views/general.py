from django.apps import apps

from core.apis.viewsets import DevExtremeModelViewSet
from report.apis.serializers import GeneralSerializer


class GeneralViewSet(DevExtremeModelViewSet, ):
    @property
    def model(self):
        return apps.get_model(
            app_label=str(self.kwargs.get('application')),
            model_name=str(self.kwargs.get('model'))
        )

    def get_queryset(self):
        return self.model.objects.all()

    def get_serializer_class(self):
        GeneralSerializer.Meta.model = self.model
        return GeneralSerializer
