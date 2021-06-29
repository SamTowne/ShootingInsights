import boto3
import json

def lambda_handler(event, context):

    ### Retrieve the shooting drill file ###
    s3 = boto3.resource("s3")
    shooting_insights_data_bucket = s3.Bucket('shooting-insights-data')
    processed_temp_file = []
    
    for obj in shooting_insights_data_bucket.objects.filter(Prefix="temp/3point/"):
      processed_temp_file = json.loads(obj.get()['Body'].read().decode('utf-8'))

    shots_made          = str(processed_temp_file['shots_made'])
    shots_attempted     = str(processed_temp_file['shots_attempted'])
    shooting_percentage = str(processed_temp_file['shooting_percentage'])
    temp                = str(processed_temp_file['temp'])

    ### Retrieve the Athena Results
    athena_client = boto3.client('athena')
    total_made_each_spot_query_results = athena_client.get_query_results(QueryExecutionId=processed_temp_file['total_made_each_spot_athena_execution_id'])
    rows = total_made_each_spot_query_results['ResultSet']['Rows']
    row2 = rows[1]
    data = row2['Data']
    values = []
    
    for item in data:
        values.append(int(item['VarCharValue']))

    total_shooting_drills = values[0]
    total_shot_attempts = values[1]
    shots_made_1 = values[2]
    shots_made_2 = values[3]
    shots_made_3 = values[4]
    shots_made_4 = values[5]
    shots_made_5 = values[6]
    shots_made_6 = values[7]
    shots_made_7 = values[8]
    shots_made_8 = values[9]
    shots_made_9 = values[10]
    shots_made_10 = values[11]
    shots_made_11 = values[12]

    total_shot_attemps_for_single_spot = float((total_shooting_drills*4))
    
    # Athena Result Calculations
    total_shots_made = shots_made_1 + shots_made_2 + shots_made_3 + shots_made_4 + shots_made_5 + shots_made_6 + shots_made_7 + shots_made_8 + shots_made_9 + shots_made_10 + shots_made_11
    total_shooting_percentage = round(100 * float(total_shots_made)/float(total_shot_attempts),2)
    spot1_percentage = round(100 * float(shots_made_1)/total_shot_attemps_for_single_spot,2)
    spot2_percentage = round(100 * float(shots_made_2)/total_shot_attemps_for_single_spot,2)
    spot3_percentage = round(100 * float(shots_made_3)/total_shot_attemps_for_single_spot,2)
    spot4_percentage = round(100 * float(shots_made_4)/total_shot_attemps_for_single_spot,2)
    spot5_percentage = round(100 * float(shots_made_5)/total_shot_attemps_for_single_spot,2)
    spot6_percentage = round(100 * float(shots_made_6)/total_shot_attemps_for_single_spot,2)
    spot7_percentage = round(100 * float(shots_made_7)/total_shot_attemps_for_single_spot,2)
    spot8_percentage = round(100 * float(shots_made_8)/total_shot_attemps_for_single_spot,2)
    spot9_percentage = round(100 * float(shots_made_9)/total_shot_attemps_for_single_spot,2)
    spot10_percentage = round(100 * float(shots_made_10)/total_shot_attemps_for_single_spot,2)
    spot11_percentage = round(100 * float(shots_made_11)/total_shot_attemps_for_single_spot,2)
        
    ### Send an email using Simple Email Service ###

    SENDER = "Sender Name <chmod777recursively@gmail.com>"
    RECIPIENT = "chmod777recursively@gmail.com"
    AWS_REGION = "us-east-1"
    SUBJECT = "Shooting Insights"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = "Dear Samuel, You made " + shots_made + " shots out of " + shots_attempted + "." + "\r\n" + "The data from this shooting drill was stored to an AWS S3 Bucket."
    #BODY_HTML = "test html body " + str(json.loads(processed_temp_file))
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
      <h3>Shooting Drill Results </h3>
      <p>You made <b>{_shots_made} shots</b> out of {_shots_attempted}.</p>
      <p>Your shooting percentage was <b>{_shooting_percentage}%</b>.</p>
      <p>The temperature was <b>{_temp}&deg;F</b>.</p>
      <br>
      <h3>Shooting Stats (all time)</h3>
      <h4> 3 Point Shooting Drill </h4>
      <p>Data collected from <b>{_total_shooting_drills}</b> shooting drills with 44 shot attempts each.
      <br>
      <p>3 Point Shooting Percentage: {_total_shooting_percentage}%.</p>
      <p>Spot 1 Percentage: {_spot1_percentage}%.</p>
      <p>Spot 2 Percentage: {_spot2_percentage}%.</p>
      <p>Spot 3 Percentage: {_spot3_percentage}%.</p>
      <p>Spot 4 Percentage: {_spot4_percentage}%.</p>
      <p>Spot 5 Percentage: {_spot5_percentage}%.</p>
      <p>Spot 6 Percentage: {_spot6_percentage}%.</p>
      <p>Spot 7 Percentage: {_spot7_percentage}%.</p>
      <p>Spot 8 Percentage: {_spot8_percentage}%.</p>
      <p>Spot 9 Percentage: {_spot9_percentage}%.</p>
      <p>Spot 10 Percentage: {_spot10_percentage}%.</p>
      <p>Spot 11 Percentage: {_spot11_percentage}%.</p>
      <br>
      <h4>A serverless app by Sam Towne ¯\_(ツ)_/¯</h4>
    </body>
    </html>
                """.format(_shots_made=shots_made,
                _shots_attempted=shots_attempted,
                _shooting_percentage=shooting_percentage,
                _temp=temp,
                _total_shooting_drills=total_shooting_drills,
                _total_shooting_percentage=total_shooting_percentage,
                _spot1_percentage=spot1_percentage,
                _spot2_percentage=spot2_percentage,
                _spot3_percentage=spot3_percentage,
                _spot4_percentage=spot4_percentage,
                _spot5_percentage=spot5_percentage,
                _spot6_percentage=spot6_percentage,
                _spot7_percentage=spot7_percentage,
                _spot8_percentage=spot8_percentage,
                _spot9_percentage=spot9_percentage,
                _spot10_percentage=spot10_percentage,
                _spot11_percentage=spot11_percentage
                )            
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    ses_client = boto3.client('ses',region_name=AWS_REGION)
    
    # Send the email
    send_email_response = ses_client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
    )

    ### Invoke cleanup lambda (async)

    lambda_client = boto3.client("lambda")
    lambda_client.invoke(FunctionName='cleanup',
                     InvocationType='Event',
                     LogType='None'
                     )

    return {
        'statusCode': 200,
        'body': 'hi'
    }