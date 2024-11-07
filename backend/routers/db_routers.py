class BranchRouter:
    def db_for_read(self, model, **hints):
        # Route reads for branch-specific apps
        if model._meta.app_label == 'oshodi':
            return 'oshodi'
        elif model._meta.app_label == 'ojota':
            return 'ojota'
        elif model._meta.app_label == 'custom_admin':
            # Allow reading from all databases
            return ['oshodi', 'ojota', 'default'] 
        return 'default'

    def db_for_write(self, model, **hints):
        # Route writes for branch-specific apps
        if model._meta.app_label == 'oshodi':
            return 'oshodi'
        elif model._meta.app_label == 'ojota':
            return 'ojota'
        elif model._meta.app_label == 'custom_admin':
            # Allow writing to all databases
            return ['oshodi', 'ojota', 'default'] 
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Allow cross-database relations
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Control migrations for each app
        if app_label == 'oshodi':
            return db == 'oshodi'
        elif app_label == 'ojota':
            return db == 'ojota'
        elif app_label == 'custom_admin':
            return db == 'default' 
        return db == 'default'
