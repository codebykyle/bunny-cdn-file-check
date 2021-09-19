

class BunnyCollection:
    def __init__(self):
        self.collection_name = None
        self.collection_id = None
        self.library_id = None

    def __str__(self):
        return '%s - %s' % (
            self.collection_name,
            self.collection_id,
        )
