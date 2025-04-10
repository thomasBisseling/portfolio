"use client";

import * as React from "react";
import Table, { TableColumn } from "@/components/table";
import { useAppContext } from "@/context/AppContext";
import { useEffect } from "react";
import Badge from "@/components/badge";

export default function Page() {
  const { setPageTitle } = useAppContext();

  useEffect(() => {
    setPageTitle("Dashboard");
  }, [setPageTitle]);

  const columns: TableColumn[] = [
    {
      title: "Article number",
      key: "article_number",
      orderable: true,
    },
    {
      title: "Name",
    },
    {
      title: "Specification",
    },
    {
      title: "In stock",
    },
    {
      title: "",
      className: "w-20",
    },
  ];

  const data = [
    [
      "012348",
      "Blokje hout",
      "4x4 cm - 150cm",
      1000,
      <Badge text={"volume low"} color={"blue"} key={1} />,
    ],
    [
      "012348",
      "Blokje hout",
      "4x4 cm - 150cm",
      1000,
      <Badge text={"volume low"} color={"red"} key={2} />,
    ],
    [
      "012348",
      "Blokje hout",
      "4x4 cm - 150cm",
      1000,
      <Badge text={"volume low"} color={"green"} key={3} />,
    ],
  ];

  return (
    <div className={"flex flex-1/2"}>
      <Table data={data} columns={columns} title={"Stock"} />
    </div>
  );
}
