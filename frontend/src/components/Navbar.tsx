"use client";

import {
    Navbar,
    NavbarBrand,
    NavbarContent,
    NavbarItem,
    Link,
    NavbarMenuToggle,
    NavbarMenu,
    NavbarMenuItem,
} from "@nextui-org/react";
import React, { FC, ReactNode, useState } from "react";
import { menu } from "@/lib/config";
import { Link as lnk } from "@/lib/config";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars } from "@fortawesome/free-solid-svg-icons";

export const NextNavbar: FC<{ children: ReactNode }> = ({ children }) => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);


    return (
        <div>
            <Navbar
                className="fixed top-0 w-full z-50 transition-colors duration-300"
            >

                <NavbarBrand>
                    <button onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })} className="text-white font-bold">Areo</button>
                </NavbarBrand>

                <NavbarContent className="hidden sm:flex gap-4">
                    {menu.map((item: lnk, index: number) => (
                        <NavbarItem key={`${item.text}- ${index}`}>
                            <Link
                                className="w-full text-gray-300"
                                href={item.dest}
                                size="lg"
                            >
                                {item.text}
                            </Link>
                        </NavbarItem>
                    ))}
                </NavbarContent>

                <NavbarContent className="sm:hidden flex text-white">
                    <NavbarMenuToggle
                        icon={<FontAwesomeIcon icon={faBars} />}
                        aria-label={isMenuOpen ? "Close menu" : "Open menu"}
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                    />
                </NavbarContent>

                <NavbarMenu className="sm:hidden flex">
                    {menu.map((item: lnk, index: number) => (
                        <NavbarMenuItem key={`${item.text}- ${index}`}>
                            <Link
                                className="w-full text-gray-300"
                                href={item.dest}
                                size="lg"
                            >
                                {item.text}
                            </Link>
                        </NavbarMenuItem>
                    ))}
                </NavbarMenu>
            </Navbar>
            {children}
        </div >
    );
};
