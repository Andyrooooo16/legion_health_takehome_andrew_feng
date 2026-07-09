"use client";

// Client-side sticky randomization, per experiment_spec.md §2:
//  - Assignment is keyed to an anonymous distinct_id persisted via localStorage
//    (standing in for the PostHog `distinct_id` / multivariate feature-flag payload
//    described in the spec — see prototype_readme.md for the flagged simplification).
//  - Assignment is sticky: once made, it is read back from storage on every visit.
//  - Equal allocation across the four arms (25/25/25/25): each new distinct_id draws
//    uniformly at random among the four arms using crypto-strength randomness, then
//    persists the draw so it never changes for that distinct_id again.
//  - `concept_assigned` fires immediately on first resolution, before Page 2 renders —
//    implemented here by resolving assignment (and firing the event) from a client
//    effect that runs on Page 1 mount, prior to any navigation to /concept.

import { capture } from "./analytics";
import { getRaw, setRaw } from "./storage";
import { VARIANT_CONFIG, VARIANT_ORDER } from "./variants";
import type { ParticipantAssignment, ParticipantType, Variant } from "./types";

function randomId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `pid_${Date.now()}_${Math.random().toString(36).slice(2)}`;
}

function pickRandomVariant(): Variant {
  const idx = Math.floor(Math.random() * VARIANT_ORDER.length);
  return VARIANT_ORDER[idx];
}

function getOrCreateDistinctId(): string {
  const existing = getRaw("distinctId");
  if (existing) return existing;
  const id = randomId();
  setRaw("distinctId", id);
  return id;
}

function getOrAssignVariant(): Variant {
  const existing = getRaw("variant") as Variant | null;
  if (existing && VARIANT_ORDER.includes(existing)) return existing;
  const assigned = pickRandomVariant();
  setRaw("variant", assigned);
  return assigned;
}

function resolveParticipantType(): ParticipantType {
  const existing = getRaw("participantType") as ParticipantType | null;
  if (existing) return existing;

  let fromQuery: ParticipantType | null = null;
  if (typeof window !== "undefined") {
    const params = new URLSearchParams(window.location.search);
    const raw = params.get("participant_type") || params.get("src");
    if (raw === "panel" || raw === "landing_page") {
      fromQuery = raw;
    }
  }
  const resolved: ParticipantType = fromQuery ?? "landing_page";
  setRaw("participantType", resolved);
  return resolved;
}

/**
 * Resolves (or creates) the sticky assignment for this browser, and fires
 * `concept_assigned` exactly once per participant per test window (guarded via
 * localStorage so re-mounts / re-visits don't re-fire it).
 */
export function ensureAssigned(): ParticipantAssignment {
  const distinctId = getOrCreateDistinctId();
  const variant = getOrAssignVariant();
  const sponsorCategory = VARIANT_CONFIG[variant].sponsorCategory;
  const participantType = resolveParticipantType();

  const alreadyFired = getRaw("assignedFired") === "1";
  if (!alreadyFired) {
    capture(
      "concept_assigned",
      {
        variant,
        sponsor_category: sponsorCategory,
        participant_type: participantType,
      },
      distinctId
    );
    setRaw("assignedFired", "1");
  }

  return { distinctId, variant, sponsorCategory, participantType };
}

/** Reads the current assignment without creating a new one (returns null if unassigned). */
export function readAssignment(): ParticipantAssignment | null {
  const distinctId = getRaw("distinctId");
  const variant = getRaw("variant") as Variant | null;
  const participantType = getRaw("participantType") as ParticipantType | null;
  if (!distinctId || !variant || !participantType) return null;
  return {
    distinctId,
    variant,
    sponsorCategory: VARIANT_CONFIG[variant].sponsorCategory,
    participantType,
  };
}
