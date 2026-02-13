import json
import logging
import re as regex
import time

from django.db import connections
from django.db.utils import (DEFAULT_DB_ALIAS as DatabaseAlias, )
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.utils import lodash

logger = logging.getLogger(__name__)

'''
import logging
from library.pyodbc.apis import DevExtremeQueryViewSet
logger = logging.getLogger(__name__)

class OdbcViewSet(DevExtremeQueryViewSet, ):
permission_classes = []
    primary_key = 'po_id'
    query = '
SELECT * FROM ( SELECT
    column,
    ........
    ....
'''
class DevExtremeQueryViewSet(ViewSet, ):
    query = None
    table_name = None
    primary_key = 'ids'

    def connection(self, request, ):
        return connections[request.query_params.get('connection', DatabaseAlias)]

    def clean_row(self, columns, row, ):
        return {col: val.strip() if isinstance(val, str) else val for col, val in zip(columns, row)}

    def list(self, request, *args, **kwargs):
        start_time = time.time()
        params = request.query_params
        require_total_count = params.get('requireTotalCount', 'true').lower() in ('true',)
        require_group_count = params.get('requireGroupCount', 'false').lower() in ('true',)
        is_counter = params.get('isCountQuery', 'false').lower() in ('true',)
        skip = int(params.get('skip', 0))
        take = int(params.get('take', 20))
        fields = [field.strip() for field in regex.split(r'[,\s;]+', params.get('field')) if field.strip()] if params.get('field') else []
        sort = self._parse_json_param(params.get('sort', '[]'))
        group = self._parse_json_param(params.get('group', '[]'))
        filtered = self._parse_json_param(params.get('filter', '[]'))
        total_summary = self._parse_json_param(params.get('totalSummary', '[]'))
        final_query, count_query, database_type = self._build_query(
            skip=skip,
            take=take,
            sort=sort,
            group=group,
            filtered=filtered,
            is_counter=is_counter,
            request=request,
        )
        final_query = self._clean_double_where(final_query, )
        if count_query:
            count_query = self._clean_double_where(count_query, )
        self.connection(request, ).ensure_connection()
        with self.connection(request, ).cursor() as cursor:
            logger.debug(f'Executing Query ({database_type}): {final_query}')
            cursor.execute(final_query)
            columns = [column[0].lower() for column in cursor.description]
            data = [self.clean_row(columns, row) for row in cursor.fetchall()]
            total_count = None
            if require_total_count and count_query:
                logger.debug(f'Executing Count Query ({database_type}): {count_query}')
                cursor.execute(count_query)
                total_count = cursor.fetchone()[0]
        response_data = {
            'skip': skip,
            'take': take,
        }
        if total_count is not None:
            response_data['totalCount'] = total_count
        if require_group_count and group:
            response_data['groupCount'] = self._get_group_count(group, filtered, )
        if total_summary:
            response_data['summary'] = self._calculate_summary(total_summary, filtered, )
        end_time = time.time()
        response_data['execution'] = round(end_time - start_time, 4)
        response_data['data'] = data = lodash.map(data, lambda item: lodash.pick(item, *fields)) if fields else data
        return Response(response_data, )

    def _clean_double_where(self, query):
        if not query:
            return query
        cleaned = regex.sub(r'WHERE\s+WHERE', 'WHERE', query, flags=regex.IGNORECASE)
        cleaned = regex.sub(r'WHERE\s+AND', 'WHERE', cleaned, flags=regex.IGNORECASE)
        cleaned = regex.sub(r'WHERE\s+OR', 'WHERE', cleaned, flags=regex.IGNORECASE)
        return cleaned

    def _parse_json_param(self, param):
        try:
            return json.loads(param)
        except (json.JSONDecodeError, TypeError):
            return [] if param in ('[]',) else param

    def _build_where_clause(self, filtered):
        if not filtered:
            return ''
        condition = self._build_filter(filtered) if isinstance(filtered, list) else filtered
        return f'''WHERE {condition}'''

    def _build_filter(self, filters):
        if not filters:
            return '\'ERPro\' IN (\'ERPro\')'
        if len(filters) == 3 and isinstance(filters[0], str) and isinstance(filters[1], str):
            return self._build_simple_condition(filters)
        if len(filters) == 3:
            left = self._build_filter(filters[0]) if isinstance(filters[0], list) else filters[0]
            operator = filters[1].upper()
            right = self._build_filter(filters[2]) if isinstance(filters[2], list) else filters[2]
            return f'''({left} {operator} {right})'''
        return '\'ERPro\' IN (\'ERPro\')'

    def _build_simple_condition(self, current_filter):
        selector, operator, value = current_filter
        operator_query = {
            '=': '=', '<>': '!=', '>': '>', '>=': '>=', '<': '<', '<=': '<=',
            'contains': 'LIKE', 'notcontains': 'NOT LIKE',
            'startswith': 'LIKE', 'endswith': 'LIKE', 'in': 'IN', 'notin': 'NOT IN'
        }.get(operator, '=')
        if operator in ('contains',):
            value = f'%{value}%'
        elif operator in ('startswith',):
            value = f'{value}%'
        elif operator in ('endswith',):
            value = f'%{value}'
        if operator in ('in', 'notin',) and isinstance(value, list):
            value = f'''({', '.join([f''' '{val}' '''.strip() if isinstance(val, str) else str(val) for val in value])})'''
        elif isinstance(value, str) and not (value.startswith('\'') and value.endswith('\'')):
            value = f''' '{value}' '''.strip()
        return f'''{selector} {operator_query} {value}'''

    def _build_query(self, skip, take, sort, group, filtered, is_counter, request, ):
        base_query = self.query.strip()
        base_query = self._remove_trailing_where(base_query, )
        where_clause = self._build_where_clause(filtered, )
        if where_clause:
            clean_where = where_clause.replace('WHERE', '').strip()
            if self._is_complex_query(base_query, ):
                base_query = f'''SELECT * FROM ({base_query}) AS base_wrapper'''
                base_query += f''' WHERE {clean_where}'''
            else:
                has_where, existing_condition = self._extract_outer_where_condition(base_query, )
                if has_where and existing_condition:
                    base_query = base_query.replace(
                        f'''WHERE {existing_condition}''',
                        f'''WHERE ({existing_condition}) AND ({clean_where})''',
                        1
                    )
                elif has_where:
                    base_query += f''' AND ({clean_where})'''
                else:
                    base_query += f''' WHERE {clean_where}'''
        if is_counter:
            return f'''SELECT COUNT(*) FROM ({base_query}) AS counter''', ''
        if group:
            base_query += f''' GROUP BY {', '.join([item['selector'] for item in group])}'''
        order_query = self._build_order_by(sort, )
        count_query = self._build_counter(where_clause, )
        database_type = self._detect_db_type(request, )
        if take < 0:
            return base_query, count_query, database_type
        apply_pagination = {
            'postgresql': self._apply_postgresql_pagination,
            'microsoft:new': self._apply_sqlserver_pagination,
            'microsoft:2000': self._apply_sqlserver_older_pagination
        }.get(database_type, self._apply_postgresql_pagination)
        final_query = apply_pagination(base_query, skip, take, order_query, bool(order_query), )
        return final_query, count_query, database_type

    def _remove_trailing_where(self, query, ):
        query = query.strip()
        pattern = r'\bWHERE\b\s*$'
        return regex.sub(pattern, '', query, flags=regex.IGNORECASE).strip()

    def _is_complex_query(self, query, ):
        upper_query = query.upper()
        for pattern in [
            r'SELECT.*SELECT',
            r'CASE.*WHEN',
            r'FROM.*\(SELECT',
            r'WHERE.*\(SELECT',
            r'JOIN.*\(SELECT',
        ]:
            if regex.search(pattern, upper_query, regex.IGNORECASE | regex.DOTALL):
                return True
        return False

    def _extract_outer_where_condition(self, query, ):
        upper_query = query.upper()
        nesting = 0
        for loop, char in enumerate(upper_query):
            if char in ('(',):
                nesting += 1
            elif char in (')',):
                nesting -= 1
            elif char in ('W',) and upper_query[loop:loop + 5] in ('WHERE',) and nesting in (0,) and (loop in (0,) or not upper_query[loop - 1].isalnum()) and (loop + 5 in (len(upper_query),) or not upper_query[loop + 5].isalnum()):
                after_where = query[loop + 5:].strip()
                end_pattern = r'^\s*(.*?)(?:\s+(?:GROUP BY|ORDER BY|HAVING|LIMIT|OFFSET|$))'
                match = regex.search(end_pattern, after_where, regex.IGNORECASE | regex.DOTALL)
                if match:
                    condition = match.group(1).strip()
                    return True, condition
                else:
                    return True, after_where
        return False, None

    def _detect_db_type(self, request, ):
        connection_params = self.connection(request, ).get_connection_params()
        if 'version' in connection_params:
            return f'''{self.connection(request, ).vendor}:{connection_params.get('version')}'''
        try:
            if self.connection(request, ).vendor in ('microsoft',):
                self.connection(request, ).ensure_connection()
                with self.connection(request, ).cursor() as cursor:
                    cursor.execute('SELECT @@VERSION')
                    if any(version in cursor.fetchone()[0].upper() for version in ['2000', '2005', '2008']):
                        return f'''{self.connection(request, ).vendor}:2000'''
                    return f'''{self.connection(request, ).vendor}:new'''
        except (Exception,) as e:
            pass
        return 'postgresql'

    def _build_order_by(self, sorts, ):
        if not sorts:
            return ''
        clauses = []
        for sort in sorts:
            if isinstance(sort, dict) and 'selector' in sort:
                direction = 'DESC' if sort.get('desc') else 'ASC'
                clauses.append(f'''{sort['selector']} {direction}''')
        if clauses:
            return f'''ORDER BY {', '.join(clauses)}'''
        return ''

    def _apply_postgresql_pagination(self, query, skip, take, order_by, has_order, ):
        order = order_by if has_order else f'''ORDER BY {self.primary_key}'''
        return f'''{query} {order} LIMIT {take} OFFSET {skip}'''

    def _apply_sqlserver_pagination(self, query, skip, take, order_by, has_order, ):
        order = order_by if has_order else f'''ORDER BY {self.primary_key}'''
        return f'''{query} {order} OFFSET {skip} ROWS FETCH NEXT {take} ROWS ONLY'''

    def _apply_sqlserver_older_pagination(self, query, skip, take, order_by, has_order, ):
        order = order_by if has_order else f'''ORDER BY {self.primary_key}'''
        if skip in (0,):
            return f'''SELECT TOP {take} * FROM ({query}) AS take {order}'''
        return f'''
            SELECT TOP {take} * FROM ({query}) AS take
            WHERE {self.primary_key} NOT IN (
                SELECT TOP {skip} {self.primary_key} FROM ({query}) AS skip {order}
            ) {order}
        '''

    def _build_counter(self, where_clause, ):
        base_query = self.query.strip()
        base_query = self._remove_trailing_where(base_query)
        if where_clause:
            clean_where = where_clause.replace('WHERE', '').strip()
            if self._is_complex_query(base_query):
                return f'''SELECT COUNT(*) FROM ( SELECT * FROM ({base_query}) AS count_wrapper ) AS final_counter WHERE {clean_where}'''
            else:
                has_where, existing_condition = self._extract_outer_where_condition(base_query)
                if has_where and existing_condition:
                    modified_query = base_query.replace(
                        f'''WHERE {existing_condition}''',
                        f'''WHERE ({existing_condition}) AND ({clean_where})''',
                        1,
                    )
                    return f'''SELECT COUNT(*) FROM ({modified_query}) AS counter'''
                elif has_where:
                    return f'''SELECT COUNT(*) FROM ({base_query} AND {clean_where}) AS counter'''
                else:
                    return f'''SELECT COUNT(*) FROM ({base_query}) AS counter WHERE {clean_where}'''
        return f'''SELECT COUNT(*) FROM ({base_query}) AS counter'''

    def _get_group_count(self, group_list, filtered):
        return 0

    def _calculate_summary(self, summary_list, filtered):
        return {}

    def _escape_sql_string(self, value, ):
        return value.replace('\'', '\'\'')

    def _sql_value(self, value, ):
        if value is None:
            return 'NULL'
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            val = value.strip()
            if val.upper() in ('GETDATE()', 'CURRENT_TIMESTAMP'):
                return val
            return '\'' + self._escape_sql_string(val, ) + '\''
        return '\'' + self._escape_sql_string(str(value)) + '\''

    def data(self, request, ):
        if isinstance(request.data, QueryDict):
            return request.data.dict()
        return request.data if bool(request.data) else request.query_params.dict()

    def create(self, request, *args, **kwargs):
        data = self.data(request)
        if not len(data):
            raise ValueError('Parameter data is required')
        sql = 'INSERT INTO ' + self.table_name + ' (' + ', '.join(list(data[0].keys())) + ')\n'
        selects = []
        for row in data if isinstance(data, list) else [data]:
            values = [self._sql_value(row[column]) for column in row.keys()]
            selects.append('SELECT ' + ', '.join(values))
        sql += '\nUNION ALL\n'.join(selects)
        return Response({'status': 'ok'})

    def update(self, request, *args, **kwargs):
        params = request.query_params
        return Response({'status': 'ok'})

    def destroy(self, request, *args, **kwargs):
        params = request.query_params
        return Response({'status': 'ok'})
