"use client";

import React, { FC } from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { themes } from "@/lib/config";
import { HeroUIProvider } from "@heroui/react";

export const ThemeProvider: FC<{ children: React.ReactNode }> = ({ children }) => {
    return (
        <HeroUIProvider>
            <NextThemesProvider attribute="class" defaultTheme="system" themes={[themes.dark, themes.light]}>
                {children}
            </NextThemesProvider>
        </HeroUIProvider>
    )
} 