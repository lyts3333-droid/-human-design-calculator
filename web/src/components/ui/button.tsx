import { cva, type VariantProps } from "class-variance-authority";
import { forwardRef } from "react";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-full text-sm font-semibold tracking-wide transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary:
          "bg-gradient-to-r from-primary via-[#8B7CFF] to-secondary text-white shadow-[0_0_28px_rgba(111,108,255,0.35)] hover:shadow-[0_0_40px_rgba(78,197,255,0.5)] hover:scale-[1.02]",
        secondary:
          "border border-white/15 bg-white/5 text-foreground backdrop-blur-xl hover:border-accent/40 hover:bg-white/10 hover:shadow-[0_0_24px_rgba(199,168,111,0.2)]",
        outline:
          "border border-white/25 bg-transparent text-foreground backdrop-blur-xl hover:bg-white/5 hover:border-white/40",
        ghost: "text-muted hover:bg-white/5 hover:text-foreground",
      },
      size: {
        default: "h-12 px-7",
        sm: "h-10 px-5 text-xs",
        lg: "h-14 px-9 text-base",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  )
);
Button.displayName = "Button";
