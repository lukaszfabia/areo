"use client";

import {
    Navbar,
    NavbarBrand,
    NavbarContent,
    NavbarItem,
    Link,
    DropdownItem,
    DropdownTrigger,
    Dropdown,
    DropdownMenu,
    Avatar,
    Button,
    Drawer,
    DrawerBody,
    DrawerContent,
    DrawerFooter,
    DrawerHeader,
    useDisclosure,
    Checkbox,
    Form,
    Input,
} from "@nextui-org/react";
import React, { FC, ReactNode, useState } from "react";

export const AcmeLogo = () => {
    return (
        <svg fill="none" height="36" viewBox="0 0 32 32" width="36">
            <path
                clipRule="evenodd"
                d="M17.6482 10.1305L15.8785 7.02583L7.02979 22.5499H10.5278L17.6482 10.1305ZM19.8798 14.0457L18.11 17.1983L19.394 19.4511H16.8453L15.1056 22.5499H24.7272L19.8798 14.0457Z"
                fill="currentColor"
                fillRule="evenodd"
            />
        </svg>
    );
};

export const NextNavbar: FC<{ children: ReactNode }> = ({ children }) => {
    // if (isLoading) return  <Spinner color="secondary" label="Loading..." />

    return (
        <>
            <Navbar>
                <NavbarBrand>
                    <AcmeLogo />
                    <p className="font-bold font-rubik">Areo</p>
                </NavbarBrand>

                <NavbarContent className="hidden sm:flex gap-4" justify="center">
                    <NavbarItem>
                        <Link color="foreground" href="#">
                            Features
                        </Link>
                    </NavbarItem>
                    <NavbarItem isActive>
                        <Link aria-current="page" color="secondary" href="#">
                            Customers
                        </Link>
                    </NavbarItem>
                    <NavbarItem>
                        <Link color="foreground" href="#">
                            Integrations
                        </Link>
                    </NavbarItem>
                </NavbarContent>


                {/* logged */}
                {/* <NavbarContent as="div" justify="end">
                    <Dropdown placement="bottom-end">
                        <DropdownTrigger>
                            <Avatar
                                isBordered
                                as="button"
                                className="transition-transform"
                                color="secondary"
                                name="Jason Hughes"
                                size="sm"
                            />
                        </DropdownTrigger>
                        <DropdownMenu aria-label="Profile Actions" variant="flat">
                            <DropdownItem key="profile" className="h-14 gap-2">
                                <p className="font-semibold">Signed in as</p>
                                <p className="font-semibold">zoey@example.com</p>
                            </DropdownItem>
                            <DropdownItem key="weather">Weather</DropdownItem>
                            <DropdownItem key="data">Data</DropdownItem>
                            <DropdownItem key="analytics">Analytics</DropdownItem>
                            <DropdownItem key="settings">Settings</DropdownItem>
                            <DropdownItem key="help_and_feedback">Help & Feedback</DropdownItem>
                            <DropdownItem key="logout" color="danger">
                                Log Out
                            </DropdownItem>
                        </DropdownMenu>
                    </Dropdown>
                </NavbarContent> */}

                <NavbarContent as="div" justify="end">
                    <NotAuth />
                </NavbarContent>

            </Navbar>
            {children}
        </>
    );
}


function NotAuth() {
    const { isOpen, onOpen, onOpenChange } = useDisclosure();
    const [password, setPassword] = useState("");
    const [submitted, setSubmitted] = useState(null);
    const [errors, setErrors] = useState({});

    const getPasswordError = (value: string) => {
        if (value.length < 4) {
            return "Password must be 4 characters or more";
        }
        if ((value.match(/[A-Z]/g) || []).length < 1) {
            return "Password needs at least 1 uppercase letter";
        }
        if ((value.match(/[^a-z]/gi) || []).length < 1) {
            return "Password needs at least 1 symbol";
        }

        return null;
    };

    // const onSubmit = (e: { preventDefault: () => void; currentTarget: HTMLFormElement | undefined; }) => {
    //     e.preventDefault();
    //     const data = Object.fromEntries(new FormData(e.currentTarget));

    //     // Custom validation checks
    //     const newErrors = {};

    //     // Password validation
    //     const passwordError = getPasswordError(data.password);

    //     if (passwordError) {
    //         newErrors.password = passwordError;
    //     }

    //     // Username validation
    //     if (data.name === "admin") {
    //         newErrors.name = "Nice try! Choose a different username";
    //     }

    //     if (Object.keys(newErrors).length > 0) {
    //         setErrors(newErrors);

    //         return;
    //     }

    //     if (data.terms !== "true") {
    //         setErrors({ terms: "Please accept the terms" });

    //         return;
    //     }

    //     // Clear errors and submit
    //     setErrors({});
    //     setSubmitted(data);
    // };

    return (
        <>
            <Avatar
                isBordered
                as="button"
                className="transition-transform"
                color="secondary"
                size="sm"
                onClick={onOpen}
            />
            <Drawer isOpen={isOpen} onOpenChange={onOpenChange}>
                <DrawerContent>
                    {(onClose) => (
                        <>
                            <DrawerHeader className="flex flex-col gap-1">Tell Us Who are you?</DrawerHeader>
                            <DrawerBody>
                                <Form
                                    className="w-full justify-center items-center space-y-4"
                                    validationBehavior="native"
                                    validationErrors={errors}
                                    onReset={() => setSubmitted(null)}
                                // onSubmit={onSubmit}
                                >
                                    <div className="flex flex-col gap-4 max-w-md">
                                        <Input
                                            isRequired
                                            errorMessage={({ validationDetails }) => {
                                                if (validationDetails.valueMissing) {
                                                    return "Please enter your email";
                                                }
                                                if (validationDetails.typeMismatch) {
                                                    return "Please enter a valid email address";
                                                }
                                            }}
                                            label="Email"
                                            labelPlacement="outside"
                                            name="email"
                                            placeholder="Enter your email"
                                            type="email"
                                        />

                                        <Input
                                            isRequired
                                            errorMessage={getPasswordError(password)}
                                            isInvalid={getPasswordError(password) !== null}
                                            label="Password"
                                            labelPlacement="outside"
                                            name="password"
                                            placeholder="Enter your password"
                                            type="password"
                                            value={password}
                                            onValueChange={setPassword}
                                        />


                                        <Checkbox
                                            isRequired
                                            classNames={{
                                                label: "text-small",
                                            }}
                                            // isInvalid={!!errors.terms}
                                            name="terms"
                                            validationBehavior="aria"
                                            value="true"
                                            onValueChange={() => setErrors((prev) => ({ ...prev, terms: undefined }))}
                                        >
                                            Remember me
                                        </Checkbox>

                                        {/* {errors.terms && <span className="text-danger text-small">{errors.terms}</span>} */}
                                    </div>
                                </Form>
                            </DrawerBody>
                            <DrawerFooter>
                                <Button color="danger" variant="light" onPress={onClose}>
                                    Close
                                </Button>
                                <Button color="primary" onPress={onClose}>
                                    Continue
                                </Button>
                            </DrawerFooter>
                        </>
                    )}
                </DrawerContent>
            </Drawer>
        </>
    );
}
