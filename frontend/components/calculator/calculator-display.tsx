import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

interface CalculatorDisplayProps {
  currentValue: string;
  previousValue: string;
  isLoading?: boolean;
  isError?: boolean;
}

export default function CalculatorDisplay({
  currentValue,
  previousValue,
  isLoading = false,
  isError = false,
}: CalculatorDisplayProps) {
  // 将后端的 currentValue 拆分为 tokens
  const tokens = currentValue.split(" ");

  // 将 tokens 映射到真正的 JSX
  const renderTokens = () => {
    return tokens.map((tk, idx) => {
      if (tk === "|") {
        // 这里使用一个带有闪烁动画的光标
        return (
          <span
            key={`cursor-${idx}`}
            className="inline-block w-[1px] bg-current animate-blink mx-[1px]"
            style={{ height: "1em", verticalAlign: "middle" }}
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
          className="text-right text-2xl font-mono h-8 mb-1 overflow-hidden whitespace-nowrap text-ellipsis"
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
            isError ? "text-red-500" : "text-muted-foreground"
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
