import datetime
import os
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.models import (
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageEvent,
    TextMessage,
    ImageCarouselColumn,
    ImageCarouselTemplate,
    MessageTemplateAction,
    DatetimePickerTemplateAction,
    PostbackEvent,
)
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime

load_dotenv()
line_bot_api = LineBotApi(os.getenv("LINE_MESSAGING_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_MESSAGING_CHANNEL_SECRET"))

# Google Calendar API 的範圍
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def get_google_credentials():
    """取得 Google OAuth 憑證，並確保包含 refresh_token"""
    SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
    creds = None

    # 檢查 token.json 是否存在
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # 憑證不存在或過期則重新授權
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(
                port=8080, access_type="offline", prompt="consent"
            )  # 確保使用 prompt='consent'，即使用戶已經授權也會再次請求同意

        # 保存 token.json，包含 refresh_token
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())

    return creds


def convert_line_datetime_to_google_format(line_datetime):
    return datetime.strptime(line_datetime, "%Y-%m-%dT%H:%M").strftime(
        "%Y-%m-%dT%H:%M:%S"
    )


def create_calendar_event(event_data):
    """建立 Google 日曆活動，動態抓取使用者的輸入資料"""
    try:
        creds = get_google_credentials()
        service = build("calendar", "v3", credentials=creds)
        start_time = convert_line_datetime_to_google_format(event_data["start_time"])
        end_time = convert_line_datetime_to_google_format(event_data["end_time"])

        event = {
            "summary": event_data["description"],  # 使用者輸入的日程名稱作為標題
            "location": event_data["location"],  # 使用者輸入的地點
            "description": (
                f"穿搭名稱：{event_data['dress']}\n"
                f"去LineBot看穿搭圖片: https://line.me/R/ti/p/40438shuqi"
            ),
            "start": {
                "dateTime": start_time,  # 使用者選擇的開始時間
                "timeZone": "Asia/Taipei",
            },
            "end": {
                "dateTime": end_time,  # 使用者選擇的結束時間
                "timeZone": "Asia/Taipei",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 60},  # 提醒設置
                ],
            },
        }

        # 呼叫 Google Calendar API 建立活動
        event_result = (
            service.events().insert(calendarId="primary", body=event).execute()
        )
        print(f"Event created: {event_result.get('htmlLink')}")

        return event_result.get("htmlLink")  # 回傳日曆連結

    except Exception as e:
        print(f"無法建立活動: {e}")
        return None


def handleUserInput(event, conversation_state):
    """處理使用者輸入，並建立 Google 日曆活動"""
    step = conversation_state["step"]

    if isinstance(event, PostbackEvent):
        data = event.postback.data.split("&")
        action = data[0].split("=")[1]

        if action == "start_time":
            conversation_state["data"]["start_time"] = event.postback.params["datetime"]
            conversation_state["step"] = "end_time"
            sendEndTime(event)
        elif action == "end_time":
            conversation_state["data"]["end_time"] = event.postback.params["datetime"]
            conversation_state["step"] = "location"
            requestLocation(event)

    elif isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
        if step == "location":
            conversation_state["data"]["location"] = event.message.text
            conversation_state["step"] = "description"
            requestDescription(event)
        elif step == "description":
            conversation_state["data"]["description"] = event.message.text
            conversation_state["step"] = "choose_dress"
            choose_dress(event)
        elif step == "choose_dress":
            conversation_state["data"]["dress"] = event.message.text
            event_link = create_calendar_event(conversation_state["data"])
            conversation_state["step"] = "complete"
            conversation_state["data"] = {}
            if event_link:  # 確認是否成功建立日曆活動
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"建立成功！查看活動：{event_link}"),
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="無法建立活動，請稍後再試。"),
                )


def sendStartTime(event):  # 選擇開始時間
    try:
        message = TemplateSendMessage(
            alt_text="選取日期時間",
            template=ButtonsTemplate(
                title="新增穿搭日程安排開始時間",
                text="請選擇：",
                actions=[
                    DatetimePickerTemplateAction(
                        label="選取開始日期時間",
                        data="action=start_time",
                        mode="datetime",
                        initial="2024-11-09T11:00",
                        min="2024-01-01T00:00",
                        max="2024-12-31T23:59",
                    )
                ],
            ),
        )
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=f"發生錯誤！{e}")
        )


def sendEndTime(event):  # 選擇結束時間
    try:
        message = TemplateSendMessage(
            alt_text="選取結束日期時間",
            template=ButtonsTemplate(
                title="新增穿搭日程安排結束時間",
                text="請選擇：",
                actions=[
                    DatetimePickerTemplateAction(
                        label="選取結束日期時間",
                        data="action=end_time",
                        mode="datetime",
                        initial="2024-11-09T15:00",
                        min="2024-01-01T00:00",
                        max="2024-12-31T23:59",
                    )
                ],
            ),
        )
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=f"發生錯誤！{e}")
        )


def requestLocation(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入目的地"))


def requestDescription(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="請輸入日程名稱")
    )


def choose_dress(event):
    try:
        message = TemplateSendMessage(
            alt_text="穿搭組合",
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url="https://imgur.com/68jUT8F.png",
                        action=MessageTemplateAction(label="展覽裝", text="展覽裝"),
                    ),
                ]
            ),
        )
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=f"發生錯誤！{e}")
        )


# conversation_state 初始值
conversation_state = {"step": "start_time", "data": {}}
event = MessageEvent(reply_token="dummy_token", message=TextMessage(text="dummy_text"))
