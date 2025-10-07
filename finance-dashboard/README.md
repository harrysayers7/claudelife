# SAYERS Finance Dashboard

A Next.js 14+ finance dashboard with Supabase backend for managing multi-entity finances, visualizing data, and generating tax compliance documents.

## Features

- **Dashboard**: KPIs, charts, recent transactions, ML insights
- **Transactions**: AI-powered categorization review with confidence scores
- **Invoices**: Create, manage, track payments, generate PDFs
- **Reports & Tax**: BAS calculation, P&L statements, exports
- **Multi-Entity**: MOKAI PTY LTD, MOK HOUSE PTY LTD, Harrison Sayers
- **Settings**: Entity/contact/account management

## Tech Stack

- **Frontend**: Next.js 14+ (App Router), TypeScript, Tailwind CSS
- **Backend**: Supabase (PostgreSQL with RLS)
- **UI**: shadcn/ui components
- **Charts**: Recharts
- **Testing**: Vitest, Playwright
- **Deployment**: Vercel

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Supabase account with SAYERS DATA project

### Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env.local
```

Edit `.env.local` and add your Supabase credentials:
- Get `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` from Supabase dashboard
- Get `SUPABASE_SERVICE_ROLE_KEY` (keep this secret!)

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
finance-dashboard/
├── src/
│   ├── app/                  # Next.js app directory
│   │   ├── (auth)/          # Auth routes (login)
│   │   ├── (dashboard)/     # Protected dashboard routes
│   │   └── api/             # API routes
│   ├── components/          # React components
│   │   ├── ui/             # shadcn/ui components
│   │   ├── charts/         # Chart components
│   │   ├── forms/          # Form components
│   │   └── layout/         # Layout components
│   ├── lib/                # Utilities
│   │   ├── supabase/       # Supabase clients
│   │   ├── validations/    # Zod schemas
│   │   └── utils/          # Helper functions
│   ├── hooks/              # Custom React hooks
│   └── types/              # TypeScript types
├── public/                 # Static assets
├── docs/                   # Project documentation
└── tests/                  # Test files
```

## Documentation

- [Product Requirements Document](../docs/prd.md)
- [Architecture](../docs/architecture.md)
- [Frontend Specification](../docs/front-end-spec.md)
- [Test Strategy](../docs/qa/test-strategy.md)

## Development

### Running Tests

```bash
# Unit and integration tests
npm test

# E2E tests
npm run test:e2e

# Test coverage
npm run test:coverage
```

### Code Quality

```bash
# Linting
npm run lint

# Type checking
npm run type-check
```

## Deployment

Deploy to Vercel - environment variables are configured in Vercel dashboard.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | Yes |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anonymous key | Yes |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key (server-side only) | Yes |

## Security

- Row Level Security (RLS) enforced on all Supabase tables
- Multi-entity data isolation
- Authentication via Supabase Auth
- Input validation with Zod
- Audit logging for all data changes

## License

Private - All rights reserved
