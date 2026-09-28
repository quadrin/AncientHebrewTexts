import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "The Copper Scroll Atlas",
  description: "Explore the ancient places of the Copper Scroll and their candidate sites in two dimensions and three-dimensional terrain.",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
