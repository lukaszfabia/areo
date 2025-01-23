import { Input } from "@heroui/react";

export function UsernameUpdate({ defaultValue }: { defaultValue: string }) {
    return <Input
        className="max-w-xs"
        defaultValue={defaultValue}
        label="Username"
        type="text"
        variant="bordered"
        isClearable
        placeholder="Enter your new username"
    />
}