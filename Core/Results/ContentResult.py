from Core.Bunny.BunnyVideo import BunnyVideo


class ContentResult:
    def __init__(self, content_obj, status):
        self.content = content_obj  # type:BunnyVideo
        self.status_code = status  # type: int

    def passed(self) -> bool:
        return self.status_code == 200

