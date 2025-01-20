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
import React, { FC, ReactNode, useEffect, useState } from "react";
import { authMenu, notAuthMenu } from "@/lib/config";
import { Link as lnk } from "@/lib/config";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import { useAuth } from "@/providers/Auth";
import { usePathname } from "next/navigation";

// function isActive(path: string, dest: string): boolean {
//     const res = path.split("/").pop()?.replaceAll("#", "")
//     return res == dest.toLowerCase()
// }

export const NextNavbar: FC<{ children: ReactNode }> = ({ children }) => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const { user, isLoading } = useAuth();
    const [isMounted, setIsMounted] = useState(false);
    // const path = usePathname();

    useEffect(() => {
        setIsMounted(true);
    }, []);

    if (isLoading || !isMounted) return null;

    const menuItems = user ? authMenu : notAuthMenu

    return (
        <div>
            <Navbar className="fixed top-0 w-full z-50 transition-colors duration-300">
                <NavbarBrand className="text-white font-extrabold text-3xl" as={Link} href="/">
                    Areo
                </NavbarBrand>

                <NavbarContent className="hidden sm:flex gap-4">
                    {menuItems.map((item: lnk, index: number) => (
                        <NavbarItem key={`${item.text}- ${index}`} >
                            <Link className="w-full text-gray-300" href={item.dest}>
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

                <NavbarMenu className={`sm:hidden ${isMenuOpen ? 'flex' : 'hidden'} flex-col`}>
                    {menuItems.map((item: lnk, index: number) => (
                        <NavbarMenuItem key={`${item.text}- ${index}`}>
                            <Link className="w-full text-gray-300" href={item.dest}>
                                {item.text}
                            </Link>
                        </NavbarMenuItem>
                    ))}
                </NavbarMenu>
            </Navbar>
            {children}
        </div>
    );
};
