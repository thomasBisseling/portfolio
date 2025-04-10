interface SmallProgressBarProps {
  max: number;
  showValues?: boolean;
  label?: string;
  value: number;
}

export default function SmallProgressBar({ ...props }: SmallProgressBarProps) {
  const { max, showValues = true, label, value } = props;

  const percentage = Math.round((value / max) * 100);

  return (
    <div className="flex items-center">
      <div className="relative w-full h-2 bg-gray-200 rounded">
        <div
          className="absolute top-0 left-0 h-2 bg-blue-600 rounded"
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
      {showValues && (
        <span className="ml-2 text-xs text-gray-700">
          {value}/{max}
        </span>
      )}
    </div>
  );
}
