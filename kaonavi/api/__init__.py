import json
from typing import Dict

import requests
from requests.auth import HTTPBasicAuth

from kaonavi.data import KAONAVI_API_END_POINT


def get_token(consumer_key: str, consumer_secret: str) -> Dict:
    """カオナビからアクセス・トークンを取得する。

    Args:
        consumer_key: カオナビで得られるコンシューマー・キー。
        consumer_secret: カオナビで得られるコンシューマー・シークレット。

    Returns:
        カオナビからのレスポンス（JSON）を記録した辞書。
        辞書のキーと値を以下に示す。
        * access_token: アクセス・トークン。
        * token_type: アクセス・トークンの種類。
        * expire_in: アクセス・トークンの有効期限（秒）。
    """
    url = f"{KAONAVI_API_END_POINT}/token"
    response = requests.post(
        url,
        auth=HTTPBasicAuth(consumer_key, consumer_secret),
        data="grant_type=client_credentials",
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"},
    )
    return response.json()


def get_sheet(access_token: str, sheet_id: int) -> Dict:
    """カオナビからシート情報を取得する。

    Args:
        access_token: カオナビから取得したアクセス・トークン。
        sheet_id: カオナビから取得するシートのID。カオナビの[管理者メニュー] - [公開API v2 情報] - [捜査対象の管理]タブで確認する。

    Returns:
        カオナビからレスポンス（JSON）を記録した辞書。
    """
    url = f"{KAONAVI_API_END_POINT}/sheets/{sheet_id}"
    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "Kaonavi-Token": access_token,
        },
    )
    return response.json()
