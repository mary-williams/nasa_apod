# NASA APOD Slack Bot via AWS Lambda

This project creates an automated Slack bot that posts NASA's Astronomy Picture of the Day (APOD) to your Slack channel every day, using AWS Lambda for serverless execution.

<img width="665" height="587" alt="Screenshot 2025-08-02 at 4 08 01 PM" src="https://github.com/user-attachments/assets/394a0d6a-bdf0-4b65-81cc-18eebf954677" />
<img width="640" height="611" alt="Screenshot 2025-08-02 at 4 07 19 PM" src="https://github.com/user-attachments/assets/0ca6b13a-2622-4223-82b1-f00da857a370" />
<img width="811" height="626" alt="Screenshot 2025-08-02 at 4 02 28 PM" src="https://github.com/user-attachments/assets/3e7955b7-b346-4ba5-814a-b99b3422f070" />

## Features

- Fetches and posts the daily NASA APOD (image or video) to Slack.
- Runs serverlessly on AWS Lambda—no servers required!
- Uses Slack Block Kit formatting for rich message display.

## Prerequisites

- AWS Account with Lambda access
- Slack workspace and a Slack Incoming Webhook URL
- NASA API Key ([Get one](https://api.nasa.gov/))
- Python 3.8+ for local development and packaging

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/mary-williams/nasa_apod.git
    cd nasa_apod
    ```

2. **Install dependencies:**

    This project uses `requests`; make sure to include it in your Lambda deployment package.

    ```bash
    pip install requests -t .
    ```

3. **Set environment variables in AWS Lambda:**

    - `NASA_API_KEY`: Your API key from NASA
    - `SLACK_WEBHOOK_URL`: Your Slack webhook URL

    You can set these in the Lambda console under "Configuration" > "Environment variables".

4. **Zip the code for deployment:**

    ```bash
    zip -r function.zip .
    ```

5. **Create the Lambda function:**

    - Runtime: Python 3.8+
    - Handler: `lambda_function.lambda_handler`
    - Upload the zip file
    - Add environment variables

6. **Schedule the Lambda function:**

    Use AWS EventBridge (CloudWatch Events) to trigger the Lambda daily.
    - Rule schedule expression: `cron(0 13 * * ? *)` (posts at 13:00 UTC)

## How it Works

- The Lambda function fetches the day's APOD from NASA's API.
- Formats the content (image/video, title, description) for Slack.
- Posts it to the Slack channel using the webhook.

## Usage

Once deployed and scheduled, nothing else is required. The bot will automatically post each day.

## Troubleshooting

- Check your Lambda logs in AWS CloudWatch for errors.
- Ensure your API keys and webhook URLs are correct.
- Make sure necessary permissions are set for Lambda to execute.

## License

MIT
