"use client";

import React, { FC } from "react";
import { NextUIProvider } from '@nextui-org/react'
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { themes } from "@/lib/config";

export const ThemeProvider: FC<{ children: React.ReactNode }> = ({ children }) => {
    return (
        <NextUIProvider>
            <NextThemesProvider attribute="class" defaultTheme="system" themes={[themes.dark, themes.light]}>
                {children}
            </NextThemesProvider>
        </NextUIProvider>
    )
} 