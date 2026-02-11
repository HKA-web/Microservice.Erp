# example :
# DATABASES.SQLSERVER:
#     ENGINE: library.pyodbc
#     NAME: master
#     USER: sa
#     PASSWORD: PASSWORD
#     HOST: 'np:\\192.168.6.51\pipe\sql\query'
#     OPTIONS:
#       driver: 'SQL Server'
#       version: 2000
#     ATOMIC_REQUESTS: false
#     VERSION_CHECK: false
#
# from django.db import connections
#
# connections['SIDIA']
# connections['SIDIA'].ensure_
