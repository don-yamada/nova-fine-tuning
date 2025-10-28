# Nova Fine-tuning Dataset Generator

Amazon Bedrock Nova用のファインチューニングデータセットを生成するツールです。

## 概要

このプロジェクトは、画像とテキストのペアからBedrock Nova用のJSONLファイルを生成します。画像分類やマルチモーダルタスクのファインチューニングに使用できます。

## ファイル構成

```
nova-fine-tuning/
├── create_jsonl.py    # メインスクリプト
├── prompt.txt         # システムプロンプト設定
├── images/           # 学習用画像フォルダ
└── README.md
```

## 使用方法

### 1. 準備

1. `images/`フォルダにJPEG画像を配置
2. `prompt.txt`にシステムプロンプトを記述
3. `create_jsonl.py`内の以下を編集：
   - `expected_answer`: 期待する回答
   - `S3バケット名`: 実際のS3バケット名
   - `アカウントID`: AWSアカウントID

### 2. 実行

```bash
python create_jsonl.py
```

実行後、`train.jsonl`ファイルが生成されます。

## 出力形式

Bedrock conversation形式のJSONLファイルを生成：

```json
{
  "schemaVersion": "bedrock-conversation-2024",
  "system": [{"text": "システムプロンプト"}],
  "messages": [
    {
      "role": "user", 
      "content": [{"image": {"format": "jpeg", "source": {"s3Location": {...}}}}]
    },
    {
      "role": "assistant",
      "content": [{"text": "期待する回答"}]
    }
  ]
}
```

## 実際にFine-tuningする際の注意事項

- 画像はS3にアップロード済みである必要があります
- S3はカスタムモデルを作成したいリージョンに合わせてください
- ファイルパスとS3 URIが一致するよう設定してください
