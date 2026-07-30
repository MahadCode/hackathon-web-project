/**
 * Domain types mirrored from the FastAPI backend's Pydantic schemas
 * (see backend/app/schemas/*.py). Keeping these hand-in-sync avoids a
 * runtime schema-generation dependency while the API surface is stable.
 */

export type UserRole = "ADMIN" | "HR_MANAGER" | "RECRUITER" | "INTERVIEWER";

export type JobStatus = "DRAFT" | "OPEN" | "CLOSED" | "ARCHIVED";

export type CandidateStatus =
  | "NEW"
  | "PARSED"
  | "SHORTLISTED"
  | "MANUAL_REVIEW"
  | "REJECTED"
  | "INTERVIEWING"
  | "HIRED"
  | "NOT_HIRED";

export interface User {
  id: string;
  full_name: string;
  email: string;
  role: UserRole;
  company_name: string | null;
  profile_image: string | null;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login: string | null;
}

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Job {
  id: string;
  title: string;
  description: string;
  requirements: string;
  status: JobStatus;
  created_by_id: string;
  created_at: string;
  updated_at: string;
}

export interface ParsedCandidateProfile {
  name: string | null;
  email: string | null;
  phone: string | null;
  skills: string[];
  experience: string[];
  education: string[];
  projects: string[];
  certifications: string[];
  github: string | null;
  linkedin: string | null;
}

export interface Candidate {
  id: string;
  job_id: string;
  full_name: string | null;
  email: string | null;
  github_url: string | null;
  status: CandidateStatus;
  parsed_profile: ParsedCandidateProfile | null;
  match_percentage: number | null;
  created_at: string;
  updated_at: string;
}

export interface MatchingResult {
  match_percentage: number;
  missing_skills: string[];
  extra_skills: string[];
  experience_comparison: string;
  explanation: string;
}

export interface ScoreBreakdown {
  skills_score: number;
  experience_score: number;
  projects_score: number;
  education_score: number;
  certifications_score: number;
}

export interface ScoringResult {
  breakdown: ScoreBreakdown;
  total_score: number;
  reasoning: string;
}

export type DecisionType = "SHORTLIST" | "MANUAL_REVIEW" | "REJECT";

export interface DecisionResult {
  decision: DecisionType;
  reason: string;
}

export interface EmailContent {
  subject: string;
  body: string;
}

export interface WorkflowEvaluateResponse {
  parsed_candidate: ParsedCandidateProfile;
  matching_result: MatchingResult;
  score_result: ScoringResult;
  decision: DecisionResult;
  email_content: EmailContent | null;
  final_recommendation: string | null;
}

export interface InterviewQuestionResponse {
  question: string;
  focus_area: string;
  is_follow_up: boolean;
}

export interface InterviewEvaluateResponse {
  interview_id: string;
  overall_assessment: string;
  passed: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  offset: number;
  limit: number;
}

export interface ApiErrorBody {
  error: string;
  message: string;
  details?: Record<string, unknown> | null;
}

export interface AppNotification {
  id: string;
  type: "resume_processed" | "candidate_shortlisted" | "interview_scheduled" | "new_application" | "ai_recommendation";
  title: string;
  message: string;
  read: boolean;
  created_at: string;
}
