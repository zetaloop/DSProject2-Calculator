import { Card, CardHeader, CardContent } from "@/components/ui/card";

interface CalculatorDisplayProps {
  currentValue: string;
  previousValue: string;
}

export default function CalculatorDisplay({
  currentValue,
  previousValue,
}: CalculatorDisplayProps) {
  return (
    <Card>
      <CardHeader className="pb-2">
        <div
          className="text-right text-2xl font-mono h-8 mb-1 overflow-hidden whitespace-nowrap text-ellipsis"
          aria-live="polite"
        >
          {currentValue}
        </div>
      </CardHeader>
      <CardContent>
        <div
          className="text-right text-sm font-mono h-4 text-muted-foreground overflow-hidden whitespace-nowrap text-ellipsis"
          aria-live="polite"
        >
          {previousValue}
        </div>
      </CardContent>
    </Card>
  );
}
