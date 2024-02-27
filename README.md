# browser-io

Save all tabs of your multiple browsers in a single json.

This is done by getting tabs in 
- firefox (and firefox-based?) - `.../.mozilla/firefox/*.default/sessionstore-backups/recovery.jsonlz4`
- brave (and chromium-based?) - `.../BraveSoftware/Brave-Browser/Default/Sessions/Tabs_*`

## deps 

```
sudo apt install lz4json # parse lz4 format for firefox json
```

## Further objectives 

- support more browsers (probably easy for firefox based and chromium based browsers)
- implement way of extracting browser's history 

## Other info

firefox has `places.sqlite` for websites visited
For an export of firefox history.

### sqlite `places.sqlite`

sqlite3 places.sqlite "select \* from moz_places"

sqlite3> .mode json
sqlite3> .once out.json
sqlite3> SELECT \* from foo;
