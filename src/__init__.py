import pydash as _
import defintions
import sys
import spotipy
import spotipy.util as util


def login(username, scope):
    token = util.prompt_for_user_token(username,
                                       scope,
                                       client_id=defintions.SPOTIPY_CLIENT_ID,
                                       client_secret=defintions.SPOTIPY_CLIENT_SECRET,
                                       redirect_uri=defintions.SPOTIPY_REDIRECT_URI)

    if not token:
        print("Can't get token for", username)
        sys.exit()

    return token


def get_track_data(track):
    track = track['track']
    fields = dict(
        id='id',
        artist_name='artists.0.name',
        artist_id='artists.0.id',
        popularity='popularity',
        duration_ms='duration_ms',
        name='name'
    )
    return {track.get('id') : {k: _.get(track, v, '') for k, v in fields.items()}}


def main(username, playlist_name):
    token = login(username, 'user-library-read')
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_playlists()
    playlist = _.find(results['items'], lambda x: x['name'] == playlist_name)

    if playlist is None:
        print('Playlist: %s not found', playlist_name)
        sys.exit()

    playlist_id = playlist.get('id')
    playlist_track_data = sp.user_playlist(sp.me()['id'], playlist_id, fields=['tracks, next'])

    if not playlist_track_data:
        print('Retrieving data for Playlist Id: %s failed', playlist_id)
        sys.exit()

    tracks = _.map_(playlist_track_data['tracks']['items'], get_track_data)
    arists_ids = [v.get('artist_id') for t in tracks for k,v in t.items()]
    tracks_ids = [k for t in tracks for k,v in t.items()]
    artists = sp.artists(arists_ids)
    features = sp.audio_features(tracks_ids)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: %s username playlist_name" % (sys.argv[0],))
        sys.exit()

    main(sys.argv[1], sys.argv[2])
