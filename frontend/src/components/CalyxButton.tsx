import React from "react"
import { Button } from "@/components/ui/button"
import type { VariantProps } from "class-variance-authority"
import { buttonVariants } from "@/components/ui/button"
import { Button as ButtonPrimitive } from "@base-ui/react/button"

export type CalyxButtonProps = ButtonPrimitive.Props & VariantProps<typeof buttonVariants>

export const CalyxButton = React.forwardRef<HTMLButtonElement, CalyxButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <Button
        className={className}
        variant={variant}
        size={size}
        ref={ref}
        {...props}
      />
    )
  }
)
CalyxButton.displayName = "CalyxButton"
