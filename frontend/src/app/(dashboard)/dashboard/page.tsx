"use client";

import { motion } from "framer-motion";
import { Briefcase, Users, MessagesSquare, Sparkles } from "lucide-react";

import { StatCard } from "@/components/dashboard/stat-card";
import { HiringFunnelChart } from "@/components/dashboard/hiring-funnel-chart";
import { WeeklyAnalyticsChart } from "@/components/dashboard/weekly-analytics-chart";
import { RecentActivity } from "@/components/dashboard/recent-activity";
import { AIRecommendations } from "@/components/dashboard/ai-recommendations";
import { QuickActions } from "@/components/dashboard/quick-actions";
import { LatestCandidates } from "@/components/dashboard/latest-candidates";
import { Skeleton } from "@/components/ui/skeleton";
import { ScoreRing } from "@/components/shared/score-ring";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useAuth } from "@/lib/hooks/use-auth";
import { useJobs } from "@/lib/hooks/use-jobs";

/**
 * NOTE ON SAMPLE DATA: the funnel stages, weekly series, activity feed, and
 * AI recommendations below are illustrative placeholders — the backend
 * currently has no dedicated `/analytics` endpoints. Job/candidate counts
 * ARE live, wired to `useJobs`. Swap the placeholder arrays for real data
 * once an analytics endpoint exists (see backend `Score`/`Candidate` tables,
 * which already store everything needed to compute these).
 */
const FUNNEL_STAGES = [
  { label: "Applications", value: 248 },
  { label: "Parsed", value: 210 },
  { label: "Shortlisted", value: 86 },
  { label: "Interviewed", value: 41 },
  { label: "Hired", value: 12 },
];

const WEEKLY_DATA = [
  { day: "Mon", applications: 22, interviews: 4 },
  { day: "Tue", applications: 31, interviews: 6 },
  { day: "Wed", applications: 18, interviews: 5 },
  { day: "Thu", applications: 40, interviews: 9 },
  { day: "Fri", applications: 27, interviews: 7 },
  { day: "Sat", applications: 9, interviews: 2 },
  { day: "Sun", applications: 6, interviews: 1 },
];

const RECENT_ACTIVITY = [
  { id: "1", type: "resume_parsed" as const, message: "Resume Parser Agent processed 6 new resumes for Senior Backend Engineer.", timestamp: new Date(Date.now() - 12 * 60_000).toISOString() },
  { id: "2", type: "match_scored" as const, message: "Skill Matching Agent scored 4 candidates for Product Designer.", timestamp: new Date(Date.now() - 55 * 60_000).toISOString() },
  { id: "3", type: "candidate_shortlisted" as const, message: "Priya Nair was shortlisted for Staff Data Engineer.", timestamp: new Date(Date.now() - 3 * 3_600_000).toISOString() },
  { id: "4", type: "interview_scheduled" as const, message: "AI interview scheduled with 2 candidates for DevOps Lead.", timestamp: new Date(Date.now() - 8 * 3_600_000).toISOString() },
];

const AI_RECOMMENDATIONS = [
  { id: "1", title: "3 candidates are ready for interview", detail: "They scored above 80 in skill matching for open roles." },
  { id: "2", title: "Job description could be improved", detail: "\"Senior Backend Engineer\" is attracting a 34% skill mismatch rate." },
  { id: "3", title: "Review manual-review queue", detail: "5 candidates have been pending review for 3+ days." },
];

export default function DashboardPage() {
  const { user } = useAuth();
  const { data: jobs, isLoading: jobsLoading } = useJobs("OPEN");

  const firstName = user?.full_name?.split(" ")[0] ?? "there";
  const activeJobsCount = jobs?.length ?? 0;

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
        className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end"
      >
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-heading sm:text-3xl">
            Welcome back, {firstName} 👋
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Here&apos;s what your AI hiring agents have been up to.
          </p>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {jobsLoading ? (
          Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-[100px] rounded-2xl" />)
        ) : (
          <>
            <StatCard label="Active Jobs" value={String(activeJobsCount)} icon={Briefcase} accent="primary" delay={0} />
            <StatCard
              label="Candidates in Pipeline"
              value="248"
              icon={Users}
              trend={{ value: 12, positive: true }}
              accent="secondary"
              delay={0.05}
            />
            <StatCard
              label="Interviews Scheduled"
              value="14"
              icon={MessagesSquare}
              trend={{ value: 4, positive: true }}
              accent="accent"
              delay={0.1}
            />
            <StatCard
              label="AI Match Accuracy"
              value="91.4%"
              icon={Sparkles}
              trend={{ value: 2.1, positive: true }}
              accent="primary"
              delay={0.15}
            />
          </>
        )}
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <WeeklyAnalyticsChart data={WEEKLY_DATA} />
        </div>
        <Card>
          <CardHeader>
            <CardTitle>AI Hiring Score</CardTitle>
            <CardDescription>Overall pipeline health this month.</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col items-center justify-center gap-3 pb-8">
            <ScoreRing score={84} size={128} strokeWidth={10} label="/ 100" />
            <p className="text-center text-xs text-muted-foreground">
              Based on match quality, interview pass rate, and time-to-hire.
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-4">
          <HiringFunnelChart stages={FUNNEL_STAGES} />
          <QuickActions />
        </div>
        <div className="space-y-4">
          <AIRecommendations items={AI_RECOMMENDATIONS} />
          <RecentActivity events={RECENT_ACTIVITY} />
        </div>
      </div>

      <LatestCandidates candidates={[]} />
    </div>
  );
}
