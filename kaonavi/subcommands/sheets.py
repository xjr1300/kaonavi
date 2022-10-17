from argparse import Namespace
from typing import Dict

import requests


def _call_api(access_token: str, endpoint: str, sheet_id: int, timeout: int) -> Dict:
    """カオナビからシート情報を取得する。

    Args:
        access_token: カオナビから取得したアクセス・トークン。
        endpoint: カオナビAPIエンドポイントURL。
        sheet_id: カオナビから取得するシートのID。
            カオナビの[管理者メニュー] - [公開API v2 情報] - [捜査対象の管理]タブで確認する。
        timeout: カオナビAPIのリクエスト・タイムアウト秒。

    Returns:
        カオナビからレスポンス（JSON）を記録した辞書。
    """
    url = f"{endpoint}/sheets/{sheet_id}"
    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "Kaonavi-Token": access_token,
        },
        timeout=timeout,
    )
    return response.json()


def get_sheet(
    args: Namespace,
    access_token: str,
    endpoint: str,
    timeout: int,
) -> Dict:
    """シート情報を取得する。

    Args:
        args:
    """
    print(args)
    print(access_token)
    print(endpoint)
    print(timeout)
