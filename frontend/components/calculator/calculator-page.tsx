import { useState } from "react";
import CalculatorDisplay from "./calculator-display";
import CalculatorKeypad from "./calculator-keypad";

export default function CalculatorPage() {
  const [angleMode, setAngleMode] = useState("Deg");
  const [numberBase, setNumberBase] = useState("Dec");
  const [currentValue, setCurrentValue] = useState("0");
  const [previousValue, setPreviousValue] = useState("Ans = 0");

  const handleKeyPress = (value: string) => {
    // TODO: 实现计算器按键处理逻辑
    console.log("Key pressed:", value);
  };

  return (
    <div className="max-w-md mx-auto bg-background rounded-xl shadow-lg overflow-hidden">
      <div className="p-4 pb-2">
        <div className="text-sm mb-1">Scientific Calculator</div>
        <CalculatorDisplay
          currentValue={currentValue}
          previousValue={previousValue}
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
