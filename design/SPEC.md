# Technical Specification

## 1. Technology Stack Reference

Based on `rrid-app-frontend/design/TECHSTACK.md`:
- **Core**: Next.js 16 (App Router), TypeScript, React 19.
- **Styling**: Tailwind CSS 4, Shadcn/UI.
- **Backend**: Firebase (Auth, Firestore, Hosting), Airtable (Main DB).
- **AI**: Vercel AI SDK, Gemini Pro.

## 2. Application Structure

```
src/
├── app/                    # Next.js App Router
│   ├── (auth)/             # Authentication Routes
│   │   ├── login/
│   │   └── register/
│   ├── (dashboard)/        # Protected Routes
│   │   ├── layout.tsx      # Main Dashboard Layout (Sidebar/Header)
│   │   ├── page.tsx        # Dashboard Home (Grid View)
│   │   ├── preprints/
│   │   │   ├── page.tsx    # List View
│   │   │   └── [id]/       # Detail View
│   │   ├── reviewers/
│   │   │   ├── new/        # Propose Reviewer Form
│   │   │   └── [id]/       # Reviewer Details
│   │   └── quality/        # QC Portal
│   ├── api/                # Internal API Routes (if needed)
│   └── global.css          # Tailwind 4 Imports
├── components/
│   ├── ui/                 # Shadcn Primitives (Button, Card, etc.)
│   ├── domain/             # Business Components (PreprintCard, ReviewerForm)
│   └── layout/             # Shell, Sidebar, Nav
├── lib/
│   ├── airtable/           # Typed Airtable Client
│   ├── firebase/           # Firebase Config & Admin
│   ├── hooks/              # Custom React Hooks
│   └── utils.ts            # Helpers
└── types/                  # TypeScript Interfaces
```

## 3. Data Access Layer

### 3.1 Airtable Client
We will use a singleton pattern for the Airtable client to manage rate limits.

```typescript
// lib/airtable/client.ts
import Airtable from 'airtable';

const base = new Airtable({ apiKey: process.env.AIRTABLE_API_KEY }).base(process.env.AIRTABLE_BASE_ID);

export const tables = {
  preprints: base('Preprint Info ONLY'),
  reviewers: base('Student Reviewer Inputs'),
  users: base('All Users'),
};
```

### 3.2 Type Definitions
Zod schemas will be generated from the `airtable_complete_schema.json` to ensure runtime validation.

```typescript
// types/schema.ts
import { z } from 'zod';

export const PreprintSchema = z.object({
  id: z.string(),
  fields: z.object({
    Title: z.string(),
    "Corresponding Author": z.string().optional(),
    Domain: z.enum(['BCS', 'MedSci', 'PSE', 'SSH']),
    // ... mapped from schema report
  })
});
```

## 4. Key Feature Implementation

### 4.1 Authentication Flow
1.  Client: `firebase.auth().signInWithEmailAndPassword()`
2.  Firebase returns ID Token.
3.  Client sends ID Token to Next.js Server Action `createSession`.
4.  Server verifies token, fetches user role from Airtable `Users` table using the email.
5.  Server sets HTTP-only Session Cookie with encrypted user claims (Role, AirtableRecordID).

### 4.2 Preprints List with Filters
- **Component**: `PreprintList` (Server Component) -> fetches initial data.
- **State**: `useQuery` (TanStack Query) for client-side filtering and sorting without full page reloads.
- **Filter Logic**:
    ```typescript
    // Airtable Formula Generation
    const filterFormula = `AND(
      SEARCH("${searchTerm}", {Title}),
      {Domain} = "${selectedDomain}"
    )`;
    ```

### 4.3 Propose Reviewer Form
- **Library**: `react-hook-form` + `zod` resolver.
- **Validation**:
    - **Institutional Email**: Regex check. If fails, show "Justification" field.
    - **Backup Reviewer**: If "Yes" selected, "Backup Name" field becomes required.
- **Submission**:
    - Server Action: `submitReviewer(formData)`
    - Validates payload.
    - Calls `tables.reviewers.create()`.
    - Revalidates cache path `/preprints/[id]`.

## 5. Environment Variables

```env
NEXT_PUBLIC_FIREBASE_API_KEY=...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=...
FIREBASE_PROJECT_ID=...
FIREBASE_CLIENT_EMAIL=...
FIREBASE_PRIVATE_KEY=...
AIRTABLE_API_KEY=...
AIRTABLE_BASE_ID=...
```

## 6. Deployment
- **Build Command**: `next build`
- **Output**: Standalone
- **Hosting**: Vercel (recommended for Next.js optimization) or Firebase App Hosting.

