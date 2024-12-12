"use client";
import { useState, useEffect } from "react";
import { sendInput } from "@/api/calculator";
import CalculatorDisplay from "./calculator-display";
import CalculatorKeypad from "./calculator-keypad";

export default function CalculatorPage() {
  const [angleMode, setAngleMode] = useState("Deg");
  const [numberBase, setNumberBase] = useState("Dec");
  const [currentExpression, setCurrentExpression] = useState("0");
  const [currentResult, setCurrentResult] = useState("0");
  const [internalExpression, setInternalExpression] = useState<string[]>(["Ans"]);
  const [isLoading, setIsLoading] = useState(true);

  // 在组件加载时初始化显示值
  useEffect(() => {
    const initializeDisplay = async () => {
      try {
        const response = await sendInput("", internalExpression);
        setInternalExpression(response.expression);
        setCurrentExpression(response.display);
        setCurrentResult(response.result);
      } catch (error) {
        console.error("初始化显示错误:", error);
      } finally {
        setIsLoading(false);
      }
    };

    initializeDisplay();
  }, [internalExpression]);

  const handleKeyPress = async (value: string) => {
    try {
      const response = await sendInput(value, internalExpression);
      setInternalExpression(response.expression);
      setCurrentExpression(response.display);
      setCurrentResult(response.result);
    } catch (error) {
      console.error("按键处理错误:", error);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-background rounded-xl shadow-lg overflow-hidden">
      <div className="p-4 pb-2">
        <div className="text-sm mb-1">Scientific Calculator</div>
        <CalculatorDisplay
          currentValue={currentExpression}
          previousValue={`Ans = ${currentResult}`}
          isLoading={isLoading}
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
