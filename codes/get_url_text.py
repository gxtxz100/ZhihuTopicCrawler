import requests

def get_url_text(url):
    headers = {
        "user-agent": "填写从浏览器获取的user-agent",
        "cookie": "填写从浏览器获取的cookie",
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")
