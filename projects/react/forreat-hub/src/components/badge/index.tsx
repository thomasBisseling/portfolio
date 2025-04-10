"use client";

import "./badge.css";

interface BadgeProps {
  rounded?: boolean;
  color: "blue" | "yellow" | "red" | "green" | "indigo";
  text: string;
}

export default function Badge({ rounded = false, color, text }: BadgeProps) {
  const colorStyle = `badge-${color}`;
  const roundedStyle = rounded ? "badge-pill" : "";
  return <span className={`badge ${colorStyle} ${roundedStyle}`}>{text}</span>;
}
