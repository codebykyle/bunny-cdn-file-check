from Core.Content.BunnyAvailableContent import BunnyAvailableContent


class BunnyHlsContent(BunnyAvailableContent):
    def get_name(self):
        return "HLS"

    def does_match(self, input):
        return input in [
            'hls'
        ]

    def get_url(self, for_video):
        return 'https://%s/%s/playlist.m3u8' % (
            for_video.cdn_hostname,
            for_video.video_id,
        )
