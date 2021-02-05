import setuptools

with open("readme.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="meilisearch-youtube-videos-indexer",
    version="1.0.0",
    author="Yohan T.",
    description="Index your favorites YouTube channels in MeiliSearch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cronos87/meilisearch-index-youtube-videos",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["meilisearch-youtube-videos-indexer = meilisearch_youtube_videos_indexer.meilisearch_youtube_videos_indexer:main"]},
    install_requires=["meilisearch", "google-api-python-client", "toml"],
)
