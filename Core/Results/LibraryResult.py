from typing import List
from Core.Results.VideoResult import VideoResult

class LibraryResult:
    def __init__(self, successful_results=None, unsuccessful_results=None, checked_resolutions=None):
        self._successful_results = successful_results if successful_results else []  # type: List[VideoResult]
        self._unsuccessful_results = unsuccessful_results if unsuccessful_results else []  # type: List[VideoResult]
        self.checked_content = checked_resolutions if checked_resolutions else []

    def add_result(self, video, was_successful):
        if was_successful:
            self._successful_results.append(video)
        else:
            self._unsuccessful_results.append(video)

    def get_successful_results(self) -> List[VideoResult]:
        return self._successful_results

    def get_unsuccessful_results(self) -> List[VideoResult]:
        return self._unsuccessful_results

    def get_all_results(self) -> List[VideoResult]:
        return self.get_successful_results() + self.get_unsuccessful_results()

    def __add__(self, other):
        return LibraryResult(
            successful_results=self.get_successful_results() + other.get_successful_results(),
            unsuccessful_results=self.get_unsuccessful_results() + other.get_unsuccessful_results(),
            checked_resolutions=self.checked_content
        )
