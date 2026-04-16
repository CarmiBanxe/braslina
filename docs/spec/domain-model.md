# Domain Model — ERD

> Text-based ERD for braslina database schema.

merchants

id PK str "mer_XXXXXXXX"
name str
website str
mcc str
status str default="new"
created_at datetime
updated_at datetime

checklists

id PK str "mcl_XXXXXXXX"
merchant_id FK -> merchants.id
template_id str
created_at datetime
completed_at datetime (nullable)

check_items

id PK str "chi_XXXXXXXX"
checklist_id FK -> checklists.id
name str
description text
auto_verifiable bool
status str default="pending"
verified_at datetime (nullable)
evidence_url str (nullable)
notes text (nullable)

snapshots

id PK str "snp_XXXXXXXX"
merchant_id FK -> merchants.id
url str
screenshot_path str
diff_pct float (nullable)
has_changes bool
created_at datetime

test_purchases

id PK str "tpr_XXXXXXXX"
merchant_id FK -> merchants.id
amount float
currency str
result str
performed_by str
performed_at datetime
notes text (nullable)

## Relationships

- merchants 1 --< checklists (one merchant, many checklists)
- checklists 1 --< check_items (one checklist, many items)
- merchants 1 --< snapshots (one merchant, many snapshots)
- merchants 1 --< test_purchases (one merchant, many purchases)
