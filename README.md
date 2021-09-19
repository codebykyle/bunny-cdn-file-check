# Bunny CDN Video Checker

There currently appears to be an issue where, if you upload a video before checking on MP4 ballback on BunnyCDN, 
videos can be left in a state where the MP4 videos are not transcoded.

In order to fix this, you must contact BunnyCDN's support team.

This tool will help you identify affected videos. It will check an entire stream container
for the status of transcoded videos.

### Setup and install
It is recommended you use a virtual environment to run this application, however, that is not required.


Install the dependencies for the application

`pip install -r requirements.txt`

You will need the information from the "API" tab on your stream container.

In Bunny CDN, go to the Stream tab, then click API. Note down the following:
- Video Library ID
- CDN Hostname
- API Key

You can run the application like so:

`python check_bunny.py --library-id yourlibraryid --hostname yourcdnhostname --api-key yourapikey --content 720,1080,1440 -o result.xlsx`

The options are:

| Short | Long         | Description                                                                                                                  |
|-------|--------------|------------------------------------------------------------------------------------------------------------------------------|
| -l    | --library_id | The "Library ID" field value in the API tab of the stream container you wish to check                                        |
| -K    | --api-key    | The "API Key" field value in the API tab of the stream container you wish to check                                           |
| -H    | --hostname   | The "CDN Hostname" field value in the API tab of the stream container you wish to check                                      |
| -C    | --content    | A comma separated list of the content you'd like to check for, eg: 720p, 1080p, hls, etc. The "p" is optional for mp4 videos |
| -R    | --referer    | Sets a referer on the request to the content in order to bypass the direct access setting                                    |
| -o    | --out        | File to save the results to. Supports .json and .xlsx                                                                        |

