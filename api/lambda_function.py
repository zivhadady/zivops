import json
import os

def lambda_handler(event, context):
    # Default company name
    company_name = "Guest"
    
    # Check if the company name was passed in the query string (e.g. ?company=AcmeCorp)
    if event.get('queryStringParameters') and 'company' in event['queryStringParameters']:
        company_name = event['queryStringParameters']['company']
    # Check if passed in the JSON body for POST requests
    elif event.get('body'):
        try:
            body = json.loads(event['body'])
            if 'company' in body:
                company_name = body['company']
        except Exception:
            pass

    # Personalized greeting
    message = f"Hello {company_name}! Ready to optimize your DevOps infrastructure?"
    
    # Securely retrieve the calendar link from environment variables
    calendar_link = os.environ.get('CALENDAR_LINK', 'Link not configured.')

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': message,
            'company': company_name,
            'appointment_link': calendar_link
        })
    }
