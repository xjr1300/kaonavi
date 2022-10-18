# カオナビ データ取得プログラム

## 概要

カオナビのAPIを使用して、カオナビからデータを取得するプログラムです。
カオナビから取得したデータは、JSON形式の文字列で標準出力に出力されます。

## 対応API

本プログラムは、kaonavi API v2(2.0)に対応しています。
また、対応しているAPIの種類は以下です。

* アクセス・トークン発行
* シート情報取得

## リポジトリのクローン方法

```bash
git clone https://github.com/xjr1300/kaonavi.git
```

## プログラムのディレクトリ構成

```text
kaonavi
├── kaonavi
│   └── subcommands
├── .env.sample
└── requirements.txt
```

リポジトリをクローンしたとき、`kaonavi`ディレクトリがあります。
このディレクトリを`ルート・ディレクトリ`とします。

## 仮想環境の作成

`ルート・ディレクトリ`に以下の通り仮想環境を作成します。

```bash
cd kaonavi      # ルート・ディレクトリにカレント・ディレクトリを変更
python3 -m venv venv    # Python仮想環境の作成
```

```text
kaonavi
├── kaonavi
│   └── subcommands
├── .env.sample
├── requirements.txt
└── venv        # 作成した仮想環境
```

仮想環境を作成後、以下の通り作成した仮想環境を有効にします。
上記の通り仮想環境を作成したとき、仮想環境が有効になると、ターミナルのプロンプトが`(venv)`になります。

```bash
source venv/bin/activate    # Python仮想環境の有効化
```

## パッケージのインストール

以下を実行して、仮想環境に本プログラムに必要なパッケージをインストールします。

```bash
pip install -r requirements.txt
```

## 環境変数の設定

本プログラムは、以下のデータを環境変数から取得します。
ルート・ディレクトリにある`.env.sample`ファイルを参考に、ルート・ディレクトリに`.env`ファイルを作成します。
`.env`ファイルに設定する環境変数は以下です。
なお、`KAONAVI_API_ENDPOINT`は設定する必要はありません。
また、カオナビのコンシューマー・キーとコンシューマー・シークレットは、カオナビの`カオナビ管理者機能トップ - 公開API v2 情報 - 認証情報`で確認できます。

| 環境変数                | 說明                                                             | 設定値                                      |
| ----------------------- | ---------------------------------------------------------------- | ------------------------------------------- |
| KAONAVI_CONSUMER_KEY    | カオナビの管理者機能ページで確認したコンシューマー・キー         | ー                                          |
| KAONAVI_CONSUMER_SECRET | カオナビの管理者機能ページで確認したコンシューマー・シークレット | ー                                          |
| KAONAVI_API_URL         | カオナビAPIのルートURI                                           | `https://api.kaonavi.jp/api/`               |
| KAONAVI_API_VERSION     | カオナビAPIのバージョン                                          | `v2.0`                                      |
| KAONAVI_API_ENDPOINT    | カオナビAPIエンドポイントURL                                     | `${KAONAVI_API_URL}${KAONAVI_API_VERSION}/` |
| KAONAVI_API_TIMEOUT     | カオナビにAPIをリクエストするときのタイムアウト秒                | `30`                                        |

```text
kaonavi
├── kaonavi
│   └── subcommands
├── .env.sample
├── .env        # 作成した環境変数ファイル
├── requirements.txt
└── venv        # 作成した仮想環境
```

## 使用方法

### ヘルプ

```bash
python -m kaonavi -h
```

#### 說明
本コマンドの使用方法を表示します。

### シート情報取得

```bash
python -m kaonavi sheet <sheet_id>
```

#### 說明

カオナビのシート情報取得APIを呼び出して、カオナビで定義されているシートに記録されているデータを取得します。
データを取得するシートは、`カオナビ管理者機能トップ - 公開API v2 情報 - 操作対象の管理`で、当該シートの`取得`をチェックする必要があります。

#### 引数

* sheet_id: 情報を取得するシートのシートID。シートIDは、カオナビの`カオナビ管理者機能トップ - 公開API v2 情報 - 操作対象の管理`で確認できます。

---

## 本プログラムの実装方針について

`make`コマンドにより、リンターとフォーマッターを実行します。
なお、`Git Hooks`を利用して、コミットをする前（`pre-commit`）に、以下に示すリンターとフォーマッターを実行するように設定しています。

```bash
# リンターの実行
make lint
# フォーマッターの実行
make fmt
```

### リンター

リンターは`flake8`、`isort`及び`black`を使用しています。
`flake8`のプロファイルは`black`にしています。
`black`の行の最大文字数のデフォルトは`88文字`であるため、`flake8`の最大文字数を`88文字`に設定してます。

### フォーマッター

フォーマッターは、`isort`と`black`を使用しています。

## パッケージの更新

`pip-review`で使用しているパッケージに更新があるか確認できます。

```bash
# 更新されたパッケージの確認
pip-review
# 更新されたパッケージを対話式に更新
pip-review --interactive
# 更新されたパッケージを自動的に更新
pip-review --auto
```
