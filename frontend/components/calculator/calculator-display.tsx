import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

interface CalculatorDisplayProps {
  currentValue: string;
  previousValue: string;
  isLoading?: boolean;
}

export default function CalculatorDisplay({
  currentValue,
  previousValue,
  isLoading = false,
}: CalculatorDisplayProps) {
  return (
    <Card>
      <CardHeader className="pb-2">
        <div
          className="text-right text-2xl font-mono h-8 mb-1 overflow-hidden whitespace-nowrap text-ellipsis"
          aria-live="polite"
        >
          {isLoading ? (
            <Skeleton className="h-full w-24 ml-auto" />
          ) : (
            currentValue
          )}
        </div>
      </CardHeader>
      <CardContent className="pt-0 pb-4">
        <div
          className="text-right text-sm font-mono h-5 text-muted-foreground overflow-hidden whitespace-nowrap text-ellipsis"
          aria-live="polite"
        >
          {isLoading ? (
            <Skeleton className="h-full w-16 ml-auto" />
          ) : (
            previousValue
          )}
        </div>
      </CardContent>
    </Card>
  );
}
