class BunnyVideo:
    def __init__(self):
        self.video_id = None
        self.video_name = None
        self.cdn_hostname = None
        self.library_id = None
        self.collection = None

    def __str__(self):
        return '%s - %s' % (
            self.video_name,
            self.video_id,
        )
