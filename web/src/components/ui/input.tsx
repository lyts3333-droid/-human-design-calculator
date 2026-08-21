import { forwardRef } from "react";
import { cn } from "@/lib/utils";

export const Input = forwardRef<
  HTMLInputElement,
  React.InputHTMLAttributes<HTMLInputElement>
>(({ className, ...props }, ref) => (
  <input
    ref={ref}
    className={cn(
      "h-12 w-full rounded-2xl border border-white/10 bg-white/[0.04] px-4 text-sm text-foreground outline-none transition-all duration-300",
      "placeholder:text-muted/70",
      "focus:border-primary/50 focus:bg-white/[0.06] focus:shadow-[0_0_0_4px_rgba(111,108,255,0.15)]",
      className
    )}
    {...props}
  />
));
Input.displayName = "Input";

export const Select = forwardRef<
  HTMLSelectElement,
  React.SelectHTMLAttributes<HTMLSelectElement>
>(({ className, children, ...props }, ref) => (
  <select
    ref={ref}
    className={cn(
      "h-12 w-full appearance-none rounded-2xl border border-white/10 bg-white/[0.04] px-4 text-sm text-foreground outline-none transition-all duration-300",
      "focus:border-primary/50 focus:shadow-[0_0_0_4px_rgba(111,108,255,0.15)]",
      className
    )}
    {...props}
  >
    {children}
  </select>
));
Select.displayName = "Select";

export function FieldLabel({
  children,
  htmlFor,
}: {
  children: React.ReactNode;
  htmlFor?: string;
}) {
  return (
    <label
      htmlFor={htmlFor}
      className="mb-2 block text-xs font-medium tracking-[0.08em] text-muted"
    >
      {children}
    </label>
  );
}
