"use client";

import { useState } from "react";
import { CosmicBackground } from "@/components/layout/cosmic-background";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { Hero } from "@/components/home/hero";
import { BirthForm } from "@/components/home/birth-form";
import { HowItWorks } from "@/components/home/how-it-works";
import { AboutSection } from "@/components/home/about";
import { FaqSection } from "@/components/home/faq";
import { ResultsSection } from "@/components/results/results-section";
import { AuthProvider, useAuth } from "@/components/auth/auth-provider";
import { AuthGate } from "@/components/auth/auth-gate";
import type { BirthFormValues, HumanDesignResult } from "@/types/hd";

function HomeContent() {
  const { status } = useAuth();
  const [result, setResult] = useState<HumanDesignResult | null>(null);
  const [form, setForm] = useState<BirthFormValues | null>(null);

  if (status === "loading") {
    return (
      <main className="relative flex min-h-screen items-center justify-center">
        <CosmicBackground />
        <p className="relative z-10 text-sm tracking-[0.2em] text-muted">載入中…</p>
      </main>
    );
  }

  if (status === "unauthenticated") {
    return <AuthGate />;
  }

  return (
    <main className="relative min-h-screen overflow-x-hidden">
      <CosmicBackground />
      <Navbar />
      <Hero />
      <HowItWorks />
      <BirthForm
        onResult={(data, values) => {
          setResult(data);
          setForm(values);
        }}
      />
      {result && <ResultsSection data={result} form={form} />}
      <AboutSection />
      <FaqSection />
      <Footer />
    </main>
  );
}

export default function HomePage() {
  return (
    <AuthProvider>
      <HomeContent />
    </AuthProvider>
  );
}
