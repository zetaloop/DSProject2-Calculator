interface VariableDisplayProps {
  name: string;
  value: string;
}

export function VariableDisplay({ name, value }: VariableDisplayProps) {
  return (
    <span className="inline-flex items-center justify-center px-2 py-1 mx-0.5 border rounded-md bg-background relative group">
      <span className="absolute -top-2 left-2 px-1 text-xs text-muted-foreground bg-background">
        {name}
      </span>
      <span className="text-foreground">{value}</span>
    </span>
  );
}
