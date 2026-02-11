try:
    from psycopg2 import sql
except ImportError:
    from psycopg import sql
from commentmigrate.backends.base import BaseCommentMigration
from commentmigrate.utils import get_field_comment, get_table_comment


class CommentMigration(BaseCommentMigration):
    comment_sql = sql.SQL('COMMENT ON COLUMN {}.{} IS %s')
    table_comment_sql = sql.SQL('COMMENT ON TABLE {} is %s;')

    def comments_sql(self):
        results = []
        comments_sql = self._get_fields_comments_sql()
        if comments_sql:
            results.extend(comments_sql)
        table_comment = get_table_comment(self.model)
        if table_comment:
            db_table = self.db_table.replace('"', '').split('.')
            if len(db_table) > 1:
                sql_table = sql.Identifier(db_table[0], db_table[1])
            else:
                sql_table = sql.Identifier(self.db_table)
            results.append((
                self.table_comment_sql.format(sql_table),
                [table_comment],
            ))

        return results

    def _get_fields_comments_sql(self):
        comments_sql = []
        for field in self.model._meta.local_fields:
            comment = get_field_comment(field)
            if comment:
                db_table = self.db_table.replace('"', '').split('.')
                if len(db_table) > 1:
                    sql_table = sql.Identifier(db_table[0], db_table[1])
                else:
                    sql_table = sql.Identifier(self.db_table)
                comment_sql = self.comment_sql.format(
                    sql_table,
                    sql.Identifier(field.column)
                )
                comments_sql.append((comment_sql, [comment]))
        return comments_sql
