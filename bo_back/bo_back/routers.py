
back_apps = ['auth', 'contenttypes', 'sessions', 'messages', 'staticfiles', 'sites', 'admin']

class BackRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label in back_apps:
            return 'default'
        else:
        	return 'main'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in back_apps:
            return 'default'
        else:
            return 'main'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == obj2._state.db:
        	return True
        else:
        	return False

    def allow_syncdb(self, db, model):
    	# Only sync default models
    	#WARNING: assumes models are the same for "main"
        if db == 'default':
            return model._meta.app_label in back_apps
        elif model._meta.app_label in back_apps:
            return False
        else:
            return True