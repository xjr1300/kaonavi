import os
import sys
from typing import Dict

from dotenv import load_dotenv
from argparse import ArgumentParser, Namespace

# 環境変数を読み込み
load_dotenv()


def get_sheet(args: Namespace, consumer_key: str, consumer_secret: str) -> Dict:
    """シート情報を取得する。

    Args:
        args:
    """
    print(args)
    print(consumer_key)
    print(consumer_secret)


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


if __name__ == "__main__":

    def gen_argument_parser() -> ArgumentParser:
        """コマンドライン引数を解析するパーサーを返却する。

        Returns:
            コマンドライン引数を解析するパーサー。
        """
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
            consumer_key = get_consumer_key()
            consumer_secret = get_consumer_secret()
            args.func(args, consumer_key, consumer_secret)
        else:
            parser.print_help()

    main()
