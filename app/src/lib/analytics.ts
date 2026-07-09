"use client";

// PostHog-backed analytics wrapper implementing experiment_spec.md §4 exactly.
//
// - Event names and per-event property sets are frozen by the spec's funnel table and
//   property schema. The types below encode that contract so a call site cannot attach
//   a disallowed property or misspell an event name.
// - If NEXT_PUBLIC_POSTHOG_KEY is not set, PostHog is never loaded — the app still works
//   fully offline. Every event is additionally mirrored into localStorage (see storage.ts)
//   so the admin dashboard has real captured data to merge with the synthetic dataset,
//   regardless of whether a real PostHog project is configured. This dual-write is a
//   prototype convenience, not a spec requirement — flagged in prototype_readme.md.
// - Session replay and autocapture of network/console data are explicitly disabled.

import type {
  DecisionResult,
  ParticipantType,
  SponsorCategory,
  Variant,
} from "./types";
import { appendCapturedEvent } from "./storage";

export type EventName =
  | "concept_assigned"
  | "concept_viewed"
  | "learn_more_clicked"
  | "privacy_details_opened"
  | "continue_clicked"
  | "sponsor_opt_out_selected"
  | "survey_started"
  | "survey_submitted"
  | "booking_intent_selected"
  | "results_viewed"
  | "scenario_exported";

interface ConceptAssignedProps {
  variant: Variant;
  sponsor_category: SponsorCategory;
  participant_type: ParticipantType;
}
type ConceptViewedProps = ConceptAssignedProps;
type LearnMoreClickedProps = ConceptAssignedProps;
type PrivacyDetailsOpenedProps = ConceptAssignedProps;
interface ContinueClickedProps extends ConceptAssignedProps {
  decision_result: "continue";
}
interface SponsorOptOutSelectedProps extends ConceptAssignedProps {
  decision_result: Extract<DecisionResult, "opt_out" | "exit">;
  opt_out: true;
}
interface SurveyStartedProps {
  variant: Variant;
  participant_type: ParticipantType;
}
interface SurveySubmittedProps {
  variant: Variant;
  participant_type: ParticipantType;
  trust_score: number;
  independence_score: number;
  privacy_concern: number;
  continuation_intent: number;
  opt_out: boolean;
}
interface BookingIntentSelectedProps {
  variant: Variant;
  participant_type: ParticipantType;
  continuation_intent: number;
}
interface ResultsViewedProps {
  participant_type: "admin";
}
interface ScenarioExportedProps {
  participant_type: "admin";
  variant: Variant | "all";
}

export interface EventPropsMap {
  concept_assigned: ConceptAssignedProps;
  concept_viewed: ConceptViewedProps;
  learn_more_clicked: LearnMoreClickedProps;
  privacy_details_opened: PrivacyDetailsOpenedProps;
  continue_clicked: ContinueClickedProps;
  sponsor_opt_out_selected: SponsorOptOutSelectedProps;
  survey_started: SurveyStartedProps;
  survey_submitted: SurveySubmittedProps;
  booking_intent_selected: BookingIntentSelectedProps;
  results_viewed: ResultsViewedProps;
  scenario_exported: ScenarioExportedProps;
}

// Minimal shape of the posthog-js client we rely on, to avoid pulling in full types
// before the dependency is installed / when it's absent at runtime.
interface PostHogLike {
  init: (key: string, config: Record<string, unknown>) => void;
  capture: (event: string, properties?: Record<string, unknown>) => void;
  get_distinct_id?: () => string;
}

let posthogClient: PostHogLike | null = null;
let initAttempted = false;
let posthogModulePromise: Promise<unknown> | null = null;

const POSTHOG_KEY = process.env.NEXT_PUBLIC_POSTHOG_KEY;
const POSTHOG_HOST =
  process.env.NEXT_PUBLIC_POSTHOG_HOST || "https://us.i.posthog.com";

/**
 * Initializes PostHog if a key is configured. No-ops (and stays no-op) otherwise.
 * Safe to call multiple times; only initializes once.
 * Session replay, autocapture-of-network, and heatmaps are explicitly disabled
 * per experiment_spec.md §4/§8 ("session replay and network recording must be disabled").
 */
export function initAnalytics(): void {
  if (typeof window === "undefined") return;
  if (initAttempted) return;
  initAttempted = true;

  if (!POSTHOG_KEY) {
    // No key configured — fully offline mode. Nothing to initialize.
    return;
  }

  // Lazy-load posthog-js only when a key is present, so the dependency is optional
  // at runtime and the offline path never pays for it.
  posthogModulePromise = import("posthog-js")
    .then((mod) => {
      const ph = (mod.default ?? mod) as unknown as PostHogLike;
      ph.init(POSTHOG_KEY, {
        api_host: POSTHOG_HOST,
        disable_session_recording: true,
        capture_pageview: false,
        capture_pageleave: false,
        autocapture: false,
        persistence: "localStorage",
      });
      posthogClient = ph;
      return ph;
    })
    .catch(() => {
      // posthog-js not installed or failed to load — stay in offline mode silently.
      posthogClient = null;
      return null;
    });
}

export function getDistinctIdFromPostHog(): string | null {
  if (posthogClient?.get_distinct_id) {
    try {
      return posthogClient.get_distinct_id();
    } catch {
      return null;
    }
  }
  return null;
}

/**
 * Fires a single event from the frozen §4 contract. Properties are restricted at the
 * type level to exactly the allowed set for that event — no extras can be attached.
 * Always mirrors to local storage (offline-first dashboard); also forwards to PostHog
 * if a real client is configured and loaded.
 */
export function capture<E extends EventName>(
  event: E,
  properties: EventPropsMap[E],
  distinctId?: string
): void {
  if (typeof window === "undefined") return;

  const timestamp = new Date().toISOString();

  appendCapturedEvent({
    event,
    properties: properties as unknown as Record<string, unknown>,
    timestamp,
    distinctId,
  });

  if (posthogClient) {
    posthogClient.capture(event, { ...properties, distinct_id: distinctId });
  } else if (POSTHOG_KEY && posthogModulePromise) {
    // PostHog is still loading — queue by waiting on the init promise, best-effort.
    posthogModulePromise.then(() => {
      posthogClient?.capture(event, { ...properties, distinct_id: distinctId });
    });
  }
  // If no key at all, the localStorage mirror above is the only record — by design.
}
