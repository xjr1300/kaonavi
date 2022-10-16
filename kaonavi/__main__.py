from typing import Dict


def get_sheet(args) -> Dict:
    """シート情報を取得する。

    Args:
        args:
    """
    print(args)


if __name__ == "__main__":
    from argparse import ArgumentParser

    def gen_argument_parser() -> ArgumentParser:
        """コマンドライン引数を解析するパーサーを返却する。

        Returns:
            コマンドライン引数を解析するパーサー。
        """
        parser = ArgumentParser(description="カオナビにAPIをリクエストします。")
        subparsers = parser.add_subparsers()

        # シート情報取得APIをリクエストするサブコマンド
        sheet_command = subparsers.add_parser('sheet', help="シート情報取得APIをリクエストします。")
        sheet_command.add_argument('sheet_id', type=int, help="取得するシートのシートID。")
        sheet_command.set_defaults(func=get_sheet)

        return parser

    def main():
        parser = gen_argument_parser()
        args = parser.parse_args()
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()

    main()
