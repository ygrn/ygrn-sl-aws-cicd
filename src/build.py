def handler(event, context):

    data = event['body']
    print(data)

    return {"statusCode": 200}