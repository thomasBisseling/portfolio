"use client";

import { createContext, useState, ReactNode, useContext } from "react";

interface AppContextType {
  pageTitle: string;
  setPageTitle: (value: string) => void;
  totalCount: number | null;
  setTotalCount: (value: number | null) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [pageTitle, setPageTitle] = useState("");
  const [totalCount, setTotalCount] = useState<number | null>(null);

  return (
    <AppContext.Provider
      value={{ pageTitle, setPageTitle, totalCount, setTotalCount }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useAppContext must be used within an AppProvider");
  }
  return context;
}
