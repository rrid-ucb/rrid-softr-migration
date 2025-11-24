# Baserow Migration Feasibility Report

## 1. Executive Summary
Moving from Airtable to Baserow (Open Source) is a **Highly Feasible** but **Medium Effort** migration. Baserow offers near-parity on core database features but requires significant work to replicate Airtable's "Interface" views and Automations.

**Recommendation**: Start with **Managed Baserow (SaaS)** to validate schema compatibility, then move to **Self-Hosted** if custom automation logic requires direct DB access or unlimited usage.

## 2. Schema Compatibility

### 2.1 Field Type Mapping
Most Airtable fields map 1:1 to Baserow.

| Airtable Type | Baserow Type | Notes |
| :--- | :--- | :--- |
| Single Line Text | Text | Direct map. |
| Long Text | Long Text | Direct map. |
| Single Select | Single Select | Options need to be migrated. Colors might not match 1:1. |
| Multiple Select | Multiple Select | Same as above. |
| Checkbox | Boolean | Direct map. |
| Link to Record | Link to Table | **Critical**: Baserow links are strictly 1:N or N:N. Airtable is looser. |
| Formula | Formula | Baserow uses a different syntax (Python-like vs Excel-like). **High Effort** to rewrite. |
| Rollup | Lookup/Formula | Baserow handles lookups well; complex rollups might need formula combinations. |
| Created/Last Modified | Created/Last Modified | Direct map. |

### 2.2 Missing Features / Workarounds
- **Interfaces**: Baserow has an "Application Builder" (beta) but it is less mature than Airtable Interfaces. We are building a custom Next.js frontend, so **this is not a blocker**.
- **Scripting Block**: Baserow does not have a client-side JS scripting block. Logic must move to the Backend (Next.js API) or n8n.

## 3. Automation Strategy

Airtable Automations (e.g., "When record matches condition -> Send Email") must be replaced.

### Option A: n8n / Make (No-Code)
- Baserow has native webhooks.
- **Trigger**: Row Updated/Created in Baserow.
- **Action**: n8n workflow receives payload -> executes logic -> updates Baserow.
- **Pros**: Visual, easy to debug.
- **Cons**: External dependency, potential cost.

### Option B: Custom Backend (Code)
- Since we are building a Next.js app, we can move business logic into **Server Actions**.
- **Trigger**: User submits form in Next.js.
- **Action**: Next.js writes to Baserow -> calculates derived fields -> sends emails.
- **Pros**: Full control, no extra SaaS cost, version controlled.
- **Cons**: More code to write/maintain.

## 4. Hosting Options

### 4.1 Managed Baserow (baserow.io)
- **Pros**: No maintenance, instant setup.
- **Cons**: Rate limits (though generous), data residency (EU servers by default).
- **Cost**: ~$5/user/month.

### 4.2 Self-Hosted (Docker/Kubernetes)
- **Pros**: Full database access (PostgreSQL), no record limits, API speed (local network).
- **Cons**: DevOps overhead (backups, updates, scaling).
- **Cost**: Infrastructure only ($10-20/mo on DigitalOcean/Hetzner).

## 5. Migration Steps

1.  **Export Data**: Use Airtable API or CSV export (CSV loses linking structure, API script preferred).
2.  **Schema Reconstruction**:
    - Create Workspace/Database in Baserow.
    - Create Tables (`Preprints`, `Reviewers`, `Users`).
    - Create Fields (Text, Numbers, Selects).
3.  **Linkage Restoration**:
    - Import data with temporary "Legacy ID" fields.
    - Run a script to re-establish links based on Legacy IDs.
4.  **Formula Rewrite**: Manually rewrite critical formulas (e.g., `More Invites Needed?`) in Baserow syntax.
5.  **Frontend Switch**: Update Next.js `lib/db/client.ts` to point to Baserow API instead of Airtable API.

## 6. Risk Assessment

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **Formula Complexity** | High | Audit all formulas in `SCHEMA.md`. Simplify logic or move to backend code. |
| **API Rate Limits** | Medium | Self-host Baserow or implement caching (Redis) in Next.js. |
| **Data Integrity** | High | rigorous testing of Link fields during migration. |

## 7. Conclusion
Migrating to Baserow is a viable long-term strategy to reduce costs and avoid vendor lock-in. Since we are already building a custom frontend, the lack of Baserow's native "Interface" features is irrelevant. The main effort will be in **rewriting formulas** and **data migration scripts**.

