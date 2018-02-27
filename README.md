# wolverine v3.3
#### *Library for managing your Google Sheets.*

![logo](/.readme/logo.png)


![flow](/.readme/flow.png)

# Installation
Install this library as a dependency in your project.
```
pip install -e git+ssh://git@github.com/valleyworks/wolverine.git#egg=wolverine-I
echo "-e git+ssh://git@github.com/valleyworks/wolverine.git#egg=wolverine" >> requirements.txt
```
# Configuration
The following environment variables are required:
- [ ] GOOGLE_PRIVATE_KEY_ID
- [ ] GOOGLE_PRIVATE_KEY
- [ ] GOOGLE_CLIENT_EMAIL
- [ ] GOOGLE_CLIENT_ID
- [ ] GOOGLE_TYPE

You can also set the following variables if running in a test environment:
- [ ] DEBUG
- [ ] PYTEST
# Test Coverage
This code has been tested by Rogue and the test coverage is:
```
64%
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
