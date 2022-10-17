from argparse import Namespace
from typing import Dict

import requests

from . import KaonaviApiException, call_kaonavi_api


def get_sheet(
    args: Namespace,
    access_token: str,
    endpoint: str,
    timeout: int,
) -> Dict:
    """シート情報を取得する。

    Args:
        args: コマンドライン引数を格納したNamespaceオブジェクト。
        access_token: カオナビから取得したアクセス・トークン。
        endpoint: カオナビAPIエンドポイント。
        timeout: リクエスト・タイムアウト秒。

    Returns:
        シート情報を記録した辞書。
    """
    url = f"{endpoint}sheets/{args.sheet_id}"
    response = call_kaonavi_api(
        url, method="get", access_token=access_token, timeout=timeout
    )
    if response.status_code == requests.codes.ok:
        return response.json()
    elif response.status_code == requests.codes.not_found:
        raise KaonaviApiException("指定したシートIDで特定されるシートが存在しません。")
    else:
        raise KaonaviApiException("不明なエラーが発生しました。")
