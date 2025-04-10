"use client";
import { useAppContext } from "@/context/AppContext";
import Head from "next/head";

import * as React from "react";

export default function CustomHead() {
  const { pageTitle } = useAppContext();
  return (
    <Head>
      <title>{pageTitle}</title>
    </Head>
  );
}
