from typing import List
from Core.Outputs.Output import Output
from Core.Results.VideoResult import VideoResult

import xlsxwriter


class ExcelOutput(Output):
    def does_match(self,  input):
        return input.lower() in [
            '.xlsx',
        ]

    def save(self, library_result, outfile):
        workbook = xlsxwriter.Workbook(outfile)
        worksheet = workbook.add_worksheet("results")

        headers = [
            'Library ID',
            'Collection ID',
            'Collection Name',
            'Video ID',
            'Video Name',
            'CDN Hostname',
            'Passed All Checks'
        ]

        # Order the content results
        content_result_order = []

        for checked_content in library_result.checked_content:
            headers.append(str(checked_content))
            content_result_order.append(str(checked_content))

        for checked_content in library_result.checked_content:
            headers.append("Status (%s)" % str(checked_content))

        worksheet.write_row(0, 0, headers)

        row = 1 # Start at row 2 due to the he header row

        for result in library_result.get_all_results():
            result_row = [
                result.video.library_id,
                result.video.collection.collection_id if result.video.collection else None,
                result.video.collection.collection_name if result.video.collection else None,
                result.video.video_id,
                result.video.video_name,
                result.video.cdn_hostname,
                result.passed()
            ]

            content_result_dict = {}

            # Convert the list to a dictionary based on the name, then use that dictionary with the content
            # result order to ensure that everything is lined up correctly...
            for content_result in result.all_content():
                content_result_dict[str(content_result.content)] = content_result

            # We will need to do this twice, once for the pass flag, once for the status code.
            for content_order_key in content_result_order:
                result_row.append(content_result_dict[content_order_key].passed())

            for content_order_key in content_result_order:
                result_row.append(content_result_dict[content_order_key].status_code)

            worksheet.write_row(row, 0, result_row)
            row += 1

        workbook.close()

    def __str__(self):
        return '.xlsx'