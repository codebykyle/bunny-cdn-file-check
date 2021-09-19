from Core.Outputs.Output import Output
import json


class JsonOutput(Output):
    def does_match(self, input):
        return input.lower() in [
            '.json',
        ]

    def save(self, library_result, outfile):
        array_of_items = []

        for video_result in library_result.get_all_results():
            content_results_dict = {}

            for content_result in video_result.all_content():
                content_results_dict[str(content_result.content)] = {
                    'success': content_result.passed(),
                    'status_code': content_result.status_code
                }

            result_dict = {
                "video": {
                    'video_id': video_result.video.video_id,
                    'video_name': video_result.video.video_name,
                    'cdn_hostname': video_result.video.cdn_hostname,
                    'library_id': video_result.video.library_id,
                },
                'passed': video_result.passed(),
                'content_results': content_results_dict
            }

            # If the video has a collection, add a collection key.
            if video_result.video.collection:
                result_dict['collection'] = {
                    "collection_id": video_result.video.collection.collection_id,
                    "collection_name": video_result.video.collection.collection_name,
                }

            array_of_items.append(result_dict)

        with open(outfile, 'w+') as file:
            file.write(json.dumps(array_of_items, indent=4))

    def __str__(self):
        return '.json'
