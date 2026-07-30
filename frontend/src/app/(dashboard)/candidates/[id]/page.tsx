"use client";

import * as React from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";
import { ArrowLeft, Github, Linkedin, Mail, Phone, Sparkles, MessagesSquare } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Progress } from "@/components/ui/progress";
import { ScoreRing } from "@/components/shared/score-ring";
import { CandidateStatusBadge } from "@/components/candidates/candidate-status-badge";
import { useCandidate } from "@/lib/hooks/use-candidates";
import { useEvaluateCandidate } from "@/lib/hooks/use-workflow";
import { getApiErrorMessage } from "@/lib/api/client";
import { getInitials } from "@/lib/utils/cn";

export default function CandidateDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();

  const { data: candidate, isLoading } = useCandidate(params.id);
  const evaluate = useEvaluateCandidate();
  const [result, setResult] = React.useState<Awaited<ReturnType<typeof evaluate.mutateAsync>> | null>(null);

  async function handleEvaluate() {
    try {
      const data = await evaluate.mutateAsync({ candidateId: params.id });
      setResult(data);
      toast.success("AI evaluation complete.");
    } catch (error) {
      toast.error(getApiErrorMessage(error));
    }
  }

  if (isLoading || !candidate) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-64 rounded-2xl" />
      </div>
    );
  }

  const profile = candidate.parsed_profile;

  return (
    <div className="space-y-6">
      <Link
        href="/candidates"
        className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-heading"
      >
        <ArrowLeft className="h-3.5 w-3.5" /> Back to candidates
      </Link>

      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div className="flex items-center gap-4">
          <Avatar className="h-14 w-14">
            <AvatarFallback className="text-base">{getInitials(candidate.full_name)}</AvatarFallback>
          </Avatar>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-semibold tracking-tight text-heading">
                {candidate.full_name ?? "Unnamed candidate"}
              </h1>
              <CandidateStatusBadge status={candidate.status} />
            </div>
            <div className="mt-1 flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
              {candidate.email && (
                <span className="flex items-center gap-1">
                  <Mail className="h-3 w-3" /> {candidate.email}
                </span>
              )}
              {profile?.phone && (
                <span className="flex items-center gap-1">
                  <Phone className="h-3 w-3" /> {profile.phone}
                </span>
              )}
              {candidate.github_url && (
                <a
                  href={candidate.github_url}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-1 hover:text-primary"
                >
                  <Github className="h-3 w-3" /> GitHub
                </a>
              )}
              {profile?.linkedin && (
                <a
                  href={profile.linkedin}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-1 hover:text-primary"
                >
                  <Linkedin className="h-3 w-3" /> LinkedIn
                </a>
              )}
            </div>
          </div>
        </div>

        <div className="flex gap-2">
          <Button variant="outline" asChild>
            <Link href="/interviews">
              <MessagesSquare className="h-4 w-4" /> Start Interview
            </Link>
          </Button>
          <Button onClick={handleEvaluate} isLoading={evaluate.isPending}>
            <Sparkles className="h-4 w-4" /> Run AI Evaluation
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="space-y-4 lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Skills</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-wrap gap-1.5">
              {profile?.skills.length ? (
                profile.skills.map((skill) => (
                  <Badge key={skill} variant="secondary">
                    {skill}
                  </Badge>
                ))
              ) : (
                <p className="text-sm text-muted-foreground">No skills parsed yet.</p>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Experience</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {profile?.experience.length ? (
                profile.experience.map((entry, i) => (
                  <p key={i} className="text-sm text-muted-foreground">
                    • {entry}
                  </p>
                ))
              ) : (
                <p className="text-sm text-muted-foreground">No experience parsed yet.</p>
              )}
            </CardContent>
          </Card>

          {result && (
            <Card className="border-primary/20">
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-primary" />
                  <CardTitle>AI Recommendation</CardTitle>
                </div>
                <CardDescription>{result.decision.reason}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
                  {Object.entries(result.score_result.breakdown).map(([key, value]) => (
                    <div key={key} className="space-y-1.5">
                      <div className="flex items-center justify-between text-xs">
                        <span className="capitalize text-muted-foreground">
                          {key.replace("_score", "").replace("_", " ")}
                        </span>
                        <span className="font-medium text-heading">{Math.round(value)}</span>
                      </div>
                      <Progress value={value} />
                    </div>
                  ))}
                </div>
                {result.email_content && (
                  <div className="rounded-xl border border-border bg-muted/40 p-4">
                    <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                      Generated Email
                    </p>
                    <p className="mt-1 text-sm font-semibold text-heading">{result.email_content.subject}</p>
                    <p className="mt-1 whitespace-pre-wrap text-sm text-muted-foreground">
                      {result.email_content.body}
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </div>

        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Match Score</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col items-center gap-3">
              <ScoreRing
                score={result?.score_result.total_score ?? candidate.match_percentage ?? 0}
                size={112}
                label="/ 100"
              />
              {result && (
                <div className="w-full space-y-2 pt-2 text-sm">
                  <p className="font-medium text-heading">Missing skills</p>
                  <div className="flex flex-wrap gap-1.5">
                    {result.matching_result.missing_skills.length ? (
                      result.matching_result.missing_skills.map((skill) => (
                        <Badge key={skill} variant="error">
                          {skill}
                        </Badge>
                      ))
                    ) : (
                      <p className="text-xs text-muted-foreground">None — full skill match.</p>
                    )}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {profile?.certifications.length ? (
            <Card>
              <CardHeader>
                <CardTitle>Certifications</CardTitle>
              </CardHeader>
              <CardContent className="space-y-1.5">
                {profile.certifications.map((cert, i) => (
                  <p key={i} className="text-sm text-muted-foreground">
                    • {cert}
                  </p>
                ))}
              </CardContent>
            </Card>
          ) : null}
        </div>
      </div>
    </div>
  );
}
