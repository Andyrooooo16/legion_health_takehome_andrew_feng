# Legion Sponsorship Concept Test, Prototype

This is a Next.js (App Router) + TypeScript prototype implementing the patient side
sponsorship concept test described in `../deliverables/experiment_spec.md`.

See **[`prototype_readme.md`](./prototype_readme.md)** for how to run it locally, plug
in a real PostHog key, deploy to Vercel, what is synthetic vs. real, and known
limitations. See **[`analytics/event_schema.md`](./analytics/event_schema.md)** for the
PostHog event contract implemented here.

Quick start:

```bash
npm install
npm run dev
```

Then open `http://localhost:3000`.
