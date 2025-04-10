import "./button.css";

interface ButtonProps {
  title: string;
  onClick: () => void;
  size: "small" | "medium" | "large";
  color: "red" | "green" | "primary" | "dark";
  submit?: boolean;
  className?: string;
  disabled?: boolean;
}

export default function Button({ ...props }: ButtonProps) {
  const { title, onClick, size, color, submit, className, disabled } = props;

  return (
    <a
      onClick={onClick}
      className={`btn btn--${size} btn--${color} ${className}`}
      {...(disabled ? { disabled: true } : {})}
    >
      {title}
    </a>
  );
}
