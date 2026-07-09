// Content and metadata for the four concept-test arms, per experiment_spec.md §2.
// Sponsor names are entirely fictitious (synthetic), per §8 "Synthetic sponsors only."

import type { SponsorCategory, Variant } from "./types";

export interface VariantConfig {
  variant: Variant;
  sponsorCategory: SponsorCategory;
  label: string;
  headline: string;
  body: string[];
  sponsorBlurb?: string;
  sponsoredEducation?: {
    heading: string;
    body: string;
  };
  disclosureLine: string;
}

export const VARIANT_ORDER: Variant[] = [
  "control",
  "variant_a",
  "variant_b",
  "variant_c",
];

export const VARIANT_CONFIG: Record<Variant, VariantConfig> = {
  control: {
    variant: "control",
    sponsorCategory: "none",
    label: "Control — Affordable Care, No Sponsorship",
    headline: "Affordable virtual mental health care",
    body: [
      "This concept offers low-cost virtual mental health care, funded entirely through standard patient fees and insurance — no outside sponsor is involved.",
      "There is no advertising, no sponsored content, and no sharing of your information with any third party for marketing or sponsorship purposes.",
    ],
    disclosureLine:
      "No sponsor is involved in this concept. Your information is not shared for sponsorship or advertising purposes.",
  },
  variant_a: {
    variant: "variant_a",
    sponsorCategory: "consumer_health",
    label: "Variant A — Free Care, Supported by Sponsor X",
    headline: "Free virtual mental health care — supported by Acme Wellness Co.",
    body: [
      "This concept offers free virtual mental health care. Care is supported by Acme Wellness Co. (a fictitious consumer wellness brand, used for testing only), which helps cover the cost of your visits.",
      "Acme Wellness Co. does not see your personal health information and does not influence your treatment or clinician decisions.",
    ],
    sponsorBlurb:
      "Acme Wellness Co. is a synthetic sponsor created for this research prototype and does not represent a real company.",
    disclosureLine:
      "Acme Wellness Co. pays to support access to this care. They do not see your personal health information and do not influence your treatment.",
  },
  variant_b: {
    variant: "variant_b",
    sponsorCategory: "consumer_health",
    label: "Variant B — Free Care + Separated Sponsored Education",
    headline: "Free virtual mental health care — supported by Acme Wellness Co.",
    body: [
      "This concept offers free virtual mental health care, supported by Acme Wellness Co. (a fictitious consumer wellness brand, used for testing only).",
      "Acme Wellness Co. does not see your personal health information and does not influence your treatment or clinician decisions.",
    ],
    sponsorBlurb:
      "Acme Wellness Co. is a synthetic sponsor created for this research prototype and does not represent a real company.",
    sponsoredEducation: {
      heading: "Sponsored Educational Content (clearly separated from your care)",
      body: "“Managing Everyday Stress” — a general wellness article provided by Acme Wellness Co. This content is educational only, is clearly labeled as sponsored, and is never used by your clinician to make treatment decisions.",
    },
    disclosureLine:
      "Acme Wellness Co. pays to support access to this care and provides separately-labeled educational content. They do not see your personal health information and do not influence your treatment.",
  },
  variant_c: {
    variant: "variant_c",
    sponsorCategory: "pharma",
    label: "Variant C — Visible Pharma-Style Sponsor (concept-test only)",
    headline: "Free virtual mental health care — supported by Solara Pharma Labs",
    body: [
      "This concept offers free virtual mental health care, made possible through support from Solara Pharma Labs (a fictitious pharmaceutical company, used for testing only).",
      "Solara Pharma Labs' branding appears throughout your visit. Solara Pharma Labs does not see your personal health information and does not influence your treatment or clinician decisions.",
    ],
    sponsorBlurb:
      "Solara Pharma Labs is a synthetic sponsor created for this research prototype and does not represent a real company. This concept is for research purposes only and is not a candidate for the first live pilot.",
    disclosureLine:
      "Solara Pharma Labs pays to support access to this care and their branding appears in this experience. They do not see your personal health information and do not influence your treatment.",
  },
};

export function getVariantConfig(variant: Variant): VariantConfig {
  return VARIANT_CONFIG[variant];
}
