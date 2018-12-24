import os
import requests
import random
import io
from dotenv import load_dotenv


def get_posted_comics_nums():
    if not os.path.exists("posted.txt"):
        return []
    with open("posted.txt", "r") as file:
        return map(int, file.read().split())


def get_random_comics_num():
    total_num = requests.get("http://xkcd.com/info.0.json").json()["num"]
    posted_comics = get_posted_comics_nums()
    while True:
        random_num = random.randint(0, total_num)
        if random_num not in posted_comics:
            break
    return random_num


def get_comics(num):
    comics_url = "http://xkcd.com/{}/info.0.json".format(num)
    comics_json = requests.get(comics_url).json()
    comment = comics_json["alt"]
    filename = comics_json["title"]+".png"
    img = requests.get(comics_json["img"]).content
    return (filename, img, comment)


def get_upload_url(token=None, api_version=None, group_id=None):
    params = {
        "access_token": token,
        "v": api_version,
        "group_id": group_id
    }
    api = "https://api.vk.com/method/photos.getWallUploadServer"
    res = requests.get(api, params=params).json()
    return res["response"]["upload_url"]


def upload_image(content, url, group_id=None):
    params = {"group_id": group_id}
    files = {"photo": content}
    return requests.post(url, params=params, files=files)


def save_in_album(
    photo=None,
    img_hash=None,
    img_server=None,
    token=None,
    api_version=None,
    group_id=None
):
    api = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "group_id": group_id,
        "photo": photo,
        "server": img_server,
        "hash": img_hash,
        "access_token": token,
        "v": api_version,
    }
    res = requests.post(api, params=params)
    return res


def publish_post(
    attach=None,
    token=None,
    comment=None,
    api_version=None,
    group_id=None
):
    api = "https://api.vk.com/method/wall.post"
    params = {
        "owner_id": "-{}".format(group_id),
        "from_group": 1,
        "message": comment,
        "attachments": attach,
        "access_token": token,
        "v": api_version,
    }
    res = requests.post(api, params=params)
    return res


def get_token(client_id, api_version=None):
    api = "https://oauth.vk.com/authorize"
    params = {
        "client_id": client_id,
        "scope": "photos,groups,wall,offline",
        "response_type": "token",
        "v": api_version,
    }
    return requests.get(api, params=params)


def main():
    load_dotenv()
    api_version = os.getenv("api_version") or exit("no api version")
    client_id = os.getenv("client_id") or exit("no client id")
    token = os.getenv("access_token") or exit("no token")
    group_id = os.getenv("group_id") or exit("no group id")
    upload_url = get_upload_url(token, api_version, group_id)
    comics_num = get_random_comics_num()
    filename, image, comment = get_comics(comics_num)
    with open(filename, "wb") as file:
        file.write(image)
    img = open(filename, 'rb')
    upload_response = upload_image(img, upload_url, group_id).json()
    img.close()
    os.remove(filename)
    im_server = upload_response["server"]
    im_hash = upload_response["hash"]
    im = upload_response["photo"]
    save_response = save_in_album(
        im, im_hash, im_server,
        token, api_version, group_id
    ).json()
    attachments = "{}{}_{}".format(
        "photo",
        save_response["response"][0]["owner_id"],
        save_response["response"][0]["id"],
    )
    publish_response = publish_post(
        attachments,
        token,
        comment,
        api_version,
        group_id,
    )
    print(publish_response, publish_response.json())
    with open("posted.txt", "a") as file:
        file.write(" {}".format(comics_num))


if __name__ == "__main__":
    main()
