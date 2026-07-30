import { apiClient } from "@/lib/api/client";
import type { Candidate } from "@/types/domain";

/** Service layer for candidate endpoints (`/candidates/*`). */
export const candidatesApi = {
  async listForJob(jobId: string, params?: { offset?: number; limit?: number }): Promise<Candidate[]> {
    const { data } = await apiClient.get<Candidate[]>("/candidates", { params: { job_id: jobId, ...params } });
    return data;
  },

  async get(candidateId: string): Promise<Candidate> {
    const { data } = await apiClient.get<Candidate>(`/candidates/${candidateId}`);
    return data;
  },
};
