

class BunnyAvailableContent:
    def get_name(self):
        return "Content"

    def does_match(self, input):
        return True

    def get_url(self, for_video):
        raise Exception("No URL is set for resolution of: %s" % self)

    def __str__(self):
        return '%s' % self.get_name()
