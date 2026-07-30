import { apiClient, tokenStorage } from "@/lib/api/client";
import type { TokenPair, User, UserRole } from "@/types/domain";

export interface RegisterPayload {
  full_name: string;
  email: string;
  password: string;
  role: UserRole;
  company_name?: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

/** Service layer for authentication endpoints (`/auth/*`). */
export const authApi = {
  async register(payload: RegisterPayload): Promise<{ user: User; tokens: TokenPair }> {
    const { data } = await apiClient.post("/auth/register", payload);
    tokenStorage.setTokens(data.tokens);
    return data;
  },

  async login(payload: LoginPayload): Promise<TokenPair> {
    const { data } = await apiClient.post<TokenPair>("/auth/login", payload);
    tokenStorage.setTokens(data);
    return data;
  },

  async logout(): Promise<void> {
    const refreshToken = tokenStorage.getRefreshToken();
    if (refreshToken) {
      await apiClient.post("/auth/logout", { refresh_token: refreshToken }).catch(() => undefined);
    }
    tokenStorage.clear();
  },

  async forgotPassword(email: string): Promise<void> {
    await apiClient.post("/auth/forgot-password", { email });
  },

  async resetPassword(resetToken: string, newPassword: string): Promise<void> {
    await apiClient.post("/auth/reset-password", { reset_token: resetToken, new_password: newPassword });
  },

  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    await apiClient.post("/auth/change-password", {
      current_password: currentPassword,
      new_password: newPassword,
    });
  },

  async me(): Promise<User> {
    const { data } = await apiClient.get<User>("/auth/me");
    return data;
  },

  async updateProfile(payload: { full_name?: string; company_name?: string }): Promise<User> {
    const { data } = await apiClient.put<User>("/auth/profile", payload);
    return data;
  },
};
