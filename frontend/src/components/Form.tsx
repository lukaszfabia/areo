import { Checkbox, Form, FormProps } from "@nextui-org/react";
import { FC, ReactNode, RefObject } from "react";
import Email from "./ui/Email";
import Password from "./ui/Password";

export interface GenericFormProps extends FormProps {
    // for password strong check
    refOnRememberMe: RefObject<HTMLInputElement | null>
    skipValidation?: boolean
    children: ReactNode;
    className?: string;
}

export const GenericForm: FC<GenericFormProps> = ({ refOnRememberMe, skipValidation = true, children, className = "", ...rest }) => {
    return (
        <Form
            className={`flex flex-col gap-6 w-full max-w-md mx-auto ${className}`}
            validationBehavior="native"
            autoCapitalize="none"
            {...rest}
        >
            <Email />

            <Password skipValidation={skipValidation} />

            <div className="flex justify-end">
                <Checkbox ref={refOnRememberMe}>
                    Remember me
                </Checkbox>
            </div>


            {children}
        </Form>
    );
};
