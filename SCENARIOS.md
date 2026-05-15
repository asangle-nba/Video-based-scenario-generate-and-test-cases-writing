# MPATS – Media Planning and Ad Trafficking System
## Identified Scenarios from Demo Video

> **Source video:** `vlc-record-2026-05-12-12h51m43s-MPATS Sales Media Planning Internal Demo by Yashwant.mp4-.mp4`  
> **System URL (QA):** `mpats-qa.nba-hq.com`  
> **Demo Duration:** ~8 min 29 s

---

## Overview

MPATS (Media Planning and Ad Trafficking System) is the NBA's internal platform for managing sponsorship deals and media plans. The demo covers two primary functional areas:

1. **Advertiser Deals Management** – searching, viewing, and navigating deals
2. **Media Planning** – creating, viewing, editing, and managing media plans and their line items

---

## Scenario 1 – View Advertiser Deals List

**Video Timestamp:** 0 s – 90 s  
**Module:** Advertisers / Deals

**Description:**  
A user lands on the Deals landing page and views the full list of sponsorship deals. Deals are displayed in a paginated table with the following columns: Deal ID, Customer, SAP ID, Contract#, Deal Leader, Start Date, End Date, and Deal Status.

**Pre-conditions:**
- User is authenticated and has at least read access.

**Steps observed:**
1. Navigate to `mpats-qa.nba-hq.com/deals`.
2. The system displays a list of deals sorted by default order.
3. Each row shows: Deal Id, Customer name, SAP ID, Contract number, Deal Leader, Start Date, End Date, Deal Status.

**Deal statuses visible in demo:**
| Deal Status | Description |
|---|---|
| Finalized | Deal fully executed |
| Finalized Revision | Deal executed but amended |
| Pending | Deal not yet finalized |
| Contracted | Deal contracted |

**Sample deals visible:**
| Deal ID | Customer | SAP ID | Contract# | Deal Leader | Start Date | End Date | Status |
|---|---|---|---|---|---|---|---|
| 22838 | 2K SPORTS | 0010001860 | GMP18083 | Mary O'Laughlin | 09/26/2018 | 09/30/2025 | Finalized Revision |
| 40686 | 2K SPORTS | 0010001860 | GMP18083 | Mary O'Laughlin | 12/05/2023 | 12/31/2023 | Finalized |
| 40842 | 888sport | 0010002628 | GMP34667 | David Keeley | 02/01/2024 | 09/30/2026 | Pending |
| 33240 | AB InBev/Labatt | 0010000941 | GMP27805 | David Keeley | 10/01/2021 | 09/30/2024 | Finalized Revision |
| 27401 | Abu Dhabi – DCT | 0010003116 | GMP22326 | David Watts | 11/10/2021 | 10/31/2025 | Contracted |
| 2469 | Academy Sports & Outdoors | 00TBD00618 | – | Sandeep Hundiwale | 10/01/2023 | 11/29/2024 | – |
| 40440 | ACCOR | 0010002600 | GMP34285 | Nick Cowell | 10/01/2023 | 06/30/2024 | – |
| 32520 | ADIDAS | 0010000001 | GMP27105 | Sasha Swerdlow | 10/01/2021 | 06/30/2025 | Pending |
| 40762 | ADQ | 0010003497 | GMP32225 | David Watts | 01/01/2024 | 09/30/2025 | Pending |

---

## Scenario 2 – Search / Filter Deals (Saved Searches)

**Video Timestamp:** 0 s – 90 s  
**Module:** Advertisers / Saved Searches

**Description:**  
The Deals page provides a **Saved Searches** panel and inline character search. A user can filter deals by typing into the search bar or applying a saved search.

**Steps observed:**
1. Click the **SAVED SEARCHES** tab in the left sidebar.
2. Optionally enter characters in the "Enter characters" search field.
3. The deals list filters in real time.

---

## Scenario 3 – Expand Deal to View Budget Summary

**Video Timestamp:** 210 s – 270 s  
**Module:** Advertisers / Deals / Deal Expansion

**Description:**  
Each deal row can be expanded to reveal a year-by-year budget summary. The expansion shows International Total and DMS vs Media budget variance.

**Steps observed:**
1. Locate a deal in the list (e.g., Deal 22838 – 2K SPORTS).
2. Click the expand icon on the deal row.
3. The row expands to show a sub-table: **Year | International Total**.
4. Separately, another deal (Academy Sports #2469) shows: **Year | DMS Domestic Total | Media Total | Variance**.
   - Example: 2024 | $0 | $100,000.00 | –$100,000.00

**Sample budget expansion for 2K SPORTS (Deal 22838):**
| Year | International Total |
|---|---|
| 2024 | $815,000.00 |

**Sample budget expansion for Academy Sports (Deal 2469):**
| Year | DMS Domestic Total | Media Total | Variance |
|---|---|---|---|
| 2024 | $0.00 | $100,000.00 | –$100,000.00 |

---

## Scenario 4 – Navigate to Media Planning for a Deal

**Video Timestamp:** ~300 s  
**Module:** Media Planning

**Description:**  
From the Deals page, a user navigates into the **Media Planning** module. The Media Planning view shows a list of media plans linked to the selected deal (e.g., Deal 22838 – 2K SPORTS).

**Steps observed:**
1. From the left navigation, click **MEDIA PLANNING**.
2. The system shows the Media Planning dashboard with budget summary header:
   - Total Contractual Budget: **$815,000.00**
   - Remaining Budget: **$75,612.90**
   - Grand Total Booked: **$893,517.90**
3. A list of media plans is displayed for the deal.

**Media plans visible for 2K SPORTS (Deal 22838):**
| Media Plan Name | Customer | Year | Bill Type |
|---|---|---|---|
| NBA 2K Media Plan – 23/24 | 2K SPORTS | 2024 | Bill As Air |
| 2K EME 23-24 | 2K SPORTS | 2024 | Contractual |
| 2K Paris Game Spot | 2K SPORTS | 2024 | Contractual |
| Media Plan | 2K SPORTS | 2024 | Contractual |
| test | 2K SPORTS | 2024 | Contractual |
| NBA 2K Media Plan – 23/24 | 2K SPORTS | 2024 | Contractual |
| Test Media Plan | 2K SPORTS | 2024 | Contractual |
| Test media | 2K SPORTS | 2024 | Contractual |

---

## Scenario 5 – Create a New Media Plan

**Video Timestamp:** ~360 s  
**Module:** Media Planning / Add Media Plan

**Description:**  
A user creates a new media plan from the Media Planning list view using the **Add Media Plan** button. A creation form slides in on the right side.

**Steps observed:**
1. Click the **Add Media Plan** button on the Media Planning page.
2. A panel/form opens on the right with the following fields:
   - **Media Plan Name** (text)
   - **Brand** (dropdown)
   - **Media AE** (dropdown)
   - **Market Type** (dropdown)
   - **Status** – default: *Working Internal*
   - **Bill Type** – default: *Contractual*
   - **Bill By** – default: *NBA*
   - **Sold By** (dropdown)
   - **Plan Start Date** – e.g., 10/01/2023
   - **Plan End Date** – e.g., 09/30/2024
   - **Mark as Primary** (checkbox)
3. Fill in required fields and click **Save** (implied).

---

## Scenario 6 – View Media Plan Versions

**Video Timestamp:** ~450 s  
**Module:** Media Planning / Plan Versions

**Description:**  
Within a media plan on the Media Planning list, multiple plan versions are visible. Each version has its own Plan ID, market type, deal linkage, date range, planned budget, and primary flag.

**Steps observed:**
1. Expand/open a media plan (e.g., "NBA 2K Media Plan 23/24").
2. The system displays a version table:

| Version | Plan ID | Market Type | Deal ID | Start Date | End Date | Planned Budget | Primary |
|---|---|---|---|---|---|---|---|
| 2 | 1151 | Domestic | 22838 | 10/01/2023 | 09/30/2024 | $568.00 | Yes |
| 3 | 1152 | Domestic | 22838 | 10/01/2023 | 11/29/2024 | $9,620.00 | – |
| 4 | 1188 | Domestic | 22838 | 10/01/2023 | 01/28/2025 | $4,500.00 | – |

---

## Scenario 7 – View Media Plan Line Items (Assets / Placements)

**Video Timestamp:** ~420 s  
**Module:** Media Planning / Plan Detail / Line Items

**Description:**  
Inside a media plan version, the user drills into line-level details showing individual media placements (assets) by country, media type, date range, brand, and planned dollar amount.

**Steps observed:**
1. Select a specific plan version (e.g., Version 2, Plan ID 1151).
2. The plan detail panel opens showing individual media line items:

| Country | Media | Start Date | End Date | Asset / Brand | Planned $ Amount |
|---|---|---|---|---|---|
| United States | Digital | 12/01/2023 | 12/31/2023 | NBA Media / 2K Sports | $2,000.00 |
| United States | TV-Game | 03/01/2024 | 03/31/2024 | G League Up Next Game / 2K Sports | $500.00 |

---

## Scenario 8 – Edit an Existing Media Plan

**Video Timestamp:** ~480 s  
**Module:** Media Planning / Edit Media Plan

**Description:**  
A user edits an existing media plan using the **Edit Media Plan** form. The form is pre-populated with current plan data.

**Steps observed:**
1. Click the edit icon/button next to a media plan.
2. The Edit Media Plan panel opens with pre-filled fields:
   - **Status**: Working Internal
   - **Bill Type**: Contractual
   - **Sold By**: (dropdown)
   - **Plan Start Date**: 10/01/2023
   - **Plan End Date**: 11/29/2024
3. A **Media Detail** sub-section shows the line items with columns: Media Type, Start Date, End Date, Mark, Confirm.
4. User modifies the desired fields and saves.

---

## Scenario 9 – DMS Integration Code Review (Backend)

**Video Timestamp:** 90 s – 180 s  
**Module:** Backend / DMSIntegrationService

**Description:**  
The demo shows Visual Studio Code with `DMSRepository.cs` open, part of the `MPATSDMSIntegration` project. The developer reviews Oracle SQL queries used to fetch deal data from the DMS (Deal Management System) into MPATS.

**Key details observed:**
- Project: `MPATSDMSIntegration > DMSIntegrationService > Repository > DMSRepository.cs`
- Branch: `Feature/MPATS-85`
- The SQL query fetches: `DEALNAME`, `AMOUNT` (Proposed_Pricing), `DEALSTATUS`, `CATEGORY`, `INVENTORY` (Geo), `DEALLEADER`, `SUBLICENSEE`, `LEAGUE`, `COUNTRY`, `DEALTYPE`, `CONTRACTTYPE`, anticipated fields, and others from Oracle views `vw_cp_deal_header` and `vw_cp_deal_lines`.
- Filters applied: `contentcount > 0`, `year > 2020`, `lostdeal = 0`, date range (fromDate / toDate in MM/DD/YYYY format).
- The query uses parameterized inputs with `OracleDbType.Text`.

---

## Scenario 10 – SQL Partner/Customer Sync Logic (Database)

**Video Timestamp:** ~150 s  
**Module:** Backend / SQL / DMS Advertiser Deal Job

**Description:**  
Microsoft SQL Server Management Studio is shown with a stored procedure / SQL script that handles upsert of partner (customer) records when DMS deals are synced.

**Key logic observed:**
1. If `@CurCustomerId` is not blank AND no matching `PartnerDetail` record exists (by `PSoftId` and `PartnerType=501`):
   - Check if a deal with a TBD PSoftId exists → if so, **update** the existing `PartnerDetail` record with the real customer ID.
   - Otherwise, **insert** a new `PartnerDetail` record.
2. Retrieve `@partnerId` from `PartnerDetail` for further processing.
3. Tables involved: `AdvertiserDeal`, `PartnerDetail`.

---

## Summary of Identified Scenarios

| # | Scenario | Module | Type |
|---|---|---|---|
| 1 | View Advertiser Deals List | Deals | UI / Functional |
| 2 | Search / Filter Deals | Deals | UI / Functional |
| 3 | Expand Deal Budget Summary | Deals | UI / Functional |
| 4 | Navigate to Media Planning | Media Planning | UI / Navigation |
| 5 | Create New Media Plan | Media Planning | UI / Functional |
| 6 | View Media Plan Versions | Media Planning | UI / Functional |
| 7 | View Media Plan Line Items | Media Planning | UI / Functional |
| 8 | Edit Existing Media Plan | Media Planning | UI / Functional |
| 9 | DMS Integration – Oracle Query | Backend | Code / Integration |
| 10 | SQL Partner Sync (Upsert) | Backend / DB | Code / Integration |
