"use client";
import Loading from "@/components/ui/Spinner";
import { ReactNode, useEffect, useState } from "react";

export default function ProfileLayout({ children }: { children: ReactNode }) {
    const [isMounted, setIsMounted] = useState(false);

    useEffect(() => { setIsMounted(true) }, [])

    if (!isMounted) return <Loading />

    return (
        <main className="flex items-center justify-center py-10 min-h-screen bg-slate-950 text-white">
            {children}
        </main>
    );
}
