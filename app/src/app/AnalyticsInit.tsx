"use client";

import { useEffect } from "react";
import { initAnalytics } from "@/lib/analytics";

/** Fires once on app mount to initialize PostHog if a key is configured (no-op otherwise). */
export default function AnalyticsInit() {
  useEffect(() => {
    initAnalytics();
  }, []);
  return null;
}
