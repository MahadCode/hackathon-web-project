"use client";

import * as React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import { Telescope } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { PasswordInput } from "@/components/auth/password-input";
import { PasswordStrength } from "@/components/auth/password-strength";
import { authApi } from "@/lib/api/auth";
import { getApiErrorMessage } from "@/lib/api/client";
import type { UserRole } from "@/types/domain";

const ROLE_OPTIONS: { value: UserRole; label: string }[] = [
  { value: "RECRUITER", label: "Recruiter" },
  { value: "HR_MANAGER", label: "HR Manager" },
  { value: "INTERVIEWER", label: "Interviewer" },
  { value: "ADMIN", label: "Admin" },
];

const registerSchema = z.object({
  full_name: z.string().min(1, "Full name is required."),
  email: z.string().email("Enter a valid email address."),
  company_name: z.string().optional(),
  role: z.enum(["ADMIN", "HR_MANAGER", "RECRUITER", "INTERVIEWER"]),
  password: z.string().min(8, "Password must be at least 8 characters."),
});

type RegisterFormValues = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const [passwordValue, setPasswordValue] = React.useState("");

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: { role: "RECRUITER" },
  });

  const selectedRole = watch("role");

  async function onSubmit(values: RegisterFormValues) {
    setIsSubmitting(true);
    try {
      await authApi.register(values);
      toast.success("Account created — welcome to Talent Lens!");
      router.push("/dashboard");
    } catch (error) {
      toast.error(getApiErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col items-center gap-2 text-center lg:hidden">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-brand">
          <Telescope className="h-5 w-5 text-white" />
        </div>
        <span className="text-lg font-semibold text-heading">Talent Lens</span>
      </div>

      <div className="space-y-1.5 text-center lg:text-left">
        <h2 className="text-2xl font-semibold tracking-tight text-heading">Create your account</h2>
        <p className="text-sm text-muted-foreground">Start hiring smarter with AI-powered insights.</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="space-y-1.5">
          <Label htmlFor="full_name">Full name</Label>
          <Input id="full_name" placeholder="Jane Doe" {...register("full_name")} />
          {errors.full_name && <p className="text-xs text-error">{errors.full_name.message}</p>}
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" placeholder="you@company.com" {...register("email")} />
          {errors.email && <p className="text-xs text-error">{errors.email.message}</p>}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1.5">
            <Label htmlFor="company_name">Company</Label>
            <Input id="company_name" placeholder="Acme Corp" {...register("company_name")} />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="role">Role</Label>
            <Select value={selectedRole} onValueChange={(v) => setValue("role", v as UserRole)}>
              <SelectTrigger id="role">
                <SelectValue placeholder="Select role" />
              </SelectTrigger>
              <SelectContent>
                {ROLE_OPTIONS.map((option) => (
                  <SelectItem key={option.value} value={option.value}>
                    {option.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="password">Password</Label>
          <PasswordInput
            id="password"
            placeholder="••••••••"
            {...register("password", {
              onChange: (e) => setPasswordValue(e.target.value),
            })}
          />
          <PasswordStrength password={passwordValue} />
          {errors.password && <p className="text-xs text-error">{errors.password.message}</p>}
        </div>

        <Button type="submit" className="w-full" size="lg" isLoading={isSubmitting}>
          Create account
        </Button>
      </form>

      <p className="text-center text-sm text-muted-foreground">
        Already have an account?{" "}
        <Link href="/login" className="font-medium text-primary hover:underline">
          Sign in
        </Link>
      </p>
    </div>
  );
}
