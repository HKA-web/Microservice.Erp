# -*- coding: utf-8 -*-

from maintenancemode.core import get_maintenance_mode


def maintenance_mode(request):
    return {"maintenance_mode": get_maintenance_mode()}
