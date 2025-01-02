import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

interface CalculatorDisplayProps {
  currentValue: string[];
  previousValue: string;
  isLoading?: boolean;
  isError?: boolean;
  isAnswerState?: boolean;
}

export default function CalculatorDisplay({
  currentValue,
  previousValue,
  isLoading = false,
  isError = false,
  isAnswerState = false,
}: CalculatorDisplayProps) {
  // 将 tokens 映射到真正的 JSX
  const renderTokens = () => {
    return currentValue.map((tk, idx) => {
      if (tk === "|") {
        // 这里使用一个带有闪烁动画的光标
        return (
          <span
            key={`cursor-${idx}`}
            className="inline-block h-[1.5em] w-[3px] align-middle bg-current animate-blink mx-[1px]"
          />
        );
      } else {
        return <span key={`tk-${idx}`}>{tk}</span>;
      }
    });
  };

  return (
    <Card>
      <CardHeader className="pb-2">
        <div
          className={`text-right text-2xl font-mono h-8 mb-1 overflow-hidden whitespace-nowrap text-ellipsis ${
            isAnswerState ? "text-muted-foreground" : ""
          }`}
          aria-live="polite"
        >
          {isLoading ? (
            <Skeleton className="h-full w-24 ml-auto" />
          ) : (
            renderTokens()
          )}
        </div>
      </CardHeader>
      <CardContent className="pt-0 pb-4">
        <div
          className={`text-right text-sm font-mono h-5 overflow-hidden whitespace-nowrap text-ellipsis ${
            isError
              ? "text-red-500"
              : isAnswerState
              ? ""
              : "text-muted-foreground"
          }`}
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
