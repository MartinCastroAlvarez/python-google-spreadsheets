# wolverine v2.11
Library for managing your Google Sheets.

![logo](/logo.png)

### Flow
[Wolverine](https://github.com/valleyworks/wolverine.git)
allows you to download CSV files from Google Sheets.

![flow](/flow.png)

### Installation
```
pip install -e git+ssh://git@github.com/valleyworks/wolverine.git#egg=wolverine -I
echo "-e git+ssh://git@github.com/valleyworks/wolverine.git#egg=wolverine" >> requirements.txt
```

### Environment
Set your environment variables.
```
GOOGLE_PRIVATE_KEY_ID=""
GOOGLE_PRIVATE_KEY=""
GOOGLE_CLIENT_EMAIL=""
GOOGLE_CLIENT_ID=""
GOOGLE_TYPE=""
```

### Export
Export Google Sheet to JSON.
```
from wolverine import Wolverine

w = Wolverine('23192312-12312-123-123')
j = w.getCells("TestSheet", (1,2), (4, 5))
```

### Dimensions
Get Google Sheet dimensions.
```
from wolverine import Wolverine

w = Wolverine('23192312-12312-123-123')
total_rows = w.getTotalRows("TestSheet")
total_columns = w.getTotalColumns("TestSheet")
```

### Iteration
Iterate over all rows in the Google Sheet.
```
from wolverine import Wolverine

w = Wolverine('23192312-12312-123-123')
for row in w.iterator("TestSheet"):
    print(row)
```
