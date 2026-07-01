import React from "react"
import { Input } from "@/components/ui/input"

export type CalyxInputProps = React.ComponentProps<typeof Input>

export const CalyxInput = React.forwardRef<HTMLInputElement, CalyxInputProps>(
  ({ className, ...props }, ref) => {
    return <Input ref={ref} className={className} {...props} />
  }
)
CalyxInput.displayName = "CalyxInput"
