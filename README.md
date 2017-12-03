# wolverine v2.10
Library for managing your Google Sheets.

![alt text](/logo.png)

### Installation.
```
pip install -e git+ssh://git@github.com/valleyworks/wolverine.git#egg=wolverine -I
echo "-e git+ssh://git@github.com/valleyworks/wolverine.git#egg=wolverine" >> requirements.txt
```

### Set your environment variables.
```
GOOGLE_PRIVATE_KEY_ID=""
GOOGLE_PRIVATE_KEY=""
GOOGLE_CLIENT_EMAIL=""
GOOGLE_CLIENT_ID=""
GOOGLE_TYPE=""
```

### Export Google Sheet to JSON.
```
from wolverine import Wolverine

w = Wolverine('23192312-12312-123-123')
j = w.getCells("TestSheet", (1,2), (4, 5))
```

### Get Google Sheet dimensions.
```
from wolverine import Wolverine

w = Wolverine('23192312-12312-123-123')
w.getTotalRows("TestSheet")
w.getTotalColumns("TestSheet")
```

### Iterate over all rows in the Google Sheet.
```
from wolverine import Wolverine

w = Wolverine('23192312-12312-123-123')
for row in w.iterator("TestSheet"):
    print(row)
```
