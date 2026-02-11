import logging

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views import View

logger = logging.getLogger(__name__)


class EmptyView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = [
        'empty.view_empty',
    ]

    def get(self, request):
        return render(request, 'empty/empty/index.html', dict())
