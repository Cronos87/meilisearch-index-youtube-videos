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

- [ ] Can pass MeiliSearch config from CLI

## Buy me a coffee

If you like this project, it is much appreciated :)

<a href="https://www.buymeacoffee.com/cronos87" title="Buy me a coffee"><img src="https://img.buymeacoffee.com/api/?url=aHR0cHM6Ly9pbWcuYnV5bWVhY29mZmVlLmNvbS9hcGkvP25hbWU9Q3Jvbm9zODcmc2l6ZT0zMDAmYmctaW1hZ2U9Ym1jJmJhY2tncm91bmQ9ZmY4MTNm&creator=Cronos87&design_code=1&design_color=%23ff813f&slug=cronos87" alt="Buy me a coffee" width="500"></a>
