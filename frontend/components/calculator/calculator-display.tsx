import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { VariableDisplay } from "./variable-display";
import { CalculatorState } from "@/types";
import { useEffect, useRef } from "react";

interface CalculatorDisplayProps {
  currentValue: string[];
  previousValue: string;
  isLoading?: boolean;
  isError?: boolean;
  state: CalculatorState;
}

export default function CalculatorDisplay({
  currentValue,
  previousValue,
  isLoading = false,
  isError = false,
  state,
}: CalculatorDisplayProps) {
  const expressionRef = useRef<HTMLDivElement>(null);
  const cursorRef = useRef<HTMLSpanElement>(null);

  // 自动滚动到光标位置
  useEffect(() => {
    if (cursorRef.current && expressionRef.current) {
      const cursor = cursorRef.current;
      const container = expressionRef.current;
      const cursorRect = cursor.getBoundingClientRect();
      const containerRect = container.getBoundingClientRect();

      // 如果光标不在可视区域内，滚动到光标位置
      if (cursorRect.right > containerRect.right) {
        // 光标在右边界外
        container.scrollLeft =
          container.scrollLeft + (cursorRect.right - containerRect.right) + 20;
      } else if (cursorRect.left < containerRect.left) {
        // 光标在左边界外
        container.scrollLeft =
          container.scrollLeft - (containerRect.left - cursorRect.left) - 20;
      }
    }
  }, [currentValue]); // 当表达式改变时重新计算滚动位置

  // 将 tokens 映射到真正的 JSX
  const renderTokens = () => {
    return currentValue.map((tk, idx) => {
      if (tk === "|") {
        // 这里使用一个带有闪烁动画的光标
        return (
          <span
            key={`cursor-${idx}`}
            ref={cursorRef}
            className="inline-block h-[2em] w-[3px] align-middle bg-current animate-blink mx-[1px]"
          />
        );
      } else if (tk === "Ans" && state.ans !== null) {
        return (
          <VariableDisplay
            key={`tk-${idx}`}
            name="Ans"
            value={state.ans.toString()}
            isAnswerState={state.showing_answer}
          />
        );
      } else if (tk === "nPr") {
        return (
          <span key={`tk-${idx}`} className="font-black">
            P
          </span>
        );
      } else if (tk === "nCr") {
        return (
          <span key={`tk-${idx}`} className="font-black">
            C
          </span>
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
          ref={expressionRef}
          className={`text-right text-2xl font-mono min-h-[3rem] mb-1 overflow-x-auto overflow-y-visible whitespace-nowrap custom-scrollbar ${
            state.showing_answer ? "text-muted-foreground" : ""
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
      <CardContent className="pt-0 pb-4 relative">
        <div
          className={`text-right leading-5 font-mono min-h-[1.5rem] overflow-x-auto overflow-y-visible whitespace-nowrap custom-scrollbar transition-all ${
            isError
              ? "text-red-500 text-sm"
              : state.showing_answer
              ? "text-lg font-bold"
              : "text-sm text-muted-foreground"
          }`}
          aria-live="polite"
        >
          {isLoading ? (
            <Skeleton className="h-full w-16 ml-auto" />
          ) : (
            previousValue
          )}
        </div>
        {state.use_scientific && (
          <Badge
            variant="secondary"
            className="absolute bottom-1 left-1 text-[0.7rem] font-mono"
          >
            SCI
          </Badge>
        )}
      </CardContent>
    </Card>
  );
}
