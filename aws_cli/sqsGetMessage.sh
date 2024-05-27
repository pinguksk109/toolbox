#!/bin/bash

# SQSキューのURLを指定
QUEUE_URL=""

# メッセージ数を取得
MESSAGE_COUNT=$(aws sqs get-queue-attributes --queue-url "$QUEUE_URL" --attribute-names ApproximateNumberOfMessages --query 'Attributes.ApproximateNumberOfMessages' --output text)

echo $MESSAGE_COUNT

for (( i=0; i<MESSAGE_COUNT; i++ )); do
        MESSAGE=$(aws sqs receive-message --queue-url "$QUEUE_URL")
        echo "$MESSAGE"
done
