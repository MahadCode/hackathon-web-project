"use client";

import { motion } from "framer-motion";
import { Telescope, ShieldCheck, Sparkles, TrendingUp } from "lucide-react";

const HIGHLIGHTS = [
  { icon: Sparkles, text: "AI agents parse, match, and score every candidate in seconds." },
  { icon: TrendingUp, text: "See hiring funnels and AI accuracy trends in real time." },
  { icon: ShieldCheck, text: "Enterprise-grade security with role-based access control." },
];

export default function AuthGroupLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      <div className="relative hidden overflow-hidden bg-gradient-brand lg:flex lg:flex-col lg:justify-between lg:p-12">
        <div className="absolute inset-0 bg-gradient-mesh opacity-40" />
        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
          className="relative z-10 flex items-center gap-2 text-white"
        >
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/15">
            <Telescope className="h-5 w-5" />
          </div>
          <span className="text-lg font-semibold tracking-tight">Talent Lens</span>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.15 }}
          className="relative z-10 max-w-md space-y-6 text-white"
        >
          <h1 className="text-4xl font-semibold leading-tight tracking-tight">See Beyond the Resume.</h1>
          <p className="text-white/80">AI-Powered Hiring Intelligence for Modern Teams.</p>
          <div className="space-y-4 pt-4">
            {HIGHLIGHTS.map(({ icon: Icon, text }, i) => (
              <motion.div
                key={text}
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.3 + i * 0.1 }}
                className="flex items-start gap-3 rounded-2xl bg-white/10 p-4 backdrop-blur-sm"
              >
                <Icon className="mt-0.5 h-4 w-4 shrink-0" />
                <p className="text-sm text-white/90">{text}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        <p className="relative z-10 text-xs text-white/60">
          Trusted by hiring teams building the next generation of technical organizations.
        </p>
      </div>

      <div className="flex items-center justify-center bg-background px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="glass-panel w-full max-w-md rounded-2xl p-8 shadow-soft"
        >
          {children}
        </motion.div>
      </div>
    </div>
  );
}
