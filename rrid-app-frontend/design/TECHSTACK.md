# Technology Stack

## Core Framework
*   **Frontend/Fullstack**: Next.js 16 (App Router)
*   **Language**: TypeScript
*   **Styling**: Tailwind CSS, Shadcn/UI, Vanilla CSS for custom animations
*   **Icons**: Lucide React

## Backend & Infrastructure
*   **Platform**: Firebase (via Firebase Studio / Google Cloud)
*   **Database**: Firestore (NoSQL) for flexible schema (Projects, RFPs, Users)
*   **Auth**: Firebase Authentication
*   **Storage**: Firebase Storage (for PDFs, Images)
*   **Hosting**: Firebase Hosting / Vercel (TBD, likely Firebase given the prompt)

## AI & Data
*   **LLM Interface**: Vercel AI SDK or direct API calls (Gemini/OpenAI)
*   **Vector Database** (Optional for MVP, but likely needed for "Deep Research"): Firestore Vector Search or Pinecone.
*   **Agent Framework**: LangChain or custom agent loops using Vercel AI SDK.

## Dev Tools
*   **IDE**: Google Antigravity (AI-first Editor)
*   **Package Manager**: npm / pnpm
*   **Linting**: ESLint, Prettier
*   **Version Control**: Git

## Key Libraries
*   **UI Components**: Shadcn/UI (Radix Primitives)
*   **Animation**: Framer Motion (for "wow" factor)
*   **Forms**: React Hook Form + Zod
*   **Data Fetching**: SWR or React Query (or Server Actions)

## Detailed Versions (as of Nov 23, 2025)

| Package | Version | Purpose |
| :--- | :--- | :--- |
| **Next.js** | `16.0.3` | Core Framework (App Router) |
| **React** | `19.2.0` | UI Library |
| **Tailwind CSS** | `4.0.0` (alpha/beta) | Styling Engine |
| **Firebase** | `^12.6.0` | Backend-as-a-Service |
| **Framer Motion** | `^12.23.24` | Animation Library |
| **Lucide React** | `^0.554.0` | Icons |
| **React Hook Form** | `^7.66.1` | Form Management |
| **Zod** | `^4.1.12` | Schema Validation |
| **Shadcn UI** | Latest | Component Library (Radix Primitives) |
| **Firebase Genkit** | `^1.24.0` | AI Agent Framework (Node.js) |
| **Gemini Model** | `gemini-3-pro-preview` | LLM (via Vertex AI / AI Studio) |
| **Gemini Image** | `gemini-3-pro-image-preview` | Image Generation Model |
