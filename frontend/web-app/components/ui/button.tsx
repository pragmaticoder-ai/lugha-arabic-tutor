import { cn } from "@/lib/utils";
import * as React from "react";

type Variant = "primary" | "gold" | "ghost";
const styles: Record<Variant, string> = {
  primary: "bg-lugha-600 text-white hover:bg-lugha-700 active:bg-lugha-700",
  gold: "bg-gold-500 text-white hover:bg-gold-600",
  ghost: "bg-transparent text-lugha-600 hover:bg-lugha-50 border border-lugha-200",
};

export function Button({
  className, variant = "primary", ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant }) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-xl px-4 py-3",
        "text-sm font-semibold transition-colors min-h-11 w-full",
        "focus:outline-none focus:ring-2 focus:ring-lugha-600/30 disabled:opacity-50",
        styles[variant], className
      )}
      {...props}
    />
  );
}
