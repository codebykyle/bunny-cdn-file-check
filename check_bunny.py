from dotenv import load_dotenv
import argparse, sys, os, json, requests, pathlib

from Core.Output import output
from Core.Colors import Colors
from Core.BunnyContentChecker import BunnyContentChecker
from Core.Content import BunnyMp4Content, BunnyHlsContent
from Core.Outputs import JsonOutput, ExcelOutput, OutputManager

load_dotenv()


PRINTS_OUTPUT = True

if __name__ == '__main__':
    output(Colors.OKCYAN + Colors.BOLD + Colors.UNDERLINE + "Bunny CDN Video Status Check" + Colors.ENDC)

    output(
        "This application will check the status of a video library, and all of its collection's, "
        "and ensure that direct streams are available."
    )

    output("")

    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--library-id', required=True, help="The stream library ID for the program to scan", )
    parser.add_argument('-K', '--api-key', required=True, help="the stream library api key")
    parser.add_argument('-H', '--hostname', required=True, help="the CDN Hostname for this library")
    parser.add_argument('-c', '--content', required=True, help="A comma separated list of expected resolutions")
    parser.add_argument('-R', '--referer', required=False, help="Set a referer on the  requests")
    parser.add_argument('-o', '--out', help="A file to save an export of the results", default="results.xlsx")

    args = vars(parser.parse_args())

    checker = BunnyContentChecker(
        library_id=args['library_id'],
        api_key=args['api_key'],
        hostname=args['hostname'],
        referer=args['referer']
    )

    # Register the available checks
    checker.register_content_type(BunnyHlsContent())
    checker.register_content_type(BunnyMp4Content('240'))
    checker.register_content_type(BunnyMp4Content('360'))
    checker.register_content_type(BunnyMp4Content('480'))
    checker.register_content_type(BunnyMp4Content('720'))
    checker.register_content_type(BunnyMp4Content('1080'))
    checker.register_content_type(BunnyMp4Content('1440'))
    checker.register_content_type(BunnyMp4Content('2160'))

    # Limit what we are checking based on the input argument
    checker.set_content_to_check([str(content).strip() for content in args['content'].split(',')])

    # Check the videos
    result = checker.check_all_videos()

    # Manage saving an output file
    out_file = args['out']

    if out_file:
        output_manager = OutputManager()

        # Register available outputs
        output_manager.register_output(JsonOutput())
        output_manager.register_output(ExcelOutput())

        output_manager.save(result, out_file)
