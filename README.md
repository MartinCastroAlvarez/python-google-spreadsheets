# Wolverine
Google Spreadsheets CLI integration.

![alt text](/wallpaper.jpg)

### Setup your config
Update `$HOME/.wolverine` with the following:
```
{
    "ampush": {
        "private_key_id": "###",
        "private_key": "###",
        "client_email": "###",
        "client_id": "###",
        "type": "service_account"
    }
}
```
### Uploading a CSV to Google Sheets:
```
python3 wolverine.py upload --profile ampush --spreadsheet-id 1t90q05AOBAiO2k5jegM0F4WSO8kMvaPzQsSSsF3HtPw --worksheet-name "Sheet13" --file-path "/opt/ampush/payments/tmp/dataloss/results.csv"
```

### Iterate over all rows.
```
 python3 wolverine.py details --profile ampush --spreadsheet-id 1t90q05AOBAiO2k5jegM0F4WSO8kMvaPzQsSSsF3HtPw --worksheet-name "Sheet13"
```
