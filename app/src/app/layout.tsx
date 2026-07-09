import type { Metadata } from "next";
import "./globals.css";
import AnalyticsInit from "./AnalyticsInit";

export const metadata: Metadata = {
  title: "Legion Sponsorship Concept Test (Research Prototype)",
  description:
    "Research concept test prototype — not a clinical service. No real patient data is collected.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <AnalyticsInit />
        {children}
      </body>
    </html>
  );
}
