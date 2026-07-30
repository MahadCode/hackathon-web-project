"use client";

import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { StatCard } from "@/components/dashboard/stat-card";
import { Target, TrendingUp, Clock, Percent } from "lucide-react";

/**
 * NOTE ON SAMPLE DATA: the backend does not yet expose analytics
 * aggregation endpoints, so the series below are illustrative. The
 * `Score`, `Candidate`, and `Interview` tables already store everything
 * needed to compute these server-side — wire this page up to a future
 * `/analytics/*` endpoint by swapping the arrays for query results.
 */
const CANDIDATE_SOURCES = [
  { source: "LinkedIn", value: 128 },
  { source: "Referral", value: 64 },
  { source: "Job Board", value: 91 },
  { source: "Direct", value: 40 },
  { source: "Agency", value: 22 },
];

const SKILL_DISTRIBUTION = [
  { name: "Python", value: 32 },
  { name: "React/TS", value: 27 },
  { name: "Cloud/DevOps", value: 18 },
  { name: "Data/ML", value: 15 },
  { name: "Other", value: 8 },
];

const HIRING_TRENDS = [
  { month: "Feb", hires: 4, offers: 7 },
  { month: "Mar", hires: 6, offers: 9 },
  { month: "Apr", hires: 5, offers: 8 },
  { month: "May", hires: 9, offers: 12 },
  { month: "Jun", hires: 7, offers: 10 },
  { month: "Jul", hires: 12, offers: 15 },
];

const PIE_COLORS = ["#059669", "#10B981", "#34D399", "#6EE7B7", "#A7F3D0"];

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-heading">Analytics</h1>
        <p className="mt-1 text-sm text-muted-foreground">Hiring performance and AI accuracy across your pipeline.</p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Interview Success Rate" value="68%" icon={Target} trend={{ value: 5, positive: true }} />
        <StatCard label="AI Match Accuracy" value="91.4%" icon={Percent} trend={{ value: 2.1, positive: true }} accent="secondary" />
        <StatCard label="Avg. Time to Hire" value="14 days" icon={Clock} trend={{ value: 8, positive: false }} accent="accent" />
        <StatCard label="Hiring Trend" value="+23%" icon={TrendingUp} trend={{ value: 23, positive: true }} />
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Candidate Sources</CardTitle>
            <CardDescription>Where your applicants are coming from.</CardDescription>
          </CardHeader>
          <CardContent className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={CANDIDATE_SOURCES}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
                <XAxis dataKey="source" tick={{ fontSize: 12, fill: "#475569" }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 12, fill: "#475569" }} axisLine={false} tickLine={false} width={28} />
                <Tooltip contentStyle={{ borderRadius: 12, border: "1px solid #E2E8F0", fontSize: 13 }} />
                <Bar dataKey="value" fill="#059669" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Skill Distribution</CardTitle>
            <CardDescription>Top skill categories across all candidates.</CardDescription>
          </CardHeader>
          <CardContent className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={SKILL_DISTRIBUTION} dataKey="value" nameKey="name" innerRadius={60} outerRadius={90} paddingAngle={2}>
                  {SKILL_DISTRIBUTION.map((entry, i) => (
                    <Cell key={entry.name} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ borderRadius: 12, border: "1px solid #E2E8F0", fontSize: 13 }} />
                <Legend iconType="circle" wrapperStyle={{ fontSize: 12 }} />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Hiring Trends</CardTitle>
          <CardDescription>Offers extended vs. hires confirmed, by month.</CardDescription>
        </CardHeader>
        <CardContent className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={HIRING_TRENDS}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
              <XAxis dataKey="month" tick={{ fontSize: 12, fill: "#475569" }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 12, fill: "#475569" }} axisLine={false} tickLine={false} width={28} />
              <Tooltip contentStyle={{ borderRadius: 12, border: "1px solid #E2E8F0", fontSize: 13 }} />
              <Legend iconType="circle" wrapperStyle={{ fontSize: 12 }} />
              <Line type="monotone" dataKey="offers" stroke="#34D399" strokeWidth={2} dot={{ r: 3 }} />
              <Line type="monotone" dataKey="hires" stroke="#059669" strokeWidth={2.5} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
