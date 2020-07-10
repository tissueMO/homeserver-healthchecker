自宅サーバー 死活監視ツール
====

## Summary

自宅サーバーの死活監視 (HTTP/HTTPS) を行うツールです。  
ヘルスチェックが通らない場合は Slack にアラートを送出します。  
AWS CloudWatch Events と AWS Lambda を組み合わせることによって実質無料でミニマルな監視サービスを構築することができます。  


## Dependency

- Python 3.8
  - Python パッケージ
    - requests
- Slack Incoming Webhooks


## Setup

### AWS Lambda にデプロイするところまで

- pip コマンドが使える状態を前提とします。
- リポジトリー直下にて以下コマンドを実行します。
  - `$ pip install -r requirements.txt --target .`
    - Lambda へのデプロイ後に依存パッケージをインストールすることができないため、事前に手元に集める必要があります。
- リポジトリー全体を zip 圧縮します。
- 作成した zip ファイルを AWS Lambda にアップロードします。
- 作成した Lambda 関数にて以下の設定を適用します。
  - 環境変数
    - `SCHEMA`: `http` or `https`
    - `HOST`: ヘルスチェック対象のドメイン名
    - `PORT`: ポート番号 (80 もしくは 443 の場合は省略可能)
    - `TIMEOUT_SEC`: タイムアウト秒数。Lambda 関数のタイムアウト時間よりも短い値にする必要があります。
    - `SLACK_WEBHOOK_URL`: アラートを送出するのに使用する Slack の Incoming Webhook URL


### ミニマルな監視サービスとして稼働させる

- AWS CloudWatch Events にて作成した Lambda 関数を定期実行されるようにします。


## License

[MIT](LICENSE.md)


## Author

[tissueMO](https://github.com/tissueMO)
