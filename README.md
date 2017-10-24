# wolverine v2.1
Managers ValleyWorks Google Sheets.

![alt text](/logo.png)

### Installation.
```
pip install -e git+ssh://git@github.com/valleyworks/wolverine.git#egg=wolverine -I
echo "-e git+ssh://git@github.com/valleyworks/wolverine.git#egg=wolverine" >> requirements.txt
```

### Export to JSON
```
from wolverine import Wolverine

w = Wolverine('23192312-12312-123-123')
j = w.getCells("TestSheet", (1,2), (4, 5), "COLUMNS")
w.getTotalRows("TestSheet")
w.getTotalColumns("TestSheet")
for row in w.iterator("TestSheet"):
    print(row)
```
