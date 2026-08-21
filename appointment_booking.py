#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE 動態預約系統（SQLite / PostgreSQL 共用 SQLAlchemy 模型）

啟動時若 appointments 表為空，自動建立未來 8 週、每週三 14:00 / 15:00 / 16:00 時段。
"""

from __future__ import annotations

import datetime
import os
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.parse import parse_qs

import requests
from sqlalchemy import update

# 由 register_appointment_models(db) 注入
_db = None
Appointment = None  # type: ignore

# 預約時段設定（可改環境變數覆寫）
APPOINTMENT_START_DATE = os.environ.get("APPOINTMENT_START_DATE", "2026-06-10")
APPOINTMENT_WEEKS = int(os.environ.get("APPOINTMENT_WEEKS", "8"))
APPOINTMENT_WEEKDAY = int(os.environ.get("APPOINTMENT_WEEKDAY", "2"))  # 0=週一 … 2=週三
APPOINTMENT_TIMES = tuple(
    t.strip()
    for t in os.environ.get("APPOINTMENT_TIMES", "14:00,15:00,16:00").split(",")
    if t.strip()
)

BOOKING_KEYWORD = "立即預約"
MAX_BUTTONS_PER_BUBBLE = 10


def register_appointment_models(database) -> Any:
    """在 app.py 建立 db 後呼叫，註冊 Appointment 模型。"""
    global _db, Appointment
    _db = database

    class AppointmentModel(database.Model):
        __tablename__ = "appointments"
        __table_args__ = (
            database.UniqueConstraint(
                "booking_date", "booking_time", name="uq_appointment_slot"
            ),
        )

        id = database.Column(database.Integer, primary_key=True)
        booking_date = database.Column(database.String(10), nullable=False, index=True)
        booking_time = database.Column(database.String(5), nullable=False, index=True)
        user_id = database.Column(database.String(64), nullable=True, index=True)
        user_name = database.Column(database.String(255), nullable=True)
        booked_at = database.Column(database.DateTime, nullable=True)

        def slot_label(self) -> str:
            return f"{self.booking_date} {self.booking_time}"

    Appointment = AppointmentModel
    return Appointment


def appointments_enabled() -> bool:
    return _db is not None and Appointment is not None


def init_appointment_slots_if_empty() -> None:
    """資料表為空時，寫入 8 週 × 每週三 × 3 時段。"""
    if not appointments_enabled():
        return
    if Appointment.query.count() > 0:
        return

    try:
        start = datetime.datetime.strptime(APPOINTMENT_START_DATE, "%Y-%m-%d").date()
    except ValueError:
        print(f"[ERROR] APPOINTMENT_START_DATE 無效: {APPOINTMENT_START_DATE}")
        return

    # 對齊到指定星期（預設週三）
    while start.weekday() != APPOINTMENT_WEEKDAY:
        start += datetime.timedelta(days=1)

    rows: List[Any] = []
    wed = start
    for _ in range(APPOINTMENT_WEEKS):
        for t in APPOINTMENT_TIMES:
            rows.append(
                Appointment(
                    booking_date=wed.isoformat(),
                    booking_time=t,
                    user_id=None,
                    user_name=None,
                    booked_at=None,
                )
            )
        wed += datetime.timedelta(days=7)

    _db.session.add_all(rows)
    _db.session.commit()
    print(f"[INFO] 已初始化 {len(rows)} 個預約時段（自 {start.isoformat()} 起 {APPOINTMENT_WEEKS} 週）")


def list_available_slots() -> List[Any]:
    if not appointments_enabled():
        return []
    return (
        Appointment.query.filter(Appointment.user_id.is_(None))
        .order_by(Appointment.booking_date, Appointment.booking_time)
        .all()
    )


def get_line_display_name(line_user_id: str) -> str:
    """使用 line-bot-sdk 取得 LINE 顯示名稱；失敗時改 REST。"""
    token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN") or ""
    if not token or not line_user_id:
        return "使用者"
    try:
        from linebot import LineBotApi

        profile = LineBotApi(token).get_profile(line_user_id)
        return (profile.display_name or "使用者").strip() or "使用者"
    except Exception as e:
        print(f"[WARN] LineBotApi.get_profile 失敗: {e}")

    try:
        r = requests.get(
            f"https://api.line.me/v2/bot/profile/{line_user_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        if r.status_code == 200:
            return (r.json().get("displayName") or "使用者").strip() or "使用者"
    except Exception as e:
        print(f"[WARN] LINE profile REST 失敗: {e}")
    return "使用者"


def _parse_postback_data(data: str) -> Dict[str, str]:
    if not data:
        return {}
    return {k: (v[0] if v else "") for k, v in parse_qs(data, keep_blank_values=True).items()}


def book_slot_atomic(
    booking_date: str,
    booking_time: str,
    line_user_id: str,
    user_name: str,
) -> bool:
    """
    原子更新：僅在 user_id IS NULL 時寫入，避免重複預約。
    回傳 True 表示成功預約。
    """
    if not appointments_enabled():
        return False

    now = datetime.datetime.utcnow()
    stmt = (
        update(Appointment)
        .where(
            Appointment.booking_date == booking_date,
            Appointment.booking_time == booking_time,
            Appointment.user_id.is_(None),
        )
        .values(user_id=line_user_id, user_name=user_name, booked_at=now)
    )
    result = _db.session.execute(stmt)
    _db.session.commit()
    return bool(result.rowcount)


def build_available_slots_flex(slots: List[Any]) -> Dict[str, Any]:
    """將可用時段組裝為 Flex Message（carousel 多頁按鈕）。"""
    buttons: List[Dict[str, Any]] = []
    for slot in slots:
        label = f"{slot.booking_date} {slot.booking_time}"
        data = f"action=book&date={slot.booking_date}&time={slot.booking_time}"
        buttons.append(
            {
                "type": "button",
                "style": "primary",
                "height": "sm",
                "action": {
                    "type": "postback",
                    "label": label[:40],
                    "data": data,
                    "displayText": f"預約 {label}",
                },
            }
        )

    bubbles: List[Dict[str, Any]] = []
    for i in range(0, len(buttons), MAX_BUTTONS_PER_BUBBLE):
        chunk = buttons[i : i + MAX_BUTTONS_PER_BUBBLE]
        bubbles.append(
            {
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "可預約時段",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#ffffff",
                        },
                        {
                            "type": "text",
                            "text": f"共 {len(slots)} 個時段可選",
                            "size": "xs",
                            "color": "#eeeeee",
                            "margin": "sm",
                        },
                    ],
                    "backgroundColor": "#1DB446",
                    "paddingAll": "16px",
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": chunk,
                    "paddingAll": "16px",
                },
            }
        )

    contents: Dict[str, Any]
    if len(bubbles) == 1:
        contents = bubbles[0]
    else:
        contents = {"type": "carousel", "contents": bubbles}

    return {
        "type": "flex",
        "altText": f"可預約時段（{len(slots)} 個）",
        "contents": contents,
    }


def handle_booking_list_request(
    reply_token: str,
    reply_text: Callable[[str, str], bool],
    reply_messages: Callable[[str, List[Dict[str, Any]]], bool],
) -> None:
    """處理「立即預約」文字訊息。"""
    if not appointments_enabled():
        reply_text(
            reply_token,
            "預約功能需要資料庫支援。請在伺服器設定 DATABASE_URL（本機預設為 sqlite:///human_design.db）。",
        )
        return

    slots = list_available_slots()
    if not slots:
        reply_text(reply_token, "抱歉，目前所有時段皆已被預約完畢！")
        return

    flex_msg = build_available_slots_flex(slots)
    reply_messages(reply_token, [flex_msg])


def handle_booking_postback(
    reply_token: str,
    line_user_id: Optional[str],
    postback_data: str,
    reply_text: Callable[[str, str], bool],
) -> None:
    """處理 postback action=book。"""
    if not appointments_enabled():
        reply_text(reply_token, "預約功能暫未啟用，請稍後再試。")
        return

    params = _parse_postback_data(postback_data)
    if params.get("action") != "book":
        return

    booking_date = (params.get("date") or "").strip()
    booking_time = (params.get("time") or "").strip()
    if not booking_date or not booking_time:
        reply_text(reply_token, "預約資料不完整，請重新輸入「立即預約」。")
        return

    if not line_user_id:
        reply_text(reply_token, "無法取得您的 LINE 帳號，請稍後再試。")
        return

    display_name = get_line_display_name(line_user_id)
    ok = book_slot_atomic(booking_date, booking_time, line_user_id, display_name)
    if ok:
        reply_text(
            reply_token,
            f"🎉 預約成功！時段為 {booking_date} {booking_time}",
        )
    else:
        reply_text(
            reply_token,
            "啊！該時段剛剛正好被其他人預約走了，請重新選擇其他時段！",
        )


BOOKING_HELP_LINE = "輸入「立即預約」可查看並預約諮詢時段。"
