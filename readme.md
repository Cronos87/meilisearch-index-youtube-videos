# MeiliSearch Index YouTube Videos

This tool will index all videos of one or multiple YouTube channels into [MeiliSearch](https://www.meilisearch.com).

## How to use

Download or clone this repository and run the following command:

```bash
python youtube-get-videos-list.py [-k API_KEY] -i meilisearch-index-name CHANNEL_ID CHANNEL_ID [-t] -i meilisearch-another-index-name CHANNEL_ID CHANNEL_ID CHANNEL_ID [-t]
```

**Note:**

The argument `-k` can be omitted, but the shell will ask you to enter your YouTube API key.

The argument `-t` tell the script to get the videos' tags, but this will require 1 more call for each page. Basically, it doubles the number of requests.

By default, YouTube allows **10.000** requests per day.

## Roadmap

- [x] Can pass MeiliSearch config from CLI

## Buy me a coffee

If you like this project, it is much appreciated :)

<a href="https://www.buymeacoffee.com/cronos87" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-red.png" alt="Buy Me A Coffee" width="217"></a>
