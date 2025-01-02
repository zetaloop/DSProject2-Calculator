interface VariableDisplayProps {
  name: string;
  value: string;
  isAnswerState?: boolean;
}

export function VariableDisplay({
  name,
  value,
  isAnswerState = false,
}: VariableDisplayProps) {
  return (
    <span className="inline-flex items-center justify-center px-1.5 py-0.5 mx-0.5 border rounded-md bg-background relative group align-middle text-sm">
      <span className="absolute -top-2 left-1.5 px-0.5 text-[10px] leading-none text-muted-foreground bg-background">
        {name}
      </span>
      <span
        className={`mt-0.5 ${
          isAnswerState ? "text-muted-foreground" : "text-foreground"
        }`}
      >
        {value}
      </span>
    </span>
  );
}
