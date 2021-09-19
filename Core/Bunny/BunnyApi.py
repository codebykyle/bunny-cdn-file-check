from Core.Colors import Colors
from Core.Output import output
from Core.ProgressBar import progressBar
from Core.Bunny.BunnyVideo import BunnyVideo
from Core.Bunny.BunnyCollection import BunnyCollection

import requests


class BunnyAPI:
    def __init__(self, library_id, api_key, cdn_hostname):
        self.library_id = library_id
        self.api_key = api_key
        self.cdn_hostname = cdn_hostname

    def _get_headers(self):
        return {
            'AccessKey': self.api_key,
            'Content-Type': 'application/*+json'
        }

    def get_library_videos(self, collection=None):
        if collection:
            output(Colors.BOLD + Colors.OKBLUE + "Loading Collection Videos: %s" % collection + Colors.ENDC)
        else:
            output(Colors.BOLD + Colors.OKBLUE  + "Loading Library Videos: %s" % self.library_id + Colors.ENDC)

        video_list_url = "http://video.bunnycdn.com/library/%s/videos" % (
            self.library_id
        )

        all_videos = []
        page = 1

        # Get all pages. Do while loop would be nice; thanks, Python.
        while True:
            get_parameters = {
                'page': page,
                'itemsPerPage': 100,
                'collection': collection.collection_id if collection else None
            }

            api_response = requests.get(
                video_list_url,
                params=get_parameters,
                headers=self._get_headers()
            )

            if api_response.status_code == 200:
                json_object = api_response.json()

                for video_result in json_object['items']:
                    # We should only check videos which are in the status of '4' which is 'Live'
                    if video_result['status'] != 4:
                        continue

                    video_obj = BunnyVideo()
                    video_obj.video_id = video_result['guid']
                    video_obj.video_name = video_result['title']
                    video_obj.cdn_hostname = self.cdn_hostname
                    video_obj.library_id = video_result['videoLibraryId']
                    video_obj.collection = collection
                    all_videos.append(video_obj)

                    progressBar(
                        iteration=len(all_videos),
                        total=json_object['totalItems'],
                        prefix="Loading Videos"
                    )

                page += 1

                if len(all_videos) >= json_object['totalItems']:
                    break
            else:
                raise Exception(
                    "Unable to get collections for videos for library %s, collection: %s. Status code: %s" % (
                        self.library_id,
                        collection.collection_id,
                        api_response.status_code
                    ))

        output("")

        return all_videos

    def get_library_collections(self):
        output(Colors.BOLD + Colors.OKBLUE + "Loading Library Collections: %s" % self.library_id + Colors.ENDC)

        collections_url = "http://video.bunnycdn.com/library/%s/collections" % self.library_id

        all_collections = []
        page = 1

        # Get all pages. Do while loop would be nice; thanks, Python.
        while True:
            get_parameters = {
                'page': page,
                'itemsPerPage': 100
            }

            api_response = requests.get(
                collections_url,
                params=get_parameters,
                headers=self._get_headers()
            )

            if api_response.status_code == 200:
                json_object = api_response.json()
                total_items = json_object['totalItems']

                for item in json_object['items']:
                    collection = BunnyCollection()
                    collection.collection_id = item['guid']
                    collection.collection_name = item['name']
                    collection.library_id = item['videoLibraryId']
                    all_collections.append(collection)

                    progressBar(
                        iteration=len(all_collections),
                        total=total_items,
                        prefix="Loading Collections"
                    )

                page += 1

                if len(all_collections) >= total_items:
                    break
            else:
                raise Exception("Unable to get collections for library %s. Status code: %s" % (
                    self.library_id,
                    api_response.status_code
                ))

        output(Colors.OKGREEN + "✓ Done." + Colors.ENDC)
        output("")

        return all_collections