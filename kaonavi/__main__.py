import os
import sys
from typing import Dict

from dotenv import load_dotenv
from argparse import ArgumentParser

from subcommands import KaonaviApiException, get_token
from subcommands.sheets import get_sheet

# カオナビのAPIをリクエストするときのタイムアウト秒
KAONAVI_REQUEST_TIMEOUT = 30

# 環境変数を読み込み
load_dotenv()


def get_input(msg: str) -> str:
    """ユーザーからの入力を求める。

    Args:
        msg: ユーザーから入力を求めるときのメッセージ。

    Returns:
        ユーザーが入力した文字列。
    """
    while True:
        try:
            value = input(f"{msg}: ")
            cleaned_value = value.strip()
            if cleaned_value != "":
                break
        except KeyboardInterrupt:
            sys.exit(1)
    return cleaned_value


def get_consumer_key() -> str:
    """カオナビのコンシューマー・キーを取得する。

    カオナビのコンシューマー・キーを環境変数KAONAVI_CONSUMER_KEYから取得する。
    環境変数KAONAVI_CONSUMER_KEYが設定されていない場合は、ユーザーに入力を求める。

    Returns:
        カオナビのコンシューマー・キー
    """
    consumer_key = os.getenv("KAONAVI_CONSUMER_KEY", "")
    if consumer_key == "":
        consumer_key = get_input("カオナビのコンシューマー・キー")
    return consumer_key


def get_consumer_secret() -> str:
    """カオナビのコンシューマー・シークレットを取得する。

    カオナビのコンシューマー・シークレットを環境変数KAONAVI_CONSUMER_SECRETから取得する。
    環境変数KAONAVI_CONSUMER_SECRETが設定されていない場合は、ユーザーに入力を求める。

    Returns:
        カオナビのコンシューマー・シークレット
    """
    consumer_key = os.getenv("KAONAVI_CONSUMER_SECRET", "")
    if consumer_key == "":
        consumer_key = get_input("カオナビのコンシューマー・シークレット")
    return consumer_key


def get_end_point_url() -> str:
    """環境変数からカオナビのAPIエンドポイントを取得する。

    環境変数からカオナビのAPIエンド・ポイントを取得できない場合は、エラーメッセージを標準エラー出力に
    出力して、プログラムを終了する。

    Returns:
        カオナビのAPIエンドポイント。
    """
    key = "KAONAVI_API_ENDPOINT"
    endpoint = os.getenv(key, "")
    if endpoint == "":
        print(f"環境変数にカオナビAPIのエンドポイント({key})が設定されていません。", file=sys.stderr)
        exit(1)
    return endpoint


def get_request_timeout() -> int:
    """環境変数からカオナビのAPIをリクエストするときの、タイムアウト秒を取得する。

    環境変数からカオナビのAPIをリクエストするときのタイムアウト秒を取得できなかった場合は、デフォルトの
    タイムアウト秒を返却する。
    """
    timeout = os.getenv("KAONAVI_API_TIMEOUT", "")
    try:
        timeout = int(timeout)
    except ValueError:
        timeout = KAONAVI_REQUEST_TIMEOUT
    return timeout


def get_access_token(
    consumer_key: str, consumer_secret: str, endpoint: str, timeout: int
) -> Dict:
    """カオナビからアクセス・トークンを取得する。

    カオナビにトークンをリクエストして、アクセス・トークンを取得する。
    アクセス・トークンの取得に失敗した場合は、プログラムを終了する。

    Args:
        consumer_key: カオナビのコンシューマー・キー。
        consumer_secret: カオナビのコンシューマー・シークレット。
        endpoint: カオナビAPIエンドポイントURL。
        timeout: カオナビAPIリクエスト・タイムアウト秒。

    Returns:
        カオナビからのレスポンス（JSON）を記録した辞書。
        辞書のキーと値を以下に示す。
        * access_token: アクセス・トークン。
        * token_type: アクセス・トークンの種類。
        * expire_in: アクセス・トークンの有効期限（秒）。
    """
    try:
        return get_token(consumer_key, consumer_secret, endpoint, timeout)
    except KaonaviApiException as exception:
        print(f"{exception}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":

    def gen_argument_parser() -> ArgumentParser:
        """コマンドライン引数を解析するパーサーを返却する。

        Returns:
            コマンドライン引数を解析するパーサー。
        """
        # コマンドライン引数を解析するパーサーを構築
        parser = ArgumentParser(description="カオナビにAPIをリクエストします。")
        subparsers = parser.add_subparsers()
        # シート情報取得APIをリクエストするサブコマンド
        sheet_command = subparsers.add_parser("sheet", help="シート情報取得APIをリクエストします。")
        sheet_command.add_argument("sheet_id", type=int, help="取得するシートのシートID。")
        sheet_command.set_defaults(func=get_sheet)
        return parser

    def main():
        parser = gen_argument_parser()
        args = parser.parse_args()
        if hasattr(args, "func"):
            # コンシューマー・キーを取得
            consumer_key = get_consumer_key()
            # コンシューマー・シークレットを取得
            consumer_secret = get_consumer_secret()
            # カオナビAPIエンドポイントURLを取得
            endpoint = get_end_point_url()
            # カオナビAPIリクエストタイムアウト秒を取得
            timeout = get_request_timeout()
            # カオナビからアクセス・トークンを取得
            credentials = get_access_token(
                consumer_key, consumer_secret, endpoint, timeout
            )
            access_token = credentials["access_token"]
            # サブコマンドを実行
            args.func(args, access_token, endpoint, timeout)
        else:
            parser.print_help()

    main()
