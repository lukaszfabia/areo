import { Input } from "@heroui/react";


export function Email() {
    return (
        <Input
            isRequired
            label="Email"
            type="email"
            name="email"
            id="email"
            variant="underlined"
            errorMessage="Please enter a valid email"
            placeholder="e.g., joe.doe@example.com"
            isClearable
        />
    )
}


export function EmailUpdate({ defaultValue }: { defaultValue: string }) {
    return <Input
        className="max-w-xs"
        defaultValue={defaultValue}
        label="Email"
        type="email"
        variant="bordered"
        id="email"
        name="email"
        errorMessage="Please enter a valid email"
        isClearable
    />
}