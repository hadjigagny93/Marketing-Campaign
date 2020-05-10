import os
import logging

# By default the data is stored in this repository's "data/" folder.
# You can change it in your own settings file.
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DATA_DIR = os.path.join(REPO_DIR, 'data')
OUTPUTS_DIR = os.path.join(REPO_DIR, 'outputs')
LOGS_DIR = os.path.join(REPO_DIR, 'logs')
MODELS_DIR = os.path.join(REPO_DIR, 'src/application/models/joblib_load')


# TESTS_DIR = os.path.join(REPO_DIR, 'tests')
# TESTS_DATA_DIR = os.path.join(TESTS_DIR, 'fixtures')


# Logging
def enable_logging(log_filename, logging_level=logging.DEBUG):
    """Set loggings parameters.

    Parameters
    ----------
    log_filename: str
    logging_level: logging.level

    """
    with open(os.path.join(LOGS_DIR, log_filename), 'a') as file:
        file.write('\n')
        file.write('\n')

    LOGGING_FORMAT = '[%(asctime)s][%(levelname)s][%(module)s] - %(message)s'
    LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    logging.basicConfig(
        format=LOGGING_FORMAT,
        datefmt=LOGGING_DATE_FORMAT,
        level=logging_level,
        filename=os.path.join(LOGS_DIR, log_filename)
    )

#Columns to First file
DATE = "DATE"
AGE_COL = "AGE"
JOB_TYPE_COL = "JOB_TYPE"
STATUS_COL = "STATUS"
EDUCATION_COL = "EDUCATION"
HAS_DEFAULT_COL = 'HAS_DEFAULT'
BALANCE_COL = 'BALANCE'
HAS_HOUSING_LOAN_COL = 'HAS_HOUSING_LOAN'
HAS_PERSO_LOAN_COL = 'HAS_PERSO_LOAN'
CONTACT_COL = 'CONTACT'
DURATION_CONTACT_COL = 'DURATION_CONTACT'
NB_CONTACT_COL = "NB_CONTACT"
NB_DAY_LAST_CONTACT_COL = "NB_DAY_LAST_CONTACT"
NB_CONTACT_LAST_CAMPAIGN_COL = 'NB_CONTACT_LAST_CAMPAIGN'
RESULT_LAST_CAMPAIGN_COL = "RESULT_LAST_CAMPAIGN"
SUBSCRIPTION_COL = "SUBSCRIPTION"

#Columns to second file

EMPLOYMENT_VARIATION_RATE_COL = "EMPLOYMENT_VARIATION_RATE"
IDX_CONSUMER_PRICE_COL = "IDX_CONSUMER_PRICE"
IDX_CONSUMER_CONFIDENCE_COL = "IDX_CONSUMER_CONFIDENCE"
NB_EMPLOYE_COL = "NB_EMPLOYE"


DEFAULT_DATA = "data.csv"
ADDITIONAL_DATA = "socio_eco.csv"

RENTREE_COL = "RENTREE"
PREVIOUS_CONTACT_COL = "PREVIOUS_CONTACT"

# pipelines
NUM_FEATURES = [AGE_COL, BALANCE_COL, NB_CONTACT_LAST_CAMPAIGN_COL, EMPLOYMENT_VARIATION_RATE_COL, IDX_CONSUMER_PRICE_COL, IDX_CONSUMER_CONFIDENCE_COL, NB_EMPLOYE_COL]
CAT_FEATURES = [JOB_TYPE_COL, NB_CONTACT_COL, STATUS_COL, EDUCATION_COL, RENTREE_COL, PREVIOUS_CONTACT_COL, HAS_DEFAULT_COL, HAS_HOUSING_LOAN_COL, HAS_HOUSING_LOAN_COL, HAS_PERSO_LOAN_COL, RESULT_LAST_CAMPAIGN_COL]


UNUSEFUL_FEATURES = [CONTACT_COL, DURATION_CONTACT_COL, DATE, NB_DAY_LAST_CONTACT_COL]


