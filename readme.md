# MeiliSearch Index YouTube Videos

This tool will index all videos of one or multiple YouTube channels into [MeiliSearch](https://www.meilisearch.com).

## Installation

Download or clone this repository. Then run the following command to install dependencies:

```bash
pip install -r requirements.txt
```

## How to use

We use the file format [TOML](https://toml.io/en/) to define the channels to index.

Here is an example of how to use it:

```toml
[unity-youtube-videos-en]
name = "Unity YouTube Videos EN"
channels = [
    "UCYbK_tjZ2OrIZFBvU6CCMiA", # Brackeys
    "UCFK6NCbuCIVzA6Yj1G_ZqCg", # Code Monkey
]
tags = true

[unity-youtube-videos-fr]
name = "Unity YouTube Videos FR"
channels = [
    "UCJRwb5W4ZzG43J5_dViL6Fw" # TUTO UNITY FR
]
tags = true
```

Every sections title (ex: [unity-youtube-videos-en]) will define the index name inside MeiliSearch. Channels are an array of YouTube channels ID. Finally, tags will tell the script to get the videos tags.

**CAREFUL**

Setting tags to true will double the number of requests to the YouTube API.

Note that by default, YouTube allows **10.000** requests per day.

### Run the script

Run the following command to start indexing channels into your MeiliSearch instance:

```bash
python youtube-get-videos-list.py [-k API_KEY] [-c CLIENT_ADDRESS] [-m MEILISEARCH_MASTER_KEY] channels.toml
```

The client's address must follow the pattern "http[s]://ip:port".

**Note:**

The argument `-k` can be omitted, but the shell will ask you to enter your YouTube API key.

## Roadmap

- [ ] Use Python native argparse
- [x] Can pass MeiliSearch config from CLI

## Buy me a coffee

If you like this project, it is much appreciated :)

<a href="https://www.buymeacoffee.com/cronos87" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-red.png" alt="Buy Me A Coffee" width="217"></a>
