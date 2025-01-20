import { Input } from "@nextui-org/react";

export default function Email() {
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