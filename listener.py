import requests
import time


def reminder(title, content, mode=None, bark_id=""):
    if mode is None:
        print(title + "\n" + content)
    elif mode == "bark":
        # 提醒服务的URL
        reminder_url = f"https://api.day.app/{bark_id}/{title}/{content}"
        try:
            response = requests.post(reminder_url)
            response.raise_for_status()  # 检查请求是否成功
            print(f"提醒发送成功: {title}")
        except requests.exceptions.RequestException as e:
            print(f"发送提醒时发生错误: {e}")


url = ""
headers = {
    "Accept": "application/json,text/*;q=0.99",
    "Authorization": ""
}

last_final_rating_justifications = {}

try:
    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        for index, reply in enumerate(data['notes'][0]['details']['directReplies']):
            reviewer_name = reply['signatures'][0].split('/')[-1]
            final_rating = reply['content'].get('final_rating', {}).get('value', 'No Rating')
            final_rating_justification = reply['content'].get('final_rating_justification', None)
            final_rating_justification = final_rating_justification.get('value', None) if final_rating_justification else None

            if final_rating_justification and last_final_rating_justifications.get(index) != final_rating_justification:
                title = f"{reviewer_name}-{final_rating}"
                reminder(title, final_rating_justification)
                last_final_rating_justifications[index] = final_rating_justification

        time.sleep(300)

except requests.exceptions.RequestException as e:
    reminder("网络错误", "发生网络错误，循环已终止。")
