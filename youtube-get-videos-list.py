import sys
import math
import getpass
from apiclient.discovery import build
import googleapiclient
import meilisearch


class style():
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    RESET = '\033[0m'


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def color(content: str, color: style) -> str:
    """Returns the content colored in the given color."""
    return "%s%s%s" % (color, content, style.RESET)


def get_channels_videos_list(api_key: str, channel_id: str, index_tags=False) -> list:
    """Get channels videos list from a channel id."""
    # Create an instance of youtube api
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
    except googleapiclient.errors.HttpError:
        print(color("The provided Youtube API Key is not valid.", style.RED))
        exit()

    # Call the API to retrieve the playlist id
    res = youtube.channels().list(id=channel_id, part="contentDetails") \
                 .execute()

    # Get the playlist id
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Create an variable to store all videos
    videos = []

    # Store the next page token
    next_page_token = None

    # Store the total of requests made to the YouTube
    # for the current channel
    total_requests = 0

    # Loop until we reach the last page
    while True:
        # Call the current page of the API to get the videos id
        res = youtube.playlistItems().list(playlistId=playlist_id,
                                           part="snippet",
                                           maxResults=50,
                                           pageToken=next_page_token).execute()

        # Incremente the total requests counter
        total_requests += 1

        # Store the next page token
        next_page_token = res.get('nextPageToken')

        # Get all videos id
        videos_id = [video["snippet"]["resourceId"]["videoId"]
                     for video in res["items"]]

        # Do reauests to videos list to be able to have the tags
        if index_tags:
            res = youtube.videos().list(id=",".join(videos_id),
                                        part="snippet",
                                        maxResults=50).execute()

            # Incremente the total requests counter
            total_requests += 1

        # Concatenate the current page videos with
        # all the videos.
        # Format the video information for MeiliSearch
        for video in res['items']:
            # Get the video information
            video_id = video["id"] if "id" in video else video["snippet"]["resourceId"]["videoId"]
            channel_id = video["snippet"]["channelId"]
            channel_title = video["snippet"]["channelTitle"]
            published_date = video["snippet"]["publishedAt"]
            title = video["snippet"]["title"]
            description = video["snippet"]["description"]
            tags = video["snippet"]["tags"] if "tags" in video["snippet"] else []
            thumbnail_url = video["snippet"]["thumbnails"]["high"]["url"]
            link = "https://www.youtube.com/watch?v=%s" % video_id

            # Create the item structure
            item = {
                "id": video_id,
                "channel_title": channel_title,
                "published_date": published_date,
                "title": title,
                "description": description,
                "tags": tags,
                "link": link,
                "thumbnail": thumbnail_url
            }

            # Remove the key tags if tags are not indexed
            if index_tags is False:
                del item["tags"]

            # Index the video
            videos.append(item)

        # If we reach the last page, break the loop
        # and stop to call the API
        if next_page_token is None:
            break

    return videos, total_requests


def parse_arguments() -> dict:
    """Parse arguments and returns the list of channels."""
    # New index found if true, next iteration
    # the name of the index will be get
    new_index = False

    # Current index name
    current_index = ""

    # Store channels to index
    channels = {}

    # Read arguments
    for arg in sys.argv[1:]:
        # Find the argument -i
        if arg == "-i":
            new_index = True
        elif arg == "-t":
            channels[current_index]["index_tags"] = True
        elif new_index:
            # Store the name of the current MeiliSearch index
            current_index = arg

            # Create the list with the index name
            channels[current_index] = {
                "index_tags": False,
                "channels_id": []
            }

            # Reset the new index flag as we found the index name
            new_index = False
        elif current_index != "":
            # Add the channel id to index
            channels[current_index]["channels_id"].append(arg)

    return channels


def create_meilisearch_client() -> meilisearch.Client:
    """Create and returns the instance of MeiliSearch."""
    # Create the instance of MeiliSearch
    client = meilisearch.Client("http://127.0.0.1:7700")

    # Check if the MeiliSearch server is running
    try:
        client.health()
    except meilisearch.errors.MeiliSearchCommunicationError:
        print(color("Your MeiliSearch server is not running.", style.RED))
        exit()

    return client


if __name__ == "__main__":
    # Print help if no arguments provided or
    # if the argument -h is provided
    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        print("Help")
        exit(0)

    # Ask API Key if not provideed
    if "-k" not in sys.argv:
        api_key = getpass.getpass(prompt='Please, provid your Youtube API Key: ')
    else:
        api_key = sys.argv[sys.argv.index("-k") + 1]

    # Store channels to index
    channels = parse_arguments()

    # Create the instance of MeiliSearch
    client = create_meilisearch_client()

    # Store the total of requests made to the Youtube API
    total_requests = 0

    # Store the current index of the loop
    loop_index = 1

    # Loop over indexes with channels id and index the channels
    for index_name, channel in channels.items():
        # Add a new line to delimit the indexes
        if loop_index > 1:
            print()

        channels_id = channel["channels_id"]
        index_tags = channel["index_tags"]

        # Print the current index
        print("Indexing %s." % index_name)

        # Get the index
        meilisearch_index = client.get_or_create_index(index_name)

        # Delete all documents
        response = meilisearch_index.delete_all_documents()

        # Wait until it has been indexed
        meilisearch_index.wait_for_pending_update(response["updateId"])

        # Create an variable to store all videos
        videos = []

        # Loop over all channels and index videos
        for index, channel_id in enumerate(channels_id):
            # Print progression
            print("Get %d/%d channels." % (index + 1, len(channels_id)), end="\r")

            # Get the videos of the channel
            channel_videos, channel_total_requests = \
                get_channels_videos_list(api_key=api_key,
                                         channel_id=channel_id,
                                         index_tags=index_tags)

            # Concatenate channel videos with all videos
            videos += channel_videos

            # Incremente the total requests
            total_requests += channel_total_requests

            # Print the channel title
            print("\x1b[2K", end="\r")
            print(color("%s: OK!" % videos[-1]["channel_title"], style.GREEN))

        # Store the total of videos of the current index
        index_total_videos = len(videos)

        # Store the chunk number
        chunk_pieces_number = 100

        # Index all videos in MeiliSearch
        for index, videos in enumerate(chunks(videos, chunk_pieces_number)):
            # Print progression
            print("%d/%d indexed." % (min((index + 1) * chunk_pieces_number,
                  index_total_videos), index_total_videos), end="\r")

            # Index videos
            response = meilisearch_index.add_documents(videos)

            # Wait until it has been indexed
            meilisearch_index.wait_for_pending_update(response["updateId"])

        print()

        # Incremente the loop index
        loop_index = loop_index + 1

    # Display the total of requests
    print("\nYou made %s requests to the YouTube API." %
          color(total_requests, style.BLUE))