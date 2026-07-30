"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { Loader2 } from "lucide-react";

import { AppShell } from "@/components/layout/app-shell";
import { useAuth } from "@/lib/hooks/use-auth";
import { tokenStorage } from "@/lib/api/client";

export default function DashboardGroupLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { isLoading, isAuthenticated } = useAuth();
  const [checkedToken, setCheckedToken] = React.useState(false);

  React.useEffect(() => {
    if (!tokenStorage.getAccessToken()) {
      router.replace("/login");
      return;
    }
    setCheckedToken(true);
  }, [router]);

  if (!checkedToken || isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <Loader2 className="h-6 w-6 animate-spin text-primary" />
      </div>
    );
  }

  return <AppShell>{children}</AppShell>;
}
