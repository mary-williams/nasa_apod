import os
import requests
import datetime

NASA_API_KEY = os.environ['NASA_API_KEY']
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"

def get_apod():
    today = datetime.date.today()
    for i in range(2):
        date_str = (today - datetime.timedelta(days=i)).isoformat()
        params = {
            'api_key': NASA_API_KEY,
            'date': date_str,
            'hd': True
        }
        response = requests.get(NASA_APOD_URL, params=params)
        if response.status_code == 200:
            # good status, return dictionary from response's JSON content
            return response.json()
        elif response.status_code == 404:
            # url not found, bad status
            continue
        else:
            # unexpected status
            response.raise_for_status()
    raise Exception("Could not retrieve APOD.")

def send_slack_message(apod):
    # get values from apod param dictionary
    title = apod.get("title", "NASA APOD")
    explanation = apod.get("explanation", "")
    date = apod.get("date", "")
    media_type = apod.get("media_type", "")
    image_url = apod.get("hdurl") or apod.get("url")

    blocks = []

    # Add image block first if media is an image
    if media_type == "image" and image_url:
        blocks.append({
            "type": "image",
            "image_url": image_url,
            "alt_text": title
        })

    # Then add the text section
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*📷 {title}* ({date})\n{explanation}"
        }
    })

    # If media is a video, add a separate text block for that
    if media_type == "video" and image_url:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"🎥 Video: {image_url}"
            }
        })

    payload = {"blocks": blocks}

    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    response.raise_for_status()
    print("✅ Message sent to Slack.")

def lambda_handler(event, context):
    try:
        apod = get_apod()
        send_slack_message(apod)
        return {
            'statusCode': 200,
            'body': 'Message sent to Slack successfully!'
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            # return 500 for unexpected error
            'statusCode': 500,
            'body': f'Error occurred: {e}'
        }
