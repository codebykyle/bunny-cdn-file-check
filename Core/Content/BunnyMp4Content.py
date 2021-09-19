from Core.Content.BunnyAvailableContent import BunnyAvailableContent


class BunnyMp4Content(BunnyAvailableContent):
    def __init__(self, resolution):
        self.resolution = resolution
        super().__init__()

    def get_name(self):
        return self.resolution + "p"

    def does_match(self, input):
        return input in [
            self.resolution + 'p',
            self.resolution
        ]

    def get_url(self, for_video):
        return 'https://%s/%s/play_%sp.mp4' % (
            for_video.cdn_hostname,
            for_video.video_id,
            self.resolution
        )
