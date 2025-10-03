import * as React from 'react'

import { cn } from './utils'

export type SelectOption = {
	value: string
	label: string
}

export interface SelectRootProps
	extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, 'onChange'> {
	value?: string
	defaultValue?: string
	onValueChange?: (value: string) => void
}

type SelectItemElementProps = {
	value: string
	children: React.ReactNode
}

export const SelectItem: React.FC<SelectItemElementProps> = ({ children }) => {
	return <>{children}</>
}
SelectItem.displayName = 'SelectItem'

export const SelectContent: React.FC<React.PropsWithChildren> = ({ children }) => {
	return <>{children}</>
}
SelectContent.displayName = 'SelectContent'

export const SelectTrigger: React.FC<React.PropsWithChildren> = ({ children }) => {
	return <>{children}</>
}
SelectTrigger.displayName = 'SelectTrigger'

export const SelectValue: React.FC<{ placeholder?: string }> = ({ placeholder }) => {
	return <>{placeholder ?? null}</>
}
SelectValue.displayName = 'SelectValue'

export const Select = React.forwardRef<HTMLSelectElement, SelectRootProps>(
	({ className, children, value, defaultValue, onValueChange, ...props }, ref) => {
		// Collect options from SelectContent > SelectItem children
		const items: Array<{ value: string; label: string }> = []

		const collectItems = (nodes: React.ReactNode) => {
			React.Children.forEach(nodes, (child) => {
				if (!React.isValidElement(child)) return
				if ((child.type as any).displayName === 'SelectContent') {
					collectItems(child.props.children)
					return
				}
				if ((child.type as any).displayName === 'SelectItem') {
					const v = child.props.value as string
					const label = typeof child.props.children === 'string'
						? child.props.children
						: String(child.props.children)
					items.push({ value: v, label })
					return
				}
				// Recurse into any other wrappers (e.g., SelectTrigger)
				if (child.props && child.props.children) collectItems(child.props.children)
			})
		}

		collectItems(children)

		const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
			const newValue = e.target.value
			if (onValueChange) onValueChange(newValue)
		}

		return (
			<select
				ref={ref}
				value={value}
				defaultValue={defaultValue}
				onChange={handleChange}
				className={cn(
					'flex h-10 w-full rounded-md border px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none',
					className
				)}
				{...props}
			>
				{items.map((opt) => (
					<option key={opt.value} value={opt.value}>
						{opt.label}
					</option>
				))}
			</select>
		)
	}
)

Select.displayName = 'Select'

export default Select


