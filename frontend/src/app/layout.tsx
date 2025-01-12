import type { Metadata } from "next";
import "./globals.css";
import { meta } from "@/lib/config";
import { ThemeProvider } from "@/providers/Theme";
import { Footer } from "@/components/Footer";
import { NextNavbar } from "@/components/Navbar";

export const metadata: Metadata = {
  title: meta.title,
  description: meta.desc,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className="antialiased bg-slate-50 dark:bg-slate-950"
      >
        <ThemeProvider>
          <NextNavbar >
            {/* <AuthProvider > */}
            {children}
            <Footer />
            {/* </AuthProvider> */}
          </NextNavbar>
        </ThemeProvider>
      </body>
    </html>
  );
}

