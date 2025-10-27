import base64
import json
import glob


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def read_prompt_file(filename="prompt.txt"):
    """
    指定されたファイルから内容を読み込み、文字列として返します。
    ファイルが存在しない場合はエラーメッセージを表示します。
    """
    try:
        # ファイルを開き、'r' (読み込みモード)で内容を読み込む
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return f"エラー: ファイル '{filename}' が見つかりませんでした。"
    except Exception as e:
        return f"ファイルの読み込み中にエラーが発生しました: {e}"


with open('train.jsonl', 'w', encoding='utf-8') as f:
    for image_path in glob.glob("images/*.jpeg"):
        system_message = read_prompt_file("prompt.txt")
        expected_answer = '期待する回答を記述'
        item = {
            "schemaVersion": "bedrock-conversation-2024",
            "system": [{
                "text": system_message
            }],
            "messages": [{
                "role": "user",
                "content": [
                    {
                    "image": {
                        "format": "jpeg",
                        "source": {
                            "s3Location": {
                                "uri": "s3://S3バケット名/" + image_path,
                                "bucketOwner": "アカウントID"
                            }
                        }
                    }
                }]
            },
                {
                "role": "assistant",
                "content": [{
                        "text": expected_answer
                }]
            }
            ]
        }
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
