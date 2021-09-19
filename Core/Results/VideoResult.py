from typing import List
from Core.Results.ContentResult import ContentResult
from Core.Bunny.BunnyVideo import BunnyVideo


class VideoResult:
    def __init__(self, video):
        self.video = video  # type: BunnyVideo
        self._passed_content = []  # type: List[ContentResult]
        self._failed_content = []  # type: List[ContentResult]

    def add_content_result(self, content_result_obj):
        if content_result_obj.passed():
            self._passed_content.append(content_result_obj)
        else:
            self._failed_content.append(content_result_obj)

    def passed_content(self) -> List[ContentResult]:
        return self._passed_content

    def failed_content(self) -> List[ContentResult]:
        return self._failed_content

    def all_content(self) -> List[ContentResult]:
        return self.passed_content() + self.failed_content()

    def passed(self) -> bool:
        return len(self._failed_content) == 0