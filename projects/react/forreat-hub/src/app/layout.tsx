import { Inter } from "next/font/google";
import "./globals.css";
import * as React from "react";
import Sidebar from "@/components/sidebar";
import Header from "@/components/header";
import { AppProvider } from "@/context/AppContext";
import Head from "@/components/head";

const interSans = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <AppProvider>
        <Head />
        <body className={`${interSans.className}`}>
          <div className="flex h-screen bg-gray-50">
            <Sidebar />
            <div className="w-full mt-5 bg-white border-1 border-gray-200 rounded-tl-2xl shadow-xs h-screen">
              <Header />
              <div className={"px-10 mt-5"}>{children}</div>
            </div>
          </div>
        </body>
      </AppProvider>
    </html>
  );
}
