# MPATS – Media Planning and Ad Trafficking System
## Test Cases

> **Source:** Scenarios identified from `vlc-record-2026-05-12-12h51m43s-MPATS Sales Media Planning Internal Demo by Yashwant.mp4-.mp4`  
> **System under test:** MPATS QA – `mpats-qa.nba-hq.com`

---

## Module 1: Advertiser Deals

---

### TC-001: Deals List Loads Successfully

| Field | Detail |
|---|---|
| **Test Case ID** | TC-001 |
| **Scenario** | Scenario 1 – View Advertiser Deals List |
| **Title** | Deals list page loads and displays deal records |
| **Priority** | High |
| **Type** | Functional / UI |

**Pre-conditions:**
- User is logged in with at least read access.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Navigate to `mpats-qa.nba-hq.com/deals` | Deals list page loads without errors |
| 2 | Observe the page header | Header shows "Media Planning and Ad Trafficking System – NBA" |
| 3 | Observe the deal table columns | Columns present: Deal Id, Customer, SAP ID, Contract#, Deal Leader, Start Date, End Date, Deal Status |
| 4 | Verify at least one deal is listed | One or more deal rows are visible |
| 5 | Verify Deal Status values | Statuses are one of: Finalized, Finalized Revision, Pending, Contracted |

**Expected Outcome:** Page renders with all expected columns and populated deal rows.

---

### TC-002: Deal Row Data Integrity

| Field | Detail |
|---|---|
| **Test Case ID** | TC-002 |
| **Scenario** | Scenario 1 – View Advertiser Deals List |
| **Title** | Deal row displays correct data for a known deal |
| **Priority** | High |
| **Type** | Functional |

**Pre-conditions:**
- Deal ID 22838 (2K SPORTS) exists in the system.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Navigate to `/deals` | Deals list loads |
| 2 | Locate Deal ID **22838** | Row is present |
| 3 | Verify Customer column | Displays "2K SPORTS" |
| 4 | Verify SAP ID | Displays "0010001860" |
| 5 | Verify Contract# | Displays "GMP18083" |
| 6 | Verify Deal Leader | Displays "Mary O'Laughlin" |
| 7 | Verify Start Date | Displays "09/26/2018" |
| 8 | Verify End Date | Displays "09/30/2025" |
| 9 | Verify Deal Status | Displays "Finalized Revision" |

**Expected Outcome:** All field values match the expected data for Deal 22838.

---

### TC-003: Search Deals by Customer Name

| Field | Detail |
|---|---|
| **Test Case ID** | TC-003 |
| **Scenario** | Scenario 2 – Search / Filter Deals |
| **Title** | Deals list filters when user types in the search box |
| **Priority** | High |
| **Type** | Functional |

**Pre-conditions:**
- Multiple deals exist with different customer names.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Navigate to `/deals` | Deals list loads |
| 2 | Click the search / "Enter characters" input field | Input field is focused |
| 3 | Type "2K SPORTS" | List filters to show only deals whose Customer is "2K SPORTS" |
| 4 | Verify non-matching deals are hidden | Deals for 888sport, AB InBev, etc. are not visible |
| 5 | Clear the search field | Full deal list is restored |

**Expected Outcome:** The deals list dynamically filters based on typed text and restores on clear.

---

### TC-004: Saved Searches Panel Accessible

| Field | Detail |
|---|---|
| **Test Case ID** | TC-004 |
| **Scenario** | Scenario 2 – Saved Searches |
| **Title** | User can open and use the Saved Searches panel |
| **Priority** | Medium |
| **Type** | Functional / UI |

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Navigate to `/deals` | Deals page loads |
| 2 | Click **SAVED SEARCHES** in the sidebar | Saved Searches panel opens/expands |
| 3 | Verify saved searches are listed (if any exist) | Saved search entries are displayed |
| 4 | Click a saved search | Deals list filters to match that saved search criteria |

**Expected Outcome:** Saved Searches panel opens and applies selected filters.

---

### TC-005: Expand Deal Row to View Budget Summary

| Field | Detail |
|---|---|
| **Test Case ID** | TC-005 |
| **Scenario** | Scenario 3 – Expand Deal Budget Summary |
| **Title** | Expanding a deal row shows year-by-year budget totals |
| **Priority** | High |
| **Type** | Functional |

**Pre-conditions:**
- Deal 22838 (2K SPORTS) has at least one year of budget data.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Navigate to `/deals` | Deals list loads |
| 2 | Locate Deal 22838 | Row is visible |
| 3 | Click the expand icon on Deal 22838 row | Row expands to show budget sub-table |
| 4 | Verify sub-table columns for international deal | Columns: Year, International Total |
| 5 | Verify 2024 data | Year = 2024, International Total = $815,000.00 |
| 6 | Click expand again to collapse | Sub-table collapses; row returns to normal height |

**Expected Outcome:** Budget summary expands with correct year and amount data.

---

### TC-006: Expand Deal Row – Domestic Variance Display

| Field | Detail |
|---|---|
| **Test Case ID** | TC-006 |
| **Scenario** | Scenario 3 – Expand Deal Budget Summary |
| **Title** | Domestic deal expansion shows DMS vs Media variance |
| **Priority** | Medium |
| **Type** | Functional |

**Pre-conditions:**
- Deal 2469 (Academy Sports & Outdoors) exists with domestic budget data.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Navigate to `/deals` | Deals list loads |
| 2 | Locate Deal 2469 | Row is visible |
| 3 | Expand the deal row | Sub-table appears |
| 4 | Verify columns | Columns: Year, DMS Domestic Total, Media Total, Variance |
| 5 | Verify 2024 row values | DMS Domestic Total = $0.00, Media Total = $100,000.00, Variance = –$100,000.00 |

**Expected Outcome:** Variance column correctly shows the difference between DMS and Media totals.

---

## Module 2: Media Planning

---

### TC-007: Navigate to Media Planning Module

| Field | Detail |
|---|---|
| **Test Case ID** | TC-007 |
| **Scenario** | Scenario 4 – Navigate to Media Planning |
| **Title** | User navigates to Media Planning from the left navigation |
| **Priority** | High |
| **Type** | Navigation / UI |

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Log in and navigate to `/deals` | Deals page loads |
| 2 | Click **MEDIA PLANNING** in the left sidebar | Media Planning page loads |
| 3 | Verify the page URL or title | URL contains `/deals` context or dedicated media planning path; heading shows "MEDIA PLANNING" |
| 4 | Verify budget summary header | Header shows: Total Contractual Budget, Remaining Budget, Grand Total Booked |

**Expected Outcome:** Media Planning page loads with correct header budget figures.

---

### TC-008: Media Planning Dashboard Budget Summary Accuracy

| Field | Detail |
|---|---|
| **Test Case ID** | TC-008 |
| **Scenario** | Scenario 4 – Media Planning Dashboard |
| **Title** | Budget summary figures are correct for the selected deal |
| **Priority** | High |
| **Type** | Functional |

**Pre-conditions:**
- Deal 22838 (2K SPORTS) is selected; plans exist with known budget values.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open Media Planning for Deal 22838 | Media Planning page loads |
| 2 | Observe Total Contractual Budget | Displays **$815,000.00** |
| 3 | Observe Remaining Budget | Displays **$75,612.90** |
| 4 | Observe Grand Total Booked | Displays **$893,517.90** |
| 5 | Verify relationship: Grand Total > Total Budget | Grand Total Booked ($893,517.90) > Total Contractual ($815,000.00) – indicates over-commitment |

**Expected Outcome:** All three budget figures are correct and consistent.

---

### TC-009: Media Plan List Displays All Plans for Deal

| Field | Detail |
|---|---|
| **Test Case ID** | TC-009 |
| **Scenario** | Scenario 4 – Media Planning |
| **Title** | All media plans for a deal are listed on the Media Planning page |
| **Priority** | High |
| **Type** | Functional |

**Pre-conditions:**
- Deal 22838 (2K SPORTS) has 8+ media plans.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open Media Planning for Deal 22838 | Media Planning page loads |
| 2 | Count media plan rows | At least 8 plans are listed |
| 3 | Verify plan "NBA 2K Media Plan – 23/24" (Bill As Air) exists | Row is visible with Bill Type = "Bill As Air" |
| 4 | Verify plan "2K EME 23-24" exists | Row visible with Bill Type = "Contractual" |
| 5 | Verify plan "2K Paris Game Spot" exists | Row visible with Bill Type = "Contractual" |
| 6 | Verify column headers | Columns: Media Plan Name, Customer, Year, Bill Type |

**Expected Outcome:** All known plans for Deal 22838 are listed with correct data.

---

### TC-010: Create New Media Plan – Happy Path

| Field | Detail |
|---|---|
| **Test Case ID** | TC-010 |
| **Scenario** | Scenario 5 – Create New Media Plan |
| **Title** | User creates a new media plan with all required fields |
| **Priority** | High |
| **Type** | Functional |

**Pre-conditions:**
- User has write access. Deal is open in Media Planning view.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Click **Add Media Plan** button | Add Media Plan form/panel opens |
| 2 | Enter Media Plan Name: "Test Automation Plan" | Name field accepts input |
| 3 | Select Brand from dropdown | Brand is selected |
| 4 | Select Media AE | Media AE is selected |
| 5 | Select Market Type | Market Type is populated |
| 6 | Verify Status defaults to "Working Internal" | Status field shows "Working Internal" |
| 7 | Verify Bill Type defaults to "Contractual" | Bill Type field shows "Contractual" |
| 8 | Verify Bill By defaults to "NBA" | Bill By field shows "NBA" |
| 9 | Enter Plan Start Date: 10/01/2023 | Date is accepted |
| 10 | Enter Plan End Date: 09/30/2024 | Date is accepted |
| 11 | Click **Save** / **Submit** | Form is submitted without errors |
| 12 | Verify new plan appears in the list | "Test Automation Plan" is visible in the plan list |

**Expected Outcome:** New media plan is created and appears in the Media Planning list.

---

### TC-011: Create New Media Plan – Missing Required Fields

| Field | Detail |
|---|---|
| **Test Case ID** | TC-011 |
| **Scenario** | Scenario 5 – Create New Media Plan |
| **Title** | System shows validation errors when required fields are missing |
| **Priority** | High |
| **Type** | Negative / Validation |

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Click **Add Media Plan** | Form opens |
| 2 | Leave all fields blank | Form fields are empty |
| 3 | Click **Save** | Validation errors are displayed |
| 4 | Verify required field indicators | Required fields (e.g., Plan Name, Start Date, End Date) show error messages |

**Expected Outcome:** Form does not submit; meaningful validation messages appear for each required field.

---

### TC-012: Create Media Plan – End Date Before Start Date

| Field | Detail |
|---|---|
| **Test Case ID** | TC-012 |
| **Scenario** | Scenario 5 – Create New Media Plan |
| **Title** | System rejects media plan where End Date is before Start Date |
| **Priority** | High |
| **Type** | Negative / Validation |

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open Add Media Plan form | Form is visible |
| 2 | Enter Plan Start Date: 09/30/2024 | Date is entered |
| 3 | Enter Plan End Date: 01/01/2024 (before start) | Date is entered |
| 4 | Click **Save** | Error message displayed |
| 5 | Verify error message | Message indicates End Date cannot be before Start Date |

**Expected Outcome:** Form is not submitted; date validation error is shown.

---

### TC-013: Mark Media Plan as Primary

| Field | Detail |
|---|---|
| **Test Case ID** | TC-013 |
| **Scenario** | Scenario 5 – Create New Media Plan |
| **Title** | User can mark a plan as primary during creation |
| **Priority** | Medium |
| **Type** | Functional |

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open Add Media Plan form | Form is visible |
| 2 | Fill in all required fields | Fields populated |
| 3 | Check the **Mark as Primary** checkbox | Checkbox is checked |
| 4 | Click **Save** | Form submits |
| 5 | Open plan version list | The plan shows "Primary" flag = Yes |

**Expected Outcome:** The created plan is marked as the primary plan for the deal.

---

### TC-014: View Media Plan Versions

| Field | Detail |
|---|---|
| **Test Case ID** | TC-014 |
| **Scenario** | Scenario 6 – View Media Plan Versions |
| **Title** | User can view all versions of a media plan |
| **Priority** | High |
| **Type** | Functional |

**Pre-conditions:**
- Deal 22838, plan "NBA 2K Media Plan – 23/24" has at least 3 versions.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open Media Planning for Deal 22838 | Plan list loads |
| 2 | Click on "NBA 2K Media Plan – 23/24" | Plan detail / version list opens |
| 3 | Verify version table columns | Columns: Version, Plan ID, Market Type, Deal ID, Start Date, End Date, Planned Budget, Primary |
| 4 | Verify Version 2 row | Plan ID=1151, Market=Domestic, Deal=22838, 10/01/2023–09/30/2024, $568.00 |
| 5 | Verify Version 3 row | Plan ID=1152, Market=Domestic, Deal=22838, 10/01/2023–11/29/2024, $9,620.00 |
| 6 | Verify Version 4 row | Plan ID=1188, Market=Domestic, Deal=22838, 10/01/2023–01/28/2025, $4,500.00 |

**Expected Outcome:** All three versions display with correct details.

---

### TC-015: Primary Flag on Plan Version

| Field | Detail |
|---|---|
| **Test Case ID** | TC-015 |
| **Scenario** | Scenario 6 – View Media Plan Versions |
| **Title** | Only one version per plan is marked as Primary |
| **Priority** | Medium |
| **Type** | Functional / Business Rule |

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open Media Planning for Deal 22838 | Plan list loads |
| 2 | Open version list for "NBA 2K Media Plan – 23/24" | Version table displays |
| 3 | Count rows where Primary = Yes | Exactly 1 version has Primary = Yes |
| 4 | Note the primary version number | Record which version is primary (e.g., Version 2) |

**Expected Outcome:** Exactly one plan version is marked as Primary; others are not.

---

### TC-016: View Media Plan Line Items

| Field | Detail |
|---|---|
| **Test Case ID** | TC-016 |
| **Scenario** | Scenario 7 – View Media Plan Line Items |
| **Title** | User can drill into a plan version to view individual line items |
| **Priority** | High |
| **Type** | Functional |

**Pre-conditions:**
- Plan version 1151 has at least 2 line items.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open Media Planning for Deal 22838 | Plan list loads |
| 2 | Open plan "NBA 2K Media Plan – 23/24" Version 2 (Plan ID 1151) | Plan detail opens |
| 3 | Verify line item table columns | Columns: Country, Media, Start Date, End Date, Asset/Brand, Planned $ Amount |
| 4 | Verify Digital line item | US / Digital / 12/01/2023–12/31/2023 / NBA Media – 2K Sports / $2,000.00 |
| 5 | Verify TV-Game line item | US / TV-Game / 03/01/2024–03/31/2024 / G League Up Next Game – 2K Sports / $500.00 |

**Expected Outcome:** Line items display with correct country, media type, dates, asset, and planned amounts.

---

### TC-017: Line Item Planned Amount Totals Match Plan Budget

| Field | Detail |
|---|---|
| **Test Case ID** | TC-017 |
| **Scenario** | Scenario 7 – Media Plan Line Items |
| **Title** | Sum of line item amounts equals the plan version's Planned Budget |
| **Priority** | High |
| **Type** | Functional / Data Integrity |

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open plan version with known line items | Line items visible |
| 2 | Sum all Planned $ Amount values | Calculate total |
| 3 | Compare to Planned Budget shown in version header | Totals match (or the UI shows a reconciliation summary) |

**Expected Outcome:** Sum of line item planned amounts equals (or is reconciled against) the plan version budget.

---

### TC-018: Edit Media Plan – Update Status

| Field | Detail |
|---|---|
| **Test Case ID** | TC-018 |
| **Scenario** | Scenario 8 – Edit Existing Media Plan |
| **Title** | User can change the Status of an existing media plan |
| **Priority** | High |
| **Type** | Functional |

**Pre-conditions:**
- An existing plan with Status = "Working Internal" exists.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open Media Planning list | Plans visible |
| 2 | Click edit icon for target plan | Edit Media Plan panel opens |
| 3 | Verify form is pre-populated | Status = "Working Internal", Bill Type = "Contractual" |
| 4 | Change Status to a different value | Status dropdown updates |
| 5 | Click **Save** | Plan is saved |
| 6 | Reopen the plan | Updated Status value is displayed |

**Expected Outcome:** Plan status is updated and persisted correctly.

---

### TC-019: Edit Media Plan – Update Plan Dates

| Field | Detail |
|---|---|
| **Test Case ID** | TC-019 |
| **Scenario** | Scenario 8 – Edit Existing Media Plan |
| **Title** | User can update Plan Start and End dates of a media plan |
| **Priority** | High |
| **Type** | Functional |

**Pre-conditions:**
- A plan exists with Start Date 10/01/2023 and End Date 11/29/2024.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open edit form for the plan | Form opens pre-populated |
| 2 | Verify Plan Start Date: 10/01/2023 | Correct value shown |
| 3 | Verify Plan End Date: 11/29/2024 | Correct value shown |
| 4 | Change Plan End Date to 12/31/2024 | Date field updated |
| 5 | Click **Save** | Plan saved without errors |
| 6 | Reopen plan | End Date shows 12/31/2024 |

**Expected Outcome:** Updated dates are persisted correctly.

---

### TC-020: Edit Media Plan – Media Detail Section Visible

| Field | Detail |
|---|---|
| **Test Case ID** | TC-020 |
| **Scenario** | Scenario 8 – Edit Existing Media Plan |
| **Title** | Edit form shows Media Detail sub-section with line items |
| **Priority** | Medium |
| **Type** | UI / Functional |

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open edit form for an existing plan | Edit panel opens |
| 2 | Scroll to **Media Detail** section | Section is visible below Plan fields |
| 3 | Verify Media Detail columns | Columns: Media Type, Start Date, End Date, Mark, Confirm |
| 4 | Verify at least one media type row appears | One or more rows listed |

**Expected Outcome:** Media Detail section is visible within the Edit form with correct columns.

---

## Module 3: Backend / Integration

---

### TC-021: DMS Integration – Oracle Query Returns Deal Data

| Field | Detail |
|---|---|
| **Test Case ID** | TC-021 |
| **Scenario** | Scenario 9 – DMS Oracle Query |
| **Title** | DMSRepository Oracle query returns correct deal fields |
| **Priority** | High |
| **Type** | Integration / Backend |

**Pre-conditions:**
- Oracle database is connected. Deal data exists for date range used in test.
- `DMSIntegrationService` is running on Feature/MPATS-85 branch.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Invoke the DMS integration endpoint/method with a valid `fromDate` and `toDate` | Service executes without error |
| 2 | Verify the returned deal fields include: DEALNAME, AMOUNT, DEALSTATUS, CATEGORY, INVENTORY, DEALLEADER | All fields are non-null for active deals |
| 3 | Verify filter: `contentcount > 0` | Only deals with content are returned |
| 4 | Verify filter: `year > 2020` | Deals from 2020 or earlier are excluded |
| 5 | Verify filter: `lostdeal = 0` | Lost deals are excluded from results |
| 6 | Verify filter: `dealtype = 'GMP'` | Only GMP deals are returned |
| 7 | Verify date range filter | Only deals whose date falls within `fromDate`–`toDate` are returned |

**Expected Outcome:** Query returns correct deal records matching all filter criteria.

---

### TC-022: DMS Integration – Date Parameterization (SQL Injection Guard)

| Field | Detail |
|---|---|
| **Test Case ID** | TC-022 |
| **Scenario** | Scenario 9 – DMS Oracle Query |
| **Title** | Oracle query uses parameterized inputs; rejects malicious date values |
| **Priority** | High |
| **Type** | Security / Integration |

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Call integration with valid `fromDate` = "01/01/2024" and `toDate` = "12/31/2024" | Query executes successfully |
| 2 | Call integration with `fromDate` = `"' OR '1'='1"` (SQL injection attempt) | Query fails safely or returns empty set; no SQL injection executed |
| 3 | Call integration with `fromDate` = `null` | Service handles null gracefully; returns error or uses default date range |
| 4 | Call integration with invalid date format `fromDate` = "2024-01-01" (ISO instead of MM/DD/YYYY) | Appropriate error is returned (bad request or handled conversion) |

**Expected Outcome:** Parameterized queries prevent injection; invalid inputs return controlled errors.

---

### TC-023: SQL Partner Sync – Insert New Partner

| Field | Detail |
|---|---|
| **Test Case ID** | TC-023 |
| **Scenario** | Scenario 10 – SQL Partner Sync |
| **Title** | New partner record is inserted when no matching PartnerDetail exists |
| **Priority** | High |
| **Type** | Integration / Database |

**Pre-conditions:**
- `@CurCustomerId` = "NEW_CUSTOMER_001" does not exist in `PartnerDetail`.
- `@CurDealId` references a valid deal.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Execute DMS Advertiser Deal sync job with a new customer | Job runs |
| 2 | Verify no existing `PartnerDetail` row for `PSoftId='NEW_CUSTOMER_001'` and `PartnerType=501` | No pre-existing record |
| 3 | Run the upsert SQL logic | INSERT is executed |
| 4 | Query `PartnerDetail` for the new record | Row exists with: PartnerName, PartnerFullName, PSoftId='NEW_CUSTOMER_001', PartnerType=501, CreatedBy='DMSAdvertiserDealJob' |

**Expected Outcome:** New partner record is inserted with all correct fields.

---

### TC-024: SQL Partner Sync – Update Existing TBD Partner

| Field | Detail |
|---|---|
| **Test Case ID** | TC-024 |
| **Scenario** | Scenario 10 – SQL Partner Sync |
| **Title** | Existing PartnerDetail with TBD PSoftId is updated with real customer ID |
| **Priority** | High |
| **Type** | Integration / Database |

**Pre-conditions:**
- A `PartnerDetail` row exists with `PSoftId LIKE '%TBD%'` linked to a deal via `AdvertiserDeal`.
- `@CurCustomerId` contains the real customer ID (not TBD).

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Set up: create PartnerDetail with PSoftId='TBD_TEMP_001' | Record exists |
| 2 | Link to AdvertiserDeal for `@CurDealId` | AdvertiserDeal references the TBD partner |
| 3 | Execute DMS sync with the real customer ID `@CurCustomerId` = "REAL_ID_001" | Job executes |
| 4 | Query `PartnerDetail` for the record | PSoftId is updated to "REAL_ID_001" |
| 5 | Verify UpdatedBy and UpdatedDate | UpdatedBy='DMSAdvertiserDealJob', UpdatedDate = current date |

**Expected Outcome:** TBD partner record is updated with the real customer ID; no duplicate inserted.

---

### TC-025: SQL Partner Sync – Skip When CustomerID is Blank

| Field | Detail |
|---|---|
| **Test Case ID** | TC-025 |
| **Scenario** | Scenario 10 – SQL Partner Sync |
| **Title** | Partner insert/update is skipped when CurCustomerId is blank or null |
| **Priority** | Medium |
| **Type** | Negative / Database |

**Pre-conditions:**
- `@CurCustomerId` is NULL or empty string.

**Test Steps:**

| Step | Action | Expected Result |
|---|---|---|
| 1 | Execute DMS sync with `@CurCustomerId = NULL` | Sync runs |
| 2 | Check `PartnerDetail` for any new inserts by 'DMSAdvertiserDealJob' | No new records inserted for this customer |
| 3 | Verify `@partnerId` is not set / remains NULL | No partner ID resolved |

**Expected Outcome:** When `@CurCustomerId` is blank, the upsert block is skipped entirely.

---

## Summary of Test Cases

| TC ID | Title | Priority | Type | Scenario |
|---|---|---|---|---|
| TC-001 | Deals list loads successfully | High | Functional/UI | S1 |
| TC-002 | Deal row data integrity | High | Functional | S1 |
| TC-003 | Search deals by customer name | High | Functional | S2 |
| TC-004 | Saved searches panel accessible | Medium | Functional/UI | S2 |
| TC-005 | Expand deal row – budget summary | High | Functional | S3 |
| TC-006 | Expand deal row – domestic variance | Medium | Functional | S3 |
| TC-007 | Navigate to Media Planning module | High | Navigation/UI | S4 |
| TC-008 | Media Planning budget summary accuracy | High | Functional | S4 |
| TC-009 | Media plan list displays all plans | High | Functional | S4 |
| TC-010 | Create media plan – happy path | High | Functional | S5 |
| TC-011 | Create media plan – missing required fields | High | Negative/Validation | S5 |
| TC-012 | Create media plan – end date before start | High | Negative/Validation | S5 |
| TC-013 | Mark media plan as primary | Medium | Functional | S5 |
| TC-014 | View media plan versions | High | Functional | S6 |
| TC-015 | Primary flag – only one version primary | Medium | Functional/Business | S6 |
| TC-016 | View media plan line items | High | Functional | S7 |
| TC-017 | Line item totals match plan budget | High | Functional/Data | S7 |
| TC-018 | Edit media plan – update status | High | Functional | S8 |
| TC-019 | Edit media plan – update plan dates | High | Functional | S8 |
| TC-020 | Edit media plan – media detail visible | Medium | UI/Functional | S8 |
| TC-021 | DMS integration – Oracle query returns deal data | High | Integration | S9 |
| TC-022 | DMS integration – date parameterization (security) | High | Security | S9 |
| TC-023 | SQL partner sync – insert new partner | High | Integration/DB | S10 |
| TC-024 | SQL partner sync – update existing TBD partner | High | Integration/DB | S10 |
| TC-025 | SQL partner sync – skip when CustomerID is blank | Medium | Negative/DB | S10 |
