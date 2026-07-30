"use client";

import { useQuery } from "@tanstack/react-query";
import { candidatesApi } from "@/lib/api/candidates";

export function useCandidatesForJob(jobId: string) {
  return useQuery({
    queryKey: ["candidates", "by-job", jobId],
    queryFn: () => candidatesApi.listForJob(jobId),
    enabled: Boolean(jobId),
  });
}

export function useCandidate(candidateId: string) {
  return useQuery({
    queryKey: ["candidates", candidateId],
    queryFn: () => candidatesApi.get(candidateId),
    enabled: Boolean(candidateId),
  });
}
