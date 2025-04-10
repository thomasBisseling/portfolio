"use client";

import { ForreatLogoIcon } from "@/components/icons";
import Link from "next/link";
import * as React from "react";
import {
  CubeIcon as CubeIconSolid,
  UserGroupIcon as UserGroupIconSolid,
  CreditCardIcon as CreditCardIconSolid,
  CogIcon as CogIconSolid,
  TruckIcon as TruckIconSolid,
  CalendarDateRangeIcon as CalendarDateRangeIconSolid,
  BuildingOffice2Icon as BuildingOffice2IconSolid,
  Square3Stack3DIcon as Square3Stack3DSolid,
  DocumentCurrencyEuroIcon as DocumentCurrencyEuroIconSolid,
} from "@heroicons/react/24/solid";
import {
  CubeIcon as CubeIconOutline,
  UserGroupIcon as UserGroupIconOutline,
  CreditCardIcon as CreditCardIconOutline,
  CogIcon as CogIconOutline,
  TruckIcon as TruckIconOutline,
  CalendarDateRangeIcon as CalendarDateRangeIconOutline,
  BuildingOffice2Icon as BuildingOffice2IconOutline,
  Square3Stack3DIcon as Square3Stack3DOutline,
  DocumentCurrencyEuroIcon as DocumentCurrencyEuroIconOutline,
} from "@heroicons/react/24/outline";
import { usePathname } from "next/navigation";

interface ChildMenuItem {
  title: string;
  href: string;
  active?: boolean;
}

interface MenuItem {
  title: string;
  icon: React.FC<{ className?: string; width: number; height: number }>;
  iconActive: React.FC<{ className?: string; width: number; height: number }>;
  href?: string;
  active?: boolean;
  children?: ChildMenuItem[];
}

interface MenuItemWithoutChildrenProps {
  title: string;
  icon: React.FC<{ className?: string; width: number; height: number }>;
  iconActive: React.FC<{ className?: string; width: number; height: number }>;
  href: string;
}

interface MenuItemWithChildrenProps {
  title: string;
  icon: React.FC<{ className?: string; width: number; height: number }>;
  iconActive: React.FC<{ className?: string; width: number; height: number }>;
  children: ChildMenuItem[];
}

function MenuItemWithChildren(props: {
  menuItem: MenuItemWithChildrenProps;
  pathname: string;
}) {
  const { menuItem, pathname } = props;

  menuItem.children = menuItem.children.map((child) => {
    return {
      ...child,
      active: child.href === pathname,
    };
  });
  const active = menuItem.children.some((child) => child.active);

  return (
    <>
      <div>
        <span
          className={`flex items-center py-2 px-4 rounded-lg text-xs font-semibold ${
            !menuItem.children && !active ? "hover:bg-gray-100" : ""
          } ${active ? "bg-primary/15 text-primary-dark" : "text-black"}`}
        >
          {active ? (
            <menuItem.iconActive
              width={20}
              height={20}
              className={"fill-primary-dark"}
            />
          ) : (
            <menuItem.icon width={20} height={20} />
          )}
          <span className="ml-3">{menuItem.title}</span>
        </span>
      </div>
      {menuItem.children && (
        <div className={"ml-8"}>
          {menuItem.children.map((child) => (
            <Link key={child.title} href={child.href}>
              <span
                className={`flex items-center py-2 my-1 rounded-lg text-xs text-black ${
                  child.active
                    ? "bg-gray-100 text-primary-dark"
                    : "hover:bg-gray-100"
                }`}
              >
                <span className="ml-3">{child.title}</span>
              </span>
            </Link>
          ))}
        </div>
      )}
    </>
  );
}

function MenuItemWithoutChildren(props: {
  menuItem: MenuItemWithoutChildrenProps;
  pathname: string;
}) {
  const { menuItem, pathname } = props;

  const active = menuItem.href === pathname;
  return (
    <Link href={menuItem.href}>
      <span
        className={`flex items-center py-2 px-4 rounded-lg text-xs  font-semibold ${
          !active ? "hover:bg-gray-100" : ""
        } ${active ? "bg-primary/15 text-primary-dark" : "text-black"}`}
      >
        {active ? (
          <menuItem.iconActive
            width={20}
            height={20}
            className={"fill-primary-dark"}
          />
        ) : (
          <menuItem.icon width={20} height={20} />
        )}
        <span className="ml-3">{menuItem.title}</span>
      </span>
    </Link>
  );
}

export default function Sidebar() {
  const menuItems: MenuItem[] = [
    {
      title: "Dashboard",
      icon: CubeIconOutline,
      iconActive: CubeIconSolid,
      href: "/dashboard",
    },
    // {
    //   title: "Agenda",
    //   icon: CalendarDateRangeIconOutline,
    //   iconActive: CalendarDateRangeIconSolid,
    //   href: "/agenda",
    // },
    {
      title: "Voorraad",
      icon: Square3Stack3DOutline,
      iconActive: Square3Stack3DSolid,
      children: [
        {
          title: "Overzicht",
          href: "/inventory",
        },
        {
          title: "Producten",
          href: "/inventory/products",
        },
        {
          title: "Categorieën",
          href: "/inventory/categories",
        },
        {
          title: "Locaties",
          href: "/inventory/locations",
        },
      ],
    },
    // {
    //   title: "Facturen",
    //   icon: DocumentCurrencyEuroIconOutline,
    //   iconActive: DocumentCurrencyEuroIconSolid,
    //   href: "/invoices",
    // },
    // {
    //   title: "Bestellingen",
    //   icon: TruckIconOutline,
    //   iconActive: TruckIconSolid,
    //   href: "/orders",
    // },
    // {
    //   title: "Uitgaven",
    //   icon: CreditCardIconOutline,
    //   iconActive: CreditCardIconSolid,
    //   href: "/expenses",
    // },
    // {
    //   title: "Klanten",
    //   icon: BuildingOffice2IconOutline,
    //   iconActive: BuildingOffice2IconSolid,
    //   href: "/customers",
    // },
    // {
    //   title: "KPI's",
    //   icon: CubeIconOutline,
    //   iconActive: CubeIconSolid,
    //   href: "/kpis",
    // },
    {
      title: "Gebruikers",
      icon: UserGroupIconOutline,
      iconActive: UserGroupIconSolid,
      href: "/users",
    },
    // {
    //   title: "Instellingen",
    //   icon: CogIconOutline,
    //   iconActive: CogIconSolid,
    //   href: "/settings",
    // },
  ];

  const pathname = usePathname();
  return (
    <div className="w-1/6">
      <div className={"mt-6"}>
        <div className="px-4 py-3 border-b-1 border-gray-200">
          <div className="mx-4 flex items-center">
            <ForreatLogoIcon size={21} />
            <span className={"ml-3 text-sm font-bold text-black"}>ForRaad</span>
          </div>
        </div>
        <div className={"mt-10 flex flex-col gap-2 mx-4"}>
          {menuItems.map((menuItem) => (
            <div key={menuItem.title}>
              {menuItem.children ? (
                <MenuItemWithChildren
                  menuItem={menuItem as MenuItemWithChildrenProps}
                  pathname={pathname}
                />
              ) : (
                <MenuItemWithoutChildren
                  menuItem={menuItem as MenuItemWithoutChildrenProps}
                  pathname={pathname}
                />
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
