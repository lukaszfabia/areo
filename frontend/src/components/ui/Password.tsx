import { passwordRegex } from "@/lib/config";
import { faEyeSlash, faEye } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Input } from "@heroui/react";

import { useState } from "react";

export function Password({ skipValidation }: { skipValidation: boolean }) {
    const [isVisible, setIsVisible] = useState(false);
    const toggleVisibility = () => setIsVisible(!isVisible);

    const validatePassword = (value: string) => {
        if (skipValidation) {
            return
        }

        if (!value) {
            return "password is required";
        } else if (!passwordRegex.test(value)) {
            return "password is too weak";
        } else {
            return null;
        }
    };


    return (
        <Input
            required
            variant="underlined"
            name="password"
            id="password"
            errorMessage="Please enter a strong password"
            endContent={
                <button
                    aria-label="Toggle password visibility"
                    className="focus:outline-none text-gray-500 hover:text-gray-700 transition-colors"
                    type="button"
                    onClick={toggleVisibility}
                >
                    <FontAwesomeIcon icon={isVisible ? faEyeSlash : faEye} className="mr-2" />
                </button>
            }
            label="Password"
            placeholder="Enter your password"
            type={isVisible ? "text" : "password"}
            validate={validatePassword}
        />
    )
}

export function PasswordUpdate() {
    const [isVisible, setIsVisible] = useState(false);
    const toggleVisibility = () => setIsVisible(!isVisible);

    const validatePassword = (value: string) => {
        if (!passwordRegex.test(value)) {
            return "password is too weak";
        } else {
            return null;
        }
    };


    return (
        <Input
            className="max-w-xs"
            variant="bordered"
            name="password"
            id="password"
            errorMessage="Please enter a strong password"
            endContent={
                <button
                    aria-label="Toggle password visibility"
                    className="focus:outline-none text-gray-500 hover:text-gray-700 transition-colors"
                    type="button"
                    onClick={toggleVisibility}
                >
                    <FontAwesomeIcon icon={isVisible ? faEyeSlash : faEye} className="mr-1" />
                </button>
            }
            defaultValue=""
            label="Password"
            placeholder="Enter your new password"
            type={isVisible ? "text" : "password"}
            validate={validatePassword}
            isInvalid
        />
    )
}