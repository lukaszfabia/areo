import { passwordRegex } from "@/lib/config";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Checkbox, Form, FormProps, Input, } from "@nextui-org/react";
import { FC, ReactNode, useState } from "react";

export interface GenericFormProps extends FormProps {
    // for password strong check
    skipValidation?: boolean
    children: ReactNode;
    className?: string;
}

export const GenericForm: FC<GenericFormProps> = ({ skipValidation = true, children, className = "", ...rest }) => {
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
        <Form
            className={`flex flex-col gap-6 w-full max-w-md mx-auto ${className}`}
            validationBehavior="native"
            autoCapitalize="none"
            {...rest}
        >
            <Input
                isRequired
                label="Email"
                type="email"
                variant="underlined"
                errorMessage="Please enter a valid email"
                placeholder="e.g., joe.doe@example.com"
                isClearable
            />

            <Input
                variant="underlined"
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

            <div className="flex justify-end">
                <Checkbox>
                    Remember me
                </Checkbox>
            </div>


            {children}
        </Form>
    );
};
