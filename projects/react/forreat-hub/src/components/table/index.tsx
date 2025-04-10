import * as React from "react";
import "./table.css";
import { useSearchParams, usePathname } from "next/navigation";
import { useCallback, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  ArrowUpIcon,
  ArrowDownIcon,
  ArrowsUpDownIcon,
} from "@heroicons/react/24/solid";
import Link from "next/link";
import { EllipsisVerticalIcon } from "@heroicons/react/24/solid";

export interface TableColumn {
  title: string;
  className?: string;
  key?: string;
  orderable?: boolean;
}

export interface TableRowOptions {
  title: string;
  key?: string;
  href: string;
  className?: string;
  icon?: React.JSX.Element;
}

type TableData = string | number | React.JSX.Element;

interface TableProps {
  options?: TableRowOptions[];
  columns: TableColumn[];
  data: TableData[][];
}

function TableCell({ value }: { value: TableData }) {
  return <td>{value}</td>;
}

function TableRowOptions({ options }: { options: TableRowOptions[] }) {
  return (
    <td className="">
      <EllipsisVerticalIcon className={"w-5 h-5"} />
    </td>
  );
}

function TableHeaderCell({
  value,
  className,
  orderable,
  param_key,
}: {
  value: string;
  className: string;
  orderable: boolean | undefined;
  param_key: string;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [order, setOrder] = React.useState(null as string | null);

  useEffect(() => {
    if (searchParams.has(param_key)) {
      const value = searchParams.get(param_key);
      setOrder(value);
    } else {
      setOrder(null);
    }
  }, [searchParams, param_key]);

  const createURL = useCallback(() => {
    const params = new URLSearchParams(searchParams.toString());
    let value: string | null = "asc";
    if (searchParams.has(param_key)) {
      value = searchParams.get(param_key) === "asc" ? "desc" : null;
    }

    if (!value) {
      params.delete(param_key);
    } else {
      params.set(param_key, value);
    }

    setOrder(value);

    return pathname + "?" + params.toString();
  }, [searchParams, param_key, pathname, setOrder]);

  return (
    <>
      {orderable ? (
        <th
          className={`${className} cursor-pointer select-none flex items-center gap-1`}
          onClick={() => {
            router.push(createURL());
          }}
        >
          {order == "asc" && (
            <ArrowDownIcon className="w-3 h-3 text-primary-dark" />
          )}

          {order == "desc" && (
            <ArrowUpIcon className="w-3 h-3 text-primary-dark" />
          )}

          {order == null && (
            <ArrowsUpDownIcon className="w-4 h-4 text-primary-dark" />
          )}
          {value}
        </th>
      ) : (
        <th className={className}>{value}</th>
      )}
    </>
  );
}
/**
 * Table component is a generic table component that can be used to display data in a table format.
 */
export default function Table(props: TableProps) {
  const { columns, data, options } = props;
  return (
    <div className={"table__inner"}>
      <table className="table">
        <thead className="bg-primary/10 text-primary-dark">
          <tr>
            {columns.map((column) => (
              <TableHeaderCell
                orderable={column.orderable}
                key={column.title.toLowerCase()}
                param_key={column.key || column.title.toLowerCase()}
                value={column.title}
                className={`${column.className || ""}`}
              />
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, cellIndex) => (
                <TableCell key={cellIndex} value={cell} />
              ))}
              {options && <TableRowOptions options={options} />}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
