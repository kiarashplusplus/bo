
class FrontRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['auth', 'contenttypes', 'sessions', 'messages', 'staticfiles']:
            return 'default'
        else:
        	return 'main'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == obj2._state.db:
        	return True
        else:
        	return False

    def allow_migrate(self, db, model):
    	# Only sync default models
    	#WARNING: assumes models are the same for "main"
        if db == 'default':
            return model._meta.app_label in ['auth', 'contenttypes', 'sessions', 'messages', 'staticfiles']
        else:
        	return False
        '''elif model._meta.app_label in ['auth', 'contenttypes', 'sessions', 'messages', 'staticfiles']:
            return False
        return None'''