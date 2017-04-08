class DBRouter(object):
    def db_for_read(self, model, **kwargs):
        if model._meta.model_name in ['category','forum','torrents','vers']:
            return 'tor'
        elif model._meta.model_name == 'contents':
            return 'content'
        return None
    def db_for_write(self, model, **kwargs):
        if model._meta.model_name in ['category','forum','torrents','vers']:
            return 'tor'
        elif model._meta.model_name == 'contents':
            return 'content'
        return None
