import utils

ROOT_DIR = 'C:\Projects\DataScienceSpotify\\'
CONFIG_PATH = ROOT_DIR + 'config\config.yaml'

SPOTIPY_CLIENT_ID = utils.get_config()['keys']['clientId']
SPOTIPY_CLIENT_SECRET = utils.get_config()['keys']['secret']
SPOTIPY_REDIRECT_URI ='https://example.com/callback/'
