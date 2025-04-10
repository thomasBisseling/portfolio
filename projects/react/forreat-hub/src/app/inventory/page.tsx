"use client";

import * as React from "react";
import { useAppContext } from "@/context/AppContext";
import { useEffect } from "react";
import StockOverviewTable from "./_components/stockOverviewTable";
import Button from "@/components/button";

export default function Page() {
  const { setPageTitle } = useAppContext();

  useEffect(() => {
    setPageTitle("Voorraad overzicht");
  }, [setPageTitle]);

  const tableTitle = "Voorraad";

  return (
    <div className={"flex flex-1/2"}>
      <div className={"table__container"}>
        <div className={"flex justify-between"}>
          <h2 className={"table__header"}>{tableTitle}</h2>
          <Button
            title={"Voeg product toe"}
            onClick={() => {}}
            size={"small"}
            color={"primary"}
            className={"table__header__button"}
          />
        </div>
        <StockOverviewTable />
      </div>
    </div>
  );
}
