"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { useQuery, useQueryClient } from "@tanstack/react-query";

import { authApi } from "@/lib/api/auth";
import { tokenStorage } from "@/lib/api/client";
import type { User } from "@/types/domain";

interface AuthContextValue {
  user: User | undefined;
  isLoading: boolean;
  isAuthenticated: boolean;
  logout: () => Promise<void>;
}

const AuthContext = React.createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [hasToken, setHasToken] = React.useState(false);

  React.useEffect(() => {
    setHasToken(Boolean(tokenStorage.getAccessToken()));
  }, []);

  const { data: user, isLoading } = useQuery({
    queryKey: ["auth", "me"],
    queryFn: authApi.me,
    enabled: hasToken,
    retry: false,
  });

  const logout = React.useCallback(async () => {
    await authApi.logout();
    queryClient.clear();
    router.push("/login");
  }, [queryClient, router]);

  const value: AuthContextValue = {
    user,
    isLoading: hasToken && isLoading,
    isAuthenticated: Boolean(user),
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = React.useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider.");
  return ctx;
}
