# -*- coding: utf-8 -*-
import logging
from geoapp.settings.base import INSTALLED_APPS, DATABASES, DATABASE_APPS_MAPPING

logger = logging.getLogger('common')
logger.setLevel(logging.INFO)

# logger.info('INSTALLED APPS: {}'.format(INSTALLED_APPS))
# logger.info('CUSTOM APP ROUTER: {}'.format(list(DATABASE_APPS_MAPPING.keys())))

# contrib app
# third-party app
# your custom app


class DatabaseAppsRouter(object):
    """
    A router to control all database operations on models for different
    databases.

    In case an app is not set in settings.DATABASE_APPS_MAPPING, the router
    will fallback to the `default` database.

    Settings example:

    DATABASE_APPS_MAPPING = {'app1': 'db1', 'app2': 'db2'}
    """
    database_apps_mapping = DATABASE_APPS_MAPPING

    def db_for_read(self, model, **hints):
        """"Point all read operations to the specific database."""
        if model._meta.app_label in self.database_apps_mapping:
            return self.database_apps_mapping[model._meta.app_label]
        return None

    def db_for_write(self, model, **hints):
        """Point all write operations to the specific database."""
        if model._meta.app_label in self.database_apps_mapping:
            return self.database_apps_mapping[model._meta.app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation between apps that use the same database."""
        db_obj1 = self.database_apps_mapping.get(obj1._meta.app_label)
        db_obj2 = self.database_apps_mapping.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None

    # for Django 1.4 - Django 1.6
    def allow_syncdb(self, db, model):
        """Make sure that apps only appear in the related database."""
        if db in self.database_apps_mapping.values():
            return self.database_apps_mapping.get(model._meta.app_label) == db
        elif model._meta.app_label in self.database_apps_mapping:
            return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db in self.database_apps_mapping.values():
            return self.database_apps_mapping.get(app_label) == db
        elif app_label in self.database_apps_mapping:
            return False
        return None
