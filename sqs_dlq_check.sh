#!/bin/bash

DLQ_QUEUE_URL=""
REGION="ap-northeast-1"

# メッセージ数を取得
DLQ_COUNT=$(aws sqs get-queue-attributes --queue-url "$DLQ_QUEUE_URL" --attribute-names ApproximateNumberOfMessages --query 'Attributes.ApproximateNumberOfMessages' --output text --region "$REGION")
echo $DLQ_COUNT

# メッセージ再投入
for (( i=0; i<$DLQ_COUNT; i++ ))
do

    RESULT=$(aws sqs receive-message --queue-url "${TMP_DLQ_QUEUE_URL}" --max-number-of-messages "1" --region "$REGION")
    echo $RESULT

    BODY=$(echo $RESULT | jq -r '.Messages[].Body' | sed -e "s/,\$//")
    RECEIPTHANDLE=$(echo $RESULT | jq -r ".Messages[].ReceiptHandle" | sed -e "s/,\$//")

    aws sqs send-message --queue-url "" --message-body "${BODY}" --region "$REGION"

    aws sqs delete-message --queue-url "${TMP_DLQ_QUEUE_URL}" --receipt-handle "${RECEIPTHANDLE}" --region "$REGION"

done