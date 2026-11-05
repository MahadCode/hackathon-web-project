"use client";

import * as React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";

import { BrandLogo } from "@/components/brand/logo";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { PasswordInput } from "@/components/auth/password-input";
import { authApi } from "@/lib/api/auth";
import { getApiErrorMessage } from "@/lib/api/client";
import { homeForRole } from "@/lib/auth/roles";

const loginSchema = z.object({
  email: z.string().email("Enter a valid email address."),
  password: z.string().min(1, "Password is required."),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = React.useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({ resolver: zodResolver(loginSchema) });

  async function onSubmit(values: LoginFormValues) {
    setIsSubmitting(true);
    try {
      await authApi.login(values);
      const me = await authApi.me();
      toast.success("Welcome back.");
      router.push(homeForRole(me.role));
    } catch (error) {
      toast.error(getApiErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col items-center gap-2 text-center lg:hidden">
        <BrandLogo />
      </div>

      <div className="space-y-1.5">
        <p className="label-mono text-muted-foreground">Sign in</p>
        <h2 className="text-2xl font-normal tracking-tight text-heading">Welcome back</h2>
        <p className="text-sm text-muted-foreground">Continue to your workspace.</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="space-y-1.5">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" placeholder="you@company.com" {...register("email")} />
          {errors.email && <p className="text-xs text-error">{errors.email.message}</p>}
        </div>

        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <Label htmlFor="password">Password</Label>
            <Link href="/forgot-password" className="text-xs text-muted-foreground hover:text-heading">
              Forgot password?
            </Link>
          </div>
          <PasswordInput id="password" placeholder="••••••••" {...register("password")} />
          {errors.password && <p className="text-xs text-error">{errors.password.message}</p>}
        </div>

        <Button type="submit" className="w-full" size="lg" isLoading={isSubmitting}>
          ·· Launch
        </Button>
      </form>

      <p className="text-center text-sm text-muted-foreground">
        Hiring?{" "}
        <Link href="/register" className="text-heading underline-offset-4 hover:underline">
          Create a workspace
        </Link>
        <span className="mx-2 text-heading/20">·</span>
        Applying?{" "}
        <Link href="/register?as=candidate" className="text-heading underline-offset-4 hover:underline">
          Create a candidate account
        </Link>
      </p>
    </div>
  );
}
