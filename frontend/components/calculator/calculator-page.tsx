"use client";
import { useState, useEffect } from "react";
import { sendInput } from "@/api/calculator";
import CalculatorDisplay from "./calculator-display";
import CalculatorKeypad from "./calculator-keypad";

export default function CalculatorPage() {
  const [angleMode, setAngleMode] = useState("Deg");
  const [numberBase, setNumberBase] = useState("Dec");
  const [currentResult, setCurrentResult] = useState("0");
  const [isError, setIsError] = useState(false);
  const [internalExpression, setInternalExpression] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const processResult = (result: string) => {
    if (result.startsWith("Error: ")) {
      setIsError(true);
      return result.substring(7); // 移除 "Error: " 前缀
    }
    setIsError(false);
    return result;
  };

  // 使用空依赖数组，并在内部使用初始状态
  useEffect(() => {
    const initializeDisplay = async () => {
      try {
        const response = await sendInput("AC", []);
        setInternalExpression(response.expression);
        setCurrentResult(processResult(response.result));
      } catch (error) {
        console.error("初始化显示错误:", error);
      } finally {
        setIsLoading(false);
      }
    };

    initializeDisplay();
  }, []); // 保持空依赖数组

  const handleKeyPress = async (value: string) => {
    try {
      const response = await sendInput(value, internalExpression);
      setInternalExpression(response.expression);
      setCurrentResult(processResult(response.result));
    } catch (error) {
      console.error("按键处理错误:", error);
    }
  };

  return (
    <div className="h-screen bg-background overflow-hidden flex flex-col">
      <div className="p-4 pb-2 flex-shrink-0">
        <CalculatorDisplay
          currentValue={internalExpression}
          previousValue={currentResult}
          isLoading={isLoading}
          isError={isError}
        />
      </div>
      <CalculatorKeypad
        angleMode={angleMode}
        numberBase={numberBase}
        onAngleModeChange={setAngleMode}
        onNumberBaseChange={setNumberBase}
        onKeyPress={handleKeyPress}
      />
    </div>
  );
}
