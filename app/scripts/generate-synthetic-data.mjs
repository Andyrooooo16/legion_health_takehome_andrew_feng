#!/usr/bin/env node
// Generates a deterministic synthetic dataset for the admin dashboard demo, per
// experiment_spec.md §7 (discovery-scale, ~87-90/arm) and §8 ("Use synthetic data in
// the public prototype"). This is fabricated data for demo purposes only — it does
// NOT represent any real Legion, patient, or panel data. Output: ../src/data/synthetic-participants.json
//
// Reproducible via a seeded PRNG (mulberry32) so the committed JSON is stable across runs.

import { writeFileSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.join(__dirname, "..", "src", "data");
const OUT_FILE = path.join(OUT_DIR, "synthetic-participants.json");

const N_PER_ARM = 90;
const SEED = 20260707; // today's date at authoring time, for a stable, memorable seed

function mulberry32(seed) {
  let a = seed;
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const rand = mulberry32(SEED);

function randNormal(mean, sd) {
  // Box-Muller transform
  const u1 = Math.max(rand(), 1e-9);
  const u2 = rand();
  const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
  return mean + z * sd;
}

function clampLikert(x) {
  return Math.min(5, Math.max(1, Math.round(x)));
}

function bernoulli(p) {
  return rand() < p;
}

function choice(arr, weights) {
  const total = weights.reduce((a, b) => a + b, 0);
  let r = rand() * total;
  for (let i = 0; i < arr.length; i++) {
    r -= weights[i];
    if (r <= 0) return arr[i];
  }
  return arr[arr.length - 1];
}

// "True" underlying parameters per arm — chosen to produce a plausible, illustrative
// pattern (Control best, Variant C most concerning) consistent with the qualitative
// expectations in experiment_spec.md §1/§9, NOT derived from any real study.
const ARM_PARAMS = {
  control: {
    sponsorCategory: "none",
    continuationRate: 0.62,
    trustMean: 4.2,
    trustSd: 0.8,
    independenceMean: 4.3,
    independenceSd: 0.7,
    privacyConcernMean: 2.0,
    privacyConcernSd: 0.9,
    optOutRate: 0.05,
    comprehensionRate: 0.9,
    paidPrefMean: 2.0,
    paidPrefSd: 0.9,
    coreBookRecommendMean: 4.1,
    coreBookInsuredMean: 4.0,
    selfReportComprehensionMean: 4.1,
    learnMoreRate: 0.3,
    privacyDetailsRate: 0.22,
  },
  variant_a: {
    sponsorCategory: "consumer_health",
    continuationRate: 0.58,
    trustMean: 3.9,
    trustSd: 0.85,
    independenceMean: 3.9,
    independenceSd: 0.8,
    privacyConcernMean: 2.6,
    privacyConcernSd: 1.0,
    optOutRate: 0.1,
    comprehensionRate: 0.82,
    paidPrefMean: 2.6,
    paidPrefSd: 1.0,
    coreBookRecommendMean: 3.7,
    coreBookInsuredMean: 3.6,
    selfReportComprehensionMean: 3.7,
    learnMoreRate: 0.38,
    privacyDetailsRate: 0.3,
  },
  variant_b: {
    sponsorCategory: "consumer_health",
    continuationRate: 0.6,
    trustMean: 4.0,
    trustSd: 0.8,
    independenceMean: 4.0,
    independenceSd: 0.75,
    privacyConcernMean: 2.5,
    privacyConcernSd: 1.0,
    optOutRate: 0.09,
    comprehensionRate: 0.85,
    paidPrefMean: 2.5,
    paidPrefSd: 1.0,
    coreBookRecommendMean: 3.8,
    coreBookInsuredMean: 3.7,
    selfReportComprehensionMean: 3.9,
    learnMoreRate: 0.42,
    privacyDetailsRate: 0.33,
  },
  variant_c: {
    sponsorCategory: "pharma",
    continuationRate: 0.47,
    trustMean: 3.3,
    trustSd: 1.0,
    independenceMean: 3.2,
    independenceSd: 1.0,
    privacyConcernMean: 3.4,
    privacyConcernSd: 1.0,
    optOutRate: 0.22,
    comprehensionRate: 0.74,
    paidPrefMean: 3.4,
    paidPrefSd: 1.0,
    coreBookRecommendMean: 3.0,
    coreBookInsuredMean: 2.9,
    selfReportComprehensionMean: 3.2,
    learnMoreRate: 0.4,
    privacyDetailsRate: 0.45,
  },
};

const FREE_TEXT_BANK = {
  none: [
    "",
    "",
    "Seems fine, straightforward.",
    "Wish it were even cheaper.",
  ],
  mild: [
    "A little unsure how the sponsor fits in, but seems okay.",
    "Not a big deal, just curious about the branding.",
  ],
  moderate: [
    "I'm somewhat concerned about why a company would pay for this.",
    "Feels a bit like an ad in a health app, not thrilled about it.",
  ],
  severe: [
    "I would not trust a service that lets a company sponsor my mental health care.",
    "This feels like my care decisions could be influenced by advertisers, I would not use this.",
    "Very uncomfortable with a pharma company being visibly attached to my care.",
  ],
};

function sampleFreeText(variant) {
  // Roughly 35% of participants leave free text; severity skews worse for variant_c.
  if (!bernoulli(0.35)) return "";
  const severityWeights =
    variant === "variant_c"
      ? { none: 0.25, mild: 0.25, moderate: 0.25, severe: 0.25 }
      : variant === "variant_a" || variant === "variant_b"
      ? { none: 0.45, mild: 0.3, moderate: 0.2, severe: 0.05 }
      : { none: 0.7, mild: 0.2, moderate: 0.08, severe: 0.02 };
  const tiers = Object.keys(severityWeights);
  const tier = choice(tiers, tiers.map((t) => severityWeights[t]));
  const bank = FREE_TEXT_BANK[tier];
  return bank[Math.floor(rand() * bank.length)];
}

function generateParticipant(variant, idx) {
  const p = ARM_PARAMS[variant];
  const exposed = true; // synthetic dataset represents completed exposures
  const continued = bernoulli(p.continuationRate);
  const optOutChosen = !continued && bernoulli(0.7); // most non-continuers actively opt out rather than exit
  const exited = !continued && !optOutChosen;

  const decisionResult = continued ? "continue" : exited ? "exit" : "opt_out";
  const optOut = decisionResult !== "continue";

  const trustScore = clampLikert(randNormal(p.trustMean, p.trustSd));
  const independenceScore = clampLikert(randNormal(p.independenceMean, p.independenceSd));
  const privacyConcern = clampLikert(randNormal(p.privacyConcernMean, p.privacyConcernSd));
  // continuation_intent correlates with actual continuation but is a distinct stated-intent item
  const intentBase = continued ? p.trustMean + 0.3 : p.trustMean - 0.6;
  const continuationIntent = clampLikert(randNormal(intentBase, 0.9));
  const paidOptionPreference = clampLikert(randNormal(p.paidPrefMean, p.paidPrefSd));
  const coreBookRecommendScore = clampLikert(
    randNormal(p.coreBookRecommendMean, p.trustSd)
  );
  const coreBookInsuredChoiceScore = clampLikert(
    randNormal(p.coreBookInsuredMean, p.trustSd)
  );
  const selfReportedComprehension = clampLikert(
    randNormal(p.selfReportComprehensionMean, 0.9)
  );
  const comprehensionCorrect = bernoulli(p.comprehensionRate);

  const surveyCompleted = !exited; // exit at Page 3 skips the survey entirely, per §4 funnel table

  const participantType = bernoulli(0.5) ? "panel" : "landing_page";

  const now = new Date(Date.UTC(2026, 5, 15 + (idx % 10))).toISOString();

  return {
    distinctId: `synthetic_${variant}_${idx}`,
    variant,
    sponsorCategory: p.sponsorCategory,
    participantType,
    createdAt: now,
    updatedAt: now,
    exposed,
    learnMoreClicked: bernoulli(p.learnMoreRate),
    privacyDetailsOpened: bernoulli(p.privacyDetailsRate),
    decisionResult,
    optOut,
    exitedAtAction: exited,
    surveyStarted: surveyCompleted,
    surveySubmitted: surveyCompleted,
    trustScore: surveyCompleted ? trustScore : undefined,
    independenceScore: surveyCompleted ? independenceScore : undefined,
    privacyConcern: surveyCompleted ? privacyConcern : undefined,
    continuationIntent: surveyCompleted ? continuationIntent : undefined,
    selfReportedComprehension: surveyCompleted ? selfReportedComprehension : undefined,
    paidOptionPreference: surveyCompleted ? paidOptionPreference : undefined,
    coreBookRecommendScore: surveyCompleted ? coreBookRecommendScore : undefined,
    coreBookInsuredChoiceScore: surveyCompleted ? coreBookInsuredChoiceScore : undefined,
    comprehensionCorrect: surveyCompleted ? comprehensionCorrect : undefined,
    freeText: surveyCompleted ? sampleFreeText(variant) : "",
    isSynthetic: true,
  };
}

function main() {
  const variants = ["control", "variant_a", "variant_b", "variant_c"];
  const participants = [];
  for (const variant of variants) {
    for (let i = 0; i < N_PER_ARM; i++) {
      participants.push(generateParticipant(variant, i));
    }
  }
  mkdirSync(OUT_DIR, { recursive: true });
  writeFileSync(OUT_FILE, JSON.stringify(participants, null, 2));
  console.log(`Wrote ${participants.length} synthetic participant records to ${OUT_FILE}`);
}

main();
