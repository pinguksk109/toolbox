import json

def build_send_command(script_filename, instance_id):

    with open(script_filename, 'r', encoding='utf-8') as file:
        shell_script = file.read()

    commands_list = shell_script.strip().split('\n')

    request = {
        "DocumentName": "AWS-RunShellScript",
        "DocumentVersion": "1",
        "InstanceIds": [instance_id],
        "Parameters": {
            "workingDirectory": [""],
            "executionTimeout": ["3600"],
            "commands": commands_list
        },
        "TimeoutSeconds": 600
    }

    return request

script_filename = input("変換したいシェルのファイル名を入力してください: ")
instance_id = input("シェルを実行する対象のEC2のインスタンスIDを入力してください: ")

script_filename = 'sqs_reinsertion.sh'
send_command_request = build_send_command(script_filename, instance_id)

print(json.dumps(send_command_request, indent=5))