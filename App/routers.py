
class ExternalDatabaseRouter:
	def db_for_read(self, model,):
		if model._meta.app_label == 'App':
			return 'Applications App'
		return None

	def db_for_write(self, model,):
		if model._meta.app_label == 'App':
			return 'Applications App'
		return None

	def allow_relation(self, name, id_number, constituency, location):
		return None

	def allow_migrate(self, db, app_label, model_name=None):
		if app_label == 'App':
			return False
		return None

