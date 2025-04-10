"use client";

import { useAppContext } from "@/context/AppContext";
import * as React from "react";

export default function Header() {
  const { pageTitle, totalCount } = useAppContext();

  return (
    <header className="py-3 border-b-1 border-gray-200">
      <div className="text-black text-md font-semibold px-10">
        {pageTitle}
        {totalCount !== null && (
          <span className="text-sm text-gray-500 ml-1">
            ({totalCount > 99 ? "99+" : totalCount})
          </span>
        )}
      </div>
    </header>
  );
}
