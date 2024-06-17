import json

def build_send_command(script_filename):

    with open(script_filename, 'r', encoding='utf-8') as file:
        shell_script = file.read()

    # 改行で分割してリストにする
    commands_list = shell_script.strip().split('\n')

    request = {
        "DocumentName": "AWS-RunShellScript",
        "DocumentVersion": "1",
        "InstanceIds": ["hoge"],
        "Parameters": {
            "workingDirectory": [""],
            "executionTimeout": ["3600"],
            "commands": commands_list
        },
        "TimeoutSeconds": 600
    }

    return request

script_filename = "sqs_reinsertion.sh"

send_command_request = build_send_command_request(script_filename)

print(json.dumps(send_command_request, indent=2))
