import requests

headers = {
    "Content_Type": "application/json",
    "Authorization": "Bearer " + 'eeU9uvuv9WKmDsiLPZuh6hkBXnUXBvf/tMbtDW/+H4mvCne3GXmx1g1oXFNy2N88FNOObawlR8jEZ/hU4H8+keJhNXO06K9ItLjU1ukjfJCMgS3ovK1TUNCDmXfDVn0b1/+hBVtmJkZuMa+LJQ0E9AdB04t89/1O/w1cDnyilFU='
    }

def SendMsg(text,uid):
    res = requests.post("https://api.line.me/v2/bot/message/push", 
                        headers=headers, 
                        json={
                            "to": uid,
                            "messages": [{
                                            "type": "text",
                                            "text": text
                                        }]
                        }
                        ).json()

if __name__ == "__main__":
    SendMsg('Hello World!', 'Uddeb94b203b625ed50f27d83e9656583')