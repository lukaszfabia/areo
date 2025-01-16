import type { Metadata } from "next";
import "./globals.css";
import { meta } from "@/lib/config";
import { Footer } from "@/components/Footer";
import { NextNavbar } from "@/components/Navbar";
import { ThemeProvider } from "@/providers/Theme";

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
        className="antialiased"
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

