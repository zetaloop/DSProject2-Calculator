import React, { useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
} from "@/components/ui/dropdown-menu";

interface CalculatorKeypadProps {
  angleMode: string;
  numberBase: string;
  onAngleModeChange: (value: string) => void;
  onNumberBaseChange: (value: string) => void;
  onKeyPress: (value: string) => void;
}

type ButtonVariant =
  | "link"
  | "ghost"
  | "outline"
  | "default"
  | "destructive"
  | "secondary";

interface ButtonConfig {
  label: string | JSX.Element;
  value: string;
  shortcut?: string;
  variant: ButtonVariant;
  className?: string;
  dropdownOptions?: string[];
  onSelect?: (value: string) => void;
}

export default function CalculatorKeypad({
  angleMode,
  numberBase,
  onAngleModeChange,
  onNumberBaseChange,
  onKeyPress,
}: CalculatorKeypadProps) {
  const buttonRefs = useRef<Record<string, HTMLButtonElement | null>>({});
  const angleModes = ["Deg", "Rad", "Hyp"];
  const numberBases = ["Dec", "Bin", "Oct", "Hex"];

  const buttonConfig: ButtonConfig[] = [
    // Row 1
    {
      label: angleMode,
      value: angleMode,
      variant: "link",
      dropdownOptions: angleModes,
      onSelect: onAngleModeChange,
    },
    {
      label: numberBase,
      value: numberBase,
      variant: "link",
      dropdownOptions: numberBases,
      onSelect: onNumberBaseChange,
    },
    { label: "←", value: "←", shortcut: "ArrowLeft", variant: "link" },
    { label: "→", value: "→", shortcut: "ArrowRight", variant: "link" },
    {
      label: "AC",
      value: "AC",
      shortcut: "Escape",
      variant: "link",
      className: "text-destructive",
    },
    {
      label: "Exit",
      value: "Exit",
      shortcut: "Ctrl+W",
      variant: "link",
      className: "text-destructive",
    },

    // Row 2
    { label: "M+", value: "M+", variant: "ghost" },
    { label: "M-", value: "M-", variant: "ghost" },
    { label: "MR", value: "MR", variant: "ghost" },
    { label: "MC", value: "MC", variant: "ghost" },
    { label: "S⇔D", value: "S⇔D", variant: "ghost" },
    { label: "SCI", value: "SCI", variant: "ghost" },

    // Row 3
    {
      label: (
        <span>
          x<sup>2</sup>
        </span>
      ),
      value: "x^2",
      variant: "ghost",
    },
    {
      label: (
        <span>
          x<sup>3</sup>
        </span>
      ),
      value: "x^3",
      variant: "ghost",
    },
    {
      label: (
        <span>
          x<sup>y</sup>
        </span>
      ),
      value: "x^y",
      shortcut: "^",
      variant: "ghost",
    },
    {
      label: (
        <span>
          x<sup>-1</sup>
        </span>
      ),
      value: "x^-1",
      variant: "ghost",
    },
    { label: "√", value: "sqrt", variant: "ghost" },
    { label: "∛", value: "cbrt", variant: "ghost" },

    // Row 4
    {
      label: (
        <span>
          10<sup>x</sup>
        </span>
      ),
      value: "10^x",
      variant: "ghost",
    },
    {
      label: (
        <span>
          e<sup>x</sup>
        </span>
      ),
      value: "e^x",
      variant: "ghost",
    },
    { label: "x!", value: "x!", shortcut: "!", variant: "ghost" },
    { label: "log", value: "log", variant: "ghost" },
    { label: "ln", value: "ln", variant: "ghost" },
    { label: "|x|", value: "|x|", shortcut: "|", variant: "ghost" },

    // Row 5
    { label: "sin", value: "sin", variant: "ghost" },
    { label: "cos", value: "cos", variant: "ghost" },
    { label: "tan", value: "tan", variant: "ghost" },
    {
      label: (
        <span>
          sin<sup>-1</sup>
        </span>
      ),
      value: "sin^-1",
      variant: "ghost",
    },
    {
      label: (
        <span>
          cos<sup>-1</sup>
        </span>
      ),
      value: "cos^-1",
      variant: "ghost",
    },
    {
      label: (
        <span>
          tan<sup>-1</sup>
        </span>
      ),
      value: "tan^-1",
      variant: "ghost",
    },

    // Row 6
    { label: "(", value: "(", shortcut: "(", variant: "ghost" },
    { label: ")", value: ")", shortcut: ")", variant: "ghost" },
    { label: "π", value: "π", variant: "ghost" },
    { label: "e", value: "e", shortcut: "e", variant: "ghost" },
    { label: "i", value: "i", shortcut: "i", variant: "ghost" },
    { label: "%", value: "%", shortcut: "%", variant: "ghost" },

    // Row 7
    { label: "7", value: "7", shortcut: "7", variant: "outline" },
    { label: "8", value: "8", shortcut: "8", variant: "outline" },
    { label: "9", value: "9", shortcut: "9", variant: "outline" },
    { label: "÷", value: "/", shortcut: "/", variant: "outline" },
    { label: "nPr", value: "nPr", variant: "ghost" },
    { label: "nCr", value: "nCr", variant: "ghost" },

    // Row 8
    { label: "4", value: "4", shortcut: "4", variant: "outline" },
    { label: "5", value: "5", shortcut: "5", variant: "outline" },
    { label: "6", value: "6", shortcut: "6", variant: "outline" },
    { label: "×", value: "*", shortcut: "*", variant: "outline" },
    { label: "Mod", value: "Mod", variant: "ghost" },
    { label: "Ran#", value: "Ran#", variant: "ghost" },

    // Row 9
    { label: "1", value: "1", shortcut: "1", variant: "outline" },
    { label: "2", value: "2", shortcut: "2", variant: "outline" },
    { label: "3", value: "3", shortcut: "3", variant: "outline" },
    { label: "-", value: "-", shortcut: "-", variant: "outline" },
    { label: "Ans", value: "Ans", variant: "ghost" },
    {
      label: "DEL",
      value: "DEL",
      shortcut: "Backspace",
      variant: "ghost",
      className: "text-destructive",
    },

    // Row 10
    { label: "0", value: "0", shortcut: "0,Numpad0", variant: "outline" },
    { label: ".", value: ".", shortcut: ".,NumpadDecimal", variant: "outline" },
    {
      label: (
        <span>
          ×10<sup>n</sup>
        </span>
      ),
      value: "*10^n",
      variant: "outline",
    },
    { label: "+", value: "+", shortcut: "+,NumpadAdd", variant: "outline" },
    {
      label: "=",
      value: "=",
      shortcut: "Enter,=,NumpadEnter",
      variant: "outline",
      className: "col-span-2",
    },
  ];

  // 监听键盘事件
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      // 构建当前按键组合
      const pressedKey = [];
      if (e.ctrlKey) pressedKey.push("Ctrl");
      if (e.altKey) pressedKey.push("Alt");

      // 对于需要 Shift 的特殊字符，我们不应该在组合键中包含 Shift
      const shiftRequiredChars = new Set([
        "+",
        "*",
        "^",
        "!",
        "|",
        "(",
        ")",
        "%",
        "?",
        ":",
        "{",
        "}",
        '"',
        "<",
        ">",
        "~",
      ]);

      // 只有在不是特殊字符时，才添加 Shift 到组合键中
      if (e.shiftKey && !shiftRequiredChars.has(e.key)) {
        pressedKey.push("Shift");
      }

      // 添加主键
      const mainKey = e.key === " " ? "Space" : e.key;
      pressedKey.push(mainKey);

      const currentKeyCombo = pressedKey.join("+");

      // 遍历所有按钮配置
      for (const button of buttonConfig) {
        if (!button.shortcut) continue;

        // 支持多个快捷键，用逗号分隔
        const shortcuts = button.shortcut.split(",").map((s) => s.trim());

        // 检查当前按键组合是否匹配任一快捷键
        if (
          shortcuts.some(
            (shortcut) =>
              shortcut.toLowerCase() === currentKeyCombo.toLowerCase()
          )
        ) {
          const btn = buttonRefs.current[button.shortcut];
          if (btn) {
            btn.click();
            break;
          }
        }
      }
    }

    window.addEventListener("keydown", handleKeyDown);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  });

  const renderButton = (button: ButtonConfig, index: number) => {
    if (button.dropdownOptions) {
      return (
        <DropdownMenu key={index}>
          <DropdownMenuTrigger asChild>
            <Button
              variant={button.variant}
              ref={(el) => {
                if (button.shortcut) {
                  buttonRefs.current[button.shortcut] = el;
                }
              }}
              className={`font-semibold text-xs sm:text-sm h-full w-full ${
                button.className || ""
              }`}
            >
              {button.label}
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuRadioGroup
              value={button.label.toString()}
              onValueChange={(value) => {
                if (button.onSelect) {
                  button.onSelect(value);
                }
                if (button.value !== value) {
                  onKeyPress(`${value}`);
                }
              }}
            >
              {button.dropdownOptions.map((option) => (
                <DropdownMenuRadioItem key={option} value={option}>
                  {option}
                </DropdownMenuRadioItem>
              ))}
            </DropdownMenuRadioGroup>
          </DropdownMenuContent>
        </DropdownMenu>
      );
    }

    return (
      <Button
        key={index}
        ref={(el) => {
          if (button.shortcut) {
            buttonRefs.current[button.shortcut] = el;
          }
        }}
        variant={button.variant}
        className={`font-semibold text-xs sm:text-sm h-full w-full ${
          button.className || ""
        }`}
        onClick={() => onKeyPress(button.value)}
      >
        {button.label}
      </Button>
    );
  };

  return (
    <div className="grid grid-cols-6 gap-1 p-2 flex-grow">
      {buttonConfig.map((button, index) => renderButton(button, index))}
    </div>
  );
}
