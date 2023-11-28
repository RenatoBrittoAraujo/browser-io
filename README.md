# First iteration

- Save all open tabs in current firefox sessions to file.
- Load file as tabs in firefox.
- Default file of websites easily loads.

- for brave
- for TOR?

research:
- https://github.com/balta2ar/brotab#brotab (does what this is supposed to do)
- - sudo apt install pipx; pipx install brotab

- switch from 
/home/renato/.mozilla
to
/home/renato/snap/firefox/common/.mozilla

# second iteration

Found command that gets recovery info from firefox

The file is at `$MOZILLA_FOLDER/firefox/{...}.default/sessionstore-backups/recovery.jsonlz4`

The file format is weird, convert to json

INSTALL `lz4json`




