class Error:
    class NotFound:
        title = 'No lyrics :('
        message = 'Requested song is not available on Genius database.'

    class Request:
        title = 'Unable to reach to server'
        message = 'Connection timeout, Please try again.'

    class Spotify:
        title = 'No playing song on spotify'
        message = unicode("Could not get current spotify song. \n Either spotify is not running or no song is playing on spotify ")
