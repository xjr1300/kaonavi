from typing import Dict

from kaonavi.data import QUALIFICATION_SHEET_ID
from kaonavi.api import get_token, get_sheet


def doit(consumer_key: str, consumer_secret: str) -> Dict:
    """保有資格情報を取得する。

    Args:
        consumer_key: カオナビで得られるコンシューマー・キー。
        consumer_secret: カオナビで得られるコンシューマー・シークレット。
    """
    credentials = get_token(consumer_key, consumer_secret)
    return get_sheet(credentials["access_token"], QUALIFICATION_SHEET_ID)


if __name__ == "__main__":
    from argparse import ArgumentParser

    def gen_argument_parser() -> ArgumentParser:
        """コマンドライン引数を解析するパーサーを返却する。

        Returns:
            コマンドライン引数を解析するパーサー。
        """
        parser = ArgumentParser(description="カオナビから、全社員の保有資格を取得します。")
        parser.add_argument("consumer_key", type=str, help="カオナビで得られるコンシューマー・キー。")
        parser.add_argument(
            "consumer_secret", type=str, help="カオナビで得られるコンシューマー・シークレット。"
        )
        return parser

    def main():
        parser = gen_argument_parser()
        args = parser.parse_args()
        qualifications = doit(args.consumer_key, args.consumer_secret)
        print(qualifications)

    main()
