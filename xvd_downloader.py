import os
import tldextract
import argparse
from urllib import request
from urllib.parse import urlparse

DEFAULT_DOWNLOAD_URL = os.path.expanduser("~/Downloads/")


def get_downloadable_info(url):
    print(f"Parsing video URL from {url}")
    urls = []

    req = request.Request(url)
    # req.set_proxy("PROXY_IP_AND_PORT", type=str)
    r = request.urlopen(req)

    for line in r.read().decode(r.headers.get_content_charset()).splitlines():
        if "html5player.setVideoUrl" in line:
            urls.append(line)

    return urls


def download_videos(urls, download_folder):
    if len(urls) == 1:
        url = urls[0]
    else:
        url = urls[0] if "setVideoUrlHigh" in urls[0] else urls[1]

    if url.count("'") != 2:
        raise ValueError("Current video URL format is not supported")

    url = url.split("'")[1]
    file_name = urlparse(url).path.split("/")[-1]
    if not download_folder.endswith("/"):
        download_folder = download_folder + "/"
    download_dest = download_folder + file_name

    print(f"Downloading at {download_dest}")
    request.urlretrieve(url, download_dest)


def handle_download(url, download_folder):
    download_videos(get_downloadable_info(url), download_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="Xvideos video URL")
    parser.add_argument("-d", "--download", type=str, help="Download folder", default=DEFAULT_DOWNLOAD_URL)
    args = parser.parse_args()
    if f"{tldextract.extract(args.url).domain}" != "xvideos":
        raise ValueError(f"Invalid domain {args.url}. Please use Xvideos URL")

    handle_download(args.url, args.download)
