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
    Button,
} from "@heroui/react";
import React, { FC, ReactNode, useEffect, useState } from "react";
import { authMenu, notAuthMenu } from "@/lib/config";
import { Link as lnk } from "@/lib/config";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import { useAuth } from "@/providers/Auth";


export const NextNavbar: FC<{ children: ReactNode }> = ({ children }) => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const { user, isLoading, logout } = useAuth();
    const [isMounted, setIsMounted] = useState(false);

    useEffect(() => {
        setIsMounted(true);
    }, []);

    if (isLoading || !isMounted) return null;

    const menuItems = user ? authMenu : notAuthMenu

    return (
        <div>
            <Navbar className="fixed top-0 w-full z-50 transition-colors duration-300">
                <NavbarBrand>
                    <Link href="/" className="text-white font-extrabold text-3xl w-fit">
                        Areo</Link>
                </NavbarBrand>

                <NavbarContent className="hidden sm:flex gap-4">
                    {menuItems.map((item: lnk, index: number) => (
                        <NavbarItem key={`${item.text}- ${index}`} >
                            <Link className="w-full text-gray-300" href={item.dest} onPress={item.dest === "#" ? logout : () => { }}>
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
                            <Link className="w-full text-gray-300" href={item.dest} onPress={item.dest === "#" ? logout : () => { }}>
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
