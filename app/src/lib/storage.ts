"use client";

// Thin localStorage persistence layer. Plays two roles:
//  1. "Sticky" participant/assignment state so the multi-page flow survives navigation
//     and reloads within the same browser (experiment_spec.md §2 randomization mechanism).
//  2. The prototype's own lightweight "database" for fields that must NOT be sent to
//     PostHog (free text, Q2/Q6, comprehension check — see types.ts) and for a local
//     mirror of every fired analytics event, so the admin dashboard can show real
//     captured data even with no PostHog project configured.
//
// This is a prototype convenience, not a production data store. Nothing here is PHI.

import type { ParticipantRecord } from "./types";

const KEYS = {
  distinctId: "lsp_distinct_id",
  variant: "lsp_variant",
  sponsorCategory: "lsp_sponsor_category",
  participantType: "lsp_participant_type",
  assignedFired: "lsp_assigned_fired",
  currentRecord: "lsp_current_record",
  capturedRecords: "lsp_captured_records", // array of ParticipantRecord (real, non-synthetic)
  capturedEvents: "lsp_captured_events", // array of raw fired events (for debugging / audit)
} as const;

function safeGet(key: string): string | null {
  if (typeof window === "undefined") return null;
  try {
    return window.localStorage.getItem(key);
  } catch {
    return null;
  }
}

function safeSet(key: string, value: string): void {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(key, value);
  } catch {
    // localStorage unavailable (e.g., private browsing quota) — degrade silently.
  }
}

export function getRaw(key: keyof typeof KEYS): string | null {
  return safeGet(KEYS[key]);
}

export function setRaw(key: keyof typeof KEYS, value: string): void {
  safeSet(KEYS[key], value);
}

// ---- Captured events (raw analytics mirror) ----

export interface CapturedEvent {
  event: string;
  properties: Record<string, unknown>;
  timestamp: string;
  distinctId?: string;
}

export function appendCapturedEvent(evt: CapturedEvent): void {
  if (typeof window === "undefined") return;
  try {
    const existingRaw = window.localStorage.getItem(KEYS.capturedEvents);
    const existing: CapturedEvent[] = existingRaw ? JSON.parse(existingRaw) : [];
    existing.push(evt);
    // Cap history to avoid unbounded growth in a long-lived demo browser.
    const trimmed = existing.slice(-2000);
    window.localStorage.setItem(KEYS.capturedEvents, JSON.stringify(trimmed));
  } catch {
    // ignore
  }
}

export function getCapturedEvents(): CapturedEvent[] {
  const raw = safeGet(KEYS.capturedEvents);
  if (!raw) return [];
  try {
    return JSON.parse(raw) as CapturedEvent[];
  } catch {
    return [];
  }
}

// ---- Participant record (per-browser "current" record + append-only captured list) ----

export function getCurrentRecord(): ParticipantRecord | null {
  const raw = safeGet(KEYS.currentRecord);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as ParticipantRecord;
  } catch {
    return null;
  }
}

export function saveCurrentRecord(record: ParticipantRecord): void {
  record.updatedAt = new Date().toISOString();
  safeSet(KEYS.currentRecord, JSON.stringify(record));
  upsertCapturedRecord(record);
}

function upsertCapturedRecord(record: ParticipantRecord): void {
  if (typeof window === "undefined") return;
  try {
    const raw = window.localStorage.getItem(KEYS.capturedRecords);
    const list: ParticipantRecord[] = raw ? JSON.parse(raw) : [];
    const idx = list.findIndex((r) => r.distinctId === record.distinctId);
    if (idx >= 0) {
      list[idx] = record;
    } else {
      list.push(record);
    }
    window.localStorage.setItem(KEYS.capturedRecords, JSON.stringify(list));
  } catch {
    // ignore
  }
}

export function getCapturedRecords(): ParticipantRecord[] {
  const raw = safeGet(KEYS.capturedRecords);
  if (!raw) return [];
  try {
    return JSON.parse(raw) as ParticipantRecord[];
  } catch {
    return [];
  }
}

export function clearAllLocalData(): void {
  if (typeof window === "undefined") return;
  Object.values(KEYS).forEach((k) => window.localStorage.removeItem(k));
}
