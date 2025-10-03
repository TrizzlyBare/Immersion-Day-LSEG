import * as React from 'react'

import { cn } from './utils'

export const Input = React.forwardRef<
	HTMLInputElement,
	React.InputHTMLAttributes<HTMLInputElement>
>(({ className, ...props }, ref) => {
	return (
		<input
			ref={ref}
			className={cn(
				'flex h-10 w-full rounded-md border px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none',
				className
			)}
			{...props}
		/>
	)
})

Input.displayName = 'Input'
