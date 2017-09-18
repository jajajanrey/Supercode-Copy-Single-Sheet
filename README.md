# Copy Sheet Tab to Another Spreadsheet

A [Supercode](http://gosupercode.com) function that copies a sheet to another spreadsheet.

## Sample Usage

[Supercode](http://gosupercode.com) SDK will be available after the launch.

```
import json
import pprint
import supercode

response = supercode.call(
    "super-code-function",
    "your-supercode-api-key",
    sheet_id="SPREADSHEET_ID",
    copy_to="DESTINATION_SPREADSHEET_ID",
    service_account_json={},
    new_name="",
    tab_id="ID_OF_SHEET_TAB",
)

    
pprint(response)
```

**Note:** Supercode has not been launched yet. This is for internal testing only.
