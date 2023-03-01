from src.utils import get_date, get_teams
import boto3
from botocore.exceptions import ClientError
from dynamo_pandas import get_df
import pandas as pd

dynamodb = boto3.client('dynamodb')
results_table = boto3.resource('dynamodb').Table('results_table')
player_table = boto3.resource('dynamodb').Table('player_table')

def get_results():
    date = str(get_date.closest_wednesday)
    teama,teamb,scorea,scoreb,coloura,colourb,totala,totalb = get_teams.get_teams(date)
    #Check if scorea is a dash
    print(f"ScoreA is a {scorea}")
    if scorea != "-":
        results_df = get_df(table="results_table")
        results_df = results_df.filter(['Date',
                                'Team A Result?',
                                'Team B Result?',
                                'Team A Total',
                                'Team B Total',
                                'Team A Player 1',
                                'Team A Player 2',
                                'Team A Player 3',
                                'Team A Player 4',
                                'Team A Player 5',
                                'Team B Player 1',
                                'Team B Player 2',
                                'Team B Player 3',
                                'Team B Player 4',
                                'Team B Player 5',
                                'Team A Colour',
                                'Team B Colour'])
        results_df['Date'] = pd.to_datetime(results_df.Date, 
                                        format='%Y%m%d', errors='ignore')
        results_df['Team A Result?'] = pd.to_numeric(
                                        results_df['Team A Result?'])
        results_df['Team B Result?'] = pd.to_numeric(
                                        results_df['Team B Result?'])
        return results_df
    else:
        print("Cannot run formulas due to dash!")
        return

def calc_wdl(player, df):
    '''Calculate wins,draws,losses for each player
    Where player is on the team and result 
    is WDL based on which team they were on'''

    teama = ['Team A Player 1','Team A Player 2','Team A Player 3','Team A Player 4','Team A Player 5']
    teamb = ['Team B Player 1','Team B Player 2','Team B Player 3','Team B Player 4','Team B Player 5']
    wins = 0
    draws = 0
    losses = 0

    for team in teama:
        wins = wins + df[(df[team] == player) & (df['Team A Result?'] > df['Team B Result?'])].shape[0]
        draws = draws + df[(df[team] == player) & (df['Team A Result?'] == df['Team B Result?'])].shape[0]
        losses = losses + df[(df[team] == player) & (df['Team A Result?'] < df['Team B Result?'])].shape[0]

    for team in teamb:
        wins = wins + df[(df[team] == player) & (df['Team A Result?'] < df['Team B Result?'])].shape[0]
        draws = draws + df[(df[team] == player) & (df['Team A Result?'] == df['Team B Result?'])].shape[0]
        losses = losses + df[(df[team] == player) & (df['Team A Result?'] > df['Team B Result?'])].shape[0]
    return wins,draws,losses

def update_formulas():
    '''Updates formulas'''
    date = str(get_date.closest_wednesday)
    teama,teamb,scorea,scoreb,coloura,colourb,totala,totalb = get_teams.get_teams(date)
    #Check if scorea is a dash
    print(f"ScoreA is a {scorea}")
    if scorea != "-":
        played_thisweek = teama + teamb
        df = get_results()
        for name in played_thisweek:
            calc = calc_wdl(name,df)
            wins = calc[0]
            draws = calc[1]
            losses = calc[2]
            score = int(wins) * 3 + int(draws)
            played = int(wins) + int(draws) + int(losses)
            percentage = int(wins) / int(played) * 100
            percentage = int(percentage)
            if int(wins) < 5:
                winpercentage = '0'
            else:
                winpercentage = percentage
            try:
                player_table.update_item(
                    Key={'Name': name},
                    UpdateExpression="set Wins=:w, Draws=:d, Losses=:l, Score=:s, Played=:p, #pc=:pc, #wp=:wp",
                    ExpressionAttributeNames={
                        '#pc': 'Percent Calc',
                        '#wp': 'Win Percentage'},
                    ExpressionAttributeValues={
                        ':w': wins,
                        ':d': draws,
                        ':l': losses,
                        ':s': score,
                        ':p': played,
                        ':pc': percentage,
                        ':wp': winpercentage},
                    ReturnValues="UPDATED_NEW"
                )
            except ClientError as e:
                raise Exception(f'Error updating values: {e}')
    return