from typing import Dict, Optional

import requests
from requests.auth import HTTPBasicAuth


class KaonaviApiException(Exception):
    """カオナビAPI例外"""

    pass


def call_kaonavi_api(
    url: str,
    method: str,
    access_token: str,
    headers_ext: Optional[Dict],
    data: Optional[Dict],
    timeout: int,
) -> requests.Response:
    """カオナビAPIをリクエストする。

    アクセス・トークンをリクエスト・ヘッダに追加して、カオナビAPIをリクエストする。
    headers_extを指定した場合、リクエスト・ヘッダにheaders_extのキーと値を追加する。
    タイムアウトの設定忘れを防止するため、この関数を利用して、カオナビAPIをリクエストすること。

    Args:
        url: リクエストするAPIのURL。
        method: リクエストするときのメソッド。
        access_token: アクセス・トークン。
        headers_ext: リクエストするときに追加で付与するヘッダー。
        data: リクエストで送信するデータ。
        timeout: リクエスト・タイムアウト秒。

    Returns:
        レスポンス・オブジェクト。
    """
    headers = {
        "Content-Type": "application/json",
        "Kaonavi-Token": access_token,
    }
    if headers_ext:
        headers.update(headers_ext)
    func = getattr(requests, method)
    return func(url, headers=headers, data=data, timeout=timeout)


def get_token(
    consumer_key: str, consumer_secret: str, endpoint: str, timeout: int
) -> Dict:
    """カオナビからアクセス・トークンを取得する。

    Args:
        consumer_key: カオナビで得られるコンシューマー・キー。
        consumer_secret: カオナビで得られるコンシューマー・シークレット。
        endpoint: カオナビAPIのエンドポイントURL。
        timeout: カオナビAPIのリクエスト・タイムアウト秒。

    Returns:
        カオナビからのレスポンス（JSON）を記録した辞書。
        辞書のキーと値を以下に示す。
        * access_token: アクセス・トークン。
        * token_type: アクセス・トークンの種類。
        * expire_in: アクセス・トークンの有効期限（秒）。

    Exceptions:
        KaonaviApiException:
            認証に失敗しました。
            アクセス・トークンの発行が制限されました。
    """
    url = f"{endpoint}token"
    response = requests.post(
        url,
        auth=HTTPBasicAuth(consumer_key, consumer_secret),
        data="grant_type=client_credentials",
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"},
        timeout=timeout,
    )
    if response.status_code == requests.codes.ok:
        return response.json()
    elif response.status_code == requests.codes.unauthorized:
        raise KaonaviApiException("認証に失敗しました。")
    elif response.status_code == requests.codes.too_many_request:
        raise KaonaviApiException("アクセス・トークンの発行が制限されました。")
    else:
        raise KaonaviApiException("不明なエラーが発生しました。")
