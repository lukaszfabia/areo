"use client";

import { ReactNode } from "react";

export default function LoginLayout({ children }: { children: ReactNode }) {
    return (
        <main className="form-backgroud form-backgroud-img flex items-center justify-center py-10 min-h-screen bg-gradient-to-b from-blue-500 to-cyan-500 text-white">
            <div className="w-full max-w-md rounded-2xl border border-gray-300 p-8 backdrop-blur-3xl shadow-lg">
                {children}
            </div>
        </main>
    );
}
