import Table, { TableColumn, TableRowOptions } from "@/components/table";
import Image from "next/image";
import Link from "next/link";
import SmallProgressBar from "@/components/small_progressbar";
import * as React from "react";
import { ArrowDownIcon } from "@heroicons/react/24/solid";

export default function StockOverviewTable() {
  const options: TableRowOptions[] = [
    {
      title: "Archive",
      icon: <ArrowDownIcon className="h-4 w-4" />,
      href: "/archive",
    },
  ];
  const columns: TableColumn[] = [
    {
      title: "Item",
      className: "w-20",
      key: "image",
      orderable: false,
    },
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
      title: "Stock",
    },
    {
      title: "",
      className: "w-20",
    },
  ];

  const image = {
    height: 25,
    width: 25,
  };
  const data = [
    [
      <Image
        src={"/test_product_image_1.avif"}
        key={1}
        loading="lazy"
        height={image.height}
        width={image.width}
        alt={"test"}
      />,
      <Link
        href={"/test_product_image_1.avif"}
        key={1}
        className={"underline text-primary-dark"}
      >
        012348
      </Link>,
      "Blokje hout",
      "4x4 cm - 150cm",
      <SmallProgressBar value={50} max={100} key={1} />,
    ],
    [
      <Image
        src={"/test_product_image_2.avif"}
        key={1}
        loading="lazy"
        height={image.height}
        width={image.width}
        alt={"test"}
      />,
      <Link
        href={"/test_product_image_1.avif"}
        key={1}
        className={"underline text-primary-dark"}
      >
        012348
      </Link>,
      "Blokje hout",
      "4x4 cm - 150cm",
      <SmallProgressBar value={100} max={100} key={2} />,
    ],
  ];

  return <Table data={data} columns={columns} options={options} />;
}
