import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb')
results_table = boto3.resource('dynamodb').Table('results_table')
player_table = boto3.resource('dynamodb').Table('player_table')

def convert(item):
    #Converts a json tuple into a single string
    preitem = tuple(item.items())[0]
    postitem = tuple(preitem)[1]
    return postitem

def get_teams(date):
    try:
        print(f"Getting teams for date: {date}")
        response = dynamodb.get_item(
            Key={
                'Date': {'S': str(date)}
            },
            TableName='results_table',
        )
        if 'Item' not in response:
            raise Exception('Date Not Found')

        teama = []
        teama.append(response['Item']['Team A Player 1']['S'])
        teama.append(response['Item']['Team A Player 2']['S'])
        teama.append(response['Item']['Team A Player 3']['S'])
        teama.append(response['Item']['Team A Player 4']['S'])
        teama.append(response['Item']['Team A Player 5']['S'])
        teamb = []
        teamb.append(response['Item']['Team B Player 1']['S'])
        teamb.append(response['Item']['Team B Player 2']['S'])
        teamb.append(response['Item']['Team B Player 3']['S'])
        teamb.append(response['Item']['Team B Player 4']['S'])
        teamb.append(response['Item']['Team B Player 5']['S'])
        
        # totala = response['Item']['Team A Total']['N']
        # totalb = response['Item']['Team B Total']['N']

        # coloura = response['Item']['Team A Colour']['S']
        # colourb = response['Item']['Team B Colour']['S']

        # scorea = response['Item']['Team A Result?']['S']
        # scoreb = response['Item']['Team B Result?']['S']

        totala = response['Item']['Team A Total']
        totala = convert(totala)
        totalb = response['Item']['Team B Total']
        totalb = convert(totalb)

        coloura = response['Item']['Team A Colour']['S']
        colourb = response['Item']['Team B Colour']['S']

        scorea = response['Item']['Team A Result?']
        scorea = convert(scorea)
        scoreb = response['Item']['Team B Result?']
        scoreb = convert(scoreb)

        return teama,teamb,scorea,scoreb,coloura,colourb,totala,totalb
    except ClientError as e:
        raise Exception(f'Error getting values: {e}')