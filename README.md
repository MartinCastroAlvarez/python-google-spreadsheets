# wolverine 3.1
Library for managing your Google Sheets.

![logo](/.readme/logo.png)


![flow](/.readme/flow.png)

# Installation
### Python Eggs
Install this library as a dependency in your project.
```
pip install -e git+ssh://git@github.com/valleyworks/wolverine.git#egg=wolverine-I
echo "-e git+ssh://git@github.com/valleyworks/wolverine.git#egg=wolverine" >> requirements.txt
```
# Configuration
The following environment variables are required:
```
export GOOGLE_PRIVATE_KEY_ID='...'
export GOOGLE_PRIVATE_KEY='...'
export GOOGLE_CLIENT_EMAIL='...'
export GOOGLE_CLIENT_ID='...'
export GOOGLE_TYPE='...'
```
You can also set the following variables if running in a test environment:
```
export DEBUG='yes'
export PYTEST='yes'
```
# Usage
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
