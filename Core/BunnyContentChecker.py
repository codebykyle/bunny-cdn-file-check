from Core.Bunny.BunnyApi import BunnyAPI
from Core.Results.LibraryResult import LibraryResult
from Core.Output import output
from Core.Colors import Colors
from Core.Results import ContentResult, VideoResult
import requests


class BunnyContentChecker:
    def __init__(self, library_id, api_key, hostname, referer):
        self.library_id = library_id
        self.api_key = api_key
        self.cdn_hostname = hostname
        self.referer = referer

        self.bunny_api = BunnyAPI(
            self.library_id,
            self.api_key,
            self.cdn_hostname
        )

        self.content_to_check = []  # A list of strings, eg: 720p, 1080p, hls, etc
        self.available_content_types = []  # Available content we can parse

        self._cached_content_objs = None

    def register_content_type(self, content_type):
        self.available_content_types.append(content_type)

    def add_content_to_check(self, content_string):
        self.content_to_check.append(content_string)

    def get_content_to_check(self):
        return self.content_to_check

    def set_content_to_check(self, contents):
        self.content_to_check = contents

    def check_all_videos(self):
        results = LibraryResult()
        results.checked_content = self.get_content_check_objects()

        # First check the results of all the videos attached to the library itself
        results += self.check_videos(self.bunny_api.get_library_videos())

        # Then check all the collections & their videos
        collections = self.bunny_api.get_library_collections()

        for collection in collections:
            results += self.check_videos(self.bunny_api.get_library_videos(collection))

        return results

    def check_videos(self, videos):
        check_results = LibraryResult()

        for video in videos:
            video_results = self.check_video(video)

            check_results.add_result(
                video_results,
                video_results.passed()
            )

        return check_results

    def check_video(self, bunny_video):
        output(Colors.OKCYAN + "Checking: %s" % bunny_video)
        video_result = VideoResult(bunny_video)

        for check_obj in self.get_content_check_objects():
            content_url = check_obj.get_url(for_video=bunny_video)

            # Do a get request to the file and note down the HTTP status code for filtering later
            # We can do some HEAD requests to save bandwidth, here.
            web_result = requests.head(
                content_url,
                headers=self.get_headers()
            )

            if web_result.status_code == 200:
                output(Colors.OKGREEN + '\t ✓ ' + str(check_obj).ljust(5) + Colors.ENDC)
            else:
                output(Colors.FAIL + '\t ✕ ' + str(check_obj).ljust(5) + " (%s)" % web_result.status_code + Colors.ENDC)

            # Add the results for the content test to the result data-set
            video_result.add_content_result(
                ContentResult(
                    check_obj,
                    web_result.status_code
                )
            )

        if video_result.passed():
            output(Colors.OKGREEN + Colors.BOLD + "✓ Video Checks Passed" + Colors.ENDC)
        else:
            output(Colors.FAIL + Colors.BOLD + "✕ Video Checks Failed" + Colors.ENDC)

        output("")

        return video_result

    def get_headers(self):
        return {
            'Referer': self.referer
        }

    def get_content_check_objects(self):
        if not self._cached_content_objs:
            check_objs = []

            for content_to_check in self.get_content_to_check():
                for available_type in self.available_content_types:
                    if available_type.does_match(content_to_check):
                        check_objs.append(available_type)

            self._cached_content_objs = check_objs

        return self._cached_content_objs
