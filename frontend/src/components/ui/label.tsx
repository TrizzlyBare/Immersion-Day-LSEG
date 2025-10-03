import * as React from 'react'

import { cn } from './utils'

export const Label: React.FC<React.LabelHTMLAttributes<HTMLLabelElement>> = ({ className, ...props }) => {
	return (
		<label
			className={cn('block text-sm font-medium', className)}
			{...props}
		/>
	)
}

Label.displayName = 'Label'
