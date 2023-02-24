import logging
from src.utils import post_stats
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def main(event, context):

    print(event)
    print(context)

    try:
        post_stats.update_formulas()
    except ClientError as e:
        raise Exception(f'Error updating values: {e}')