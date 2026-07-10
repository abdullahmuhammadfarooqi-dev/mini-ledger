#blue print for schema
**1.table for user details**:
| column | type | description |
|--------|------|-------------|
| user_id | integer | primary key |
| name | text | user name |

**2.table for transactions**:
| column | type | description |
|--------|------|-------------|
| transaction_id | integer | primary key |
| account_id | integer | foreign key |
| amount_cents | integer | transaction amount |
| description | text | transaction description |
| created_at | date | transaction date |
**3. table for Account**:
| column | type | description |
|--------|------|-------------|
| account_id | integer | primary key |
| user_id | integer | foreign key |
| account_name | text | account name |
