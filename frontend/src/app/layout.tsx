import type { Metadata } from "next";
import "./globals.css";
import { meta } from "@/lib/config";
import { Footer } from "@/components/Footer";
import { NextNavbar } from "@/components/Navbar";
import { ThemeProvider } from "@/providers/Theme";
import { AuthProvider } from "@/providers/Auth";

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
    <html lang="en" suppressHydrationWarning className="dark">
      <body
        className="antialiased"
      >
        <ThemeProvider>
          <AuthProvider >
            <NextNavbar>
              {children}
              <Footer />
            </NextNavbar>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}

