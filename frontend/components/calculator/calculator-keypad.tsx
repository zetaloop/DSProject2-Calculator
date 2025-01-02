import React from "react";
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
  const angleModes = ["Deg", "Rad", "Hyp"];
  const numberBases = ["Dec", "Bin", "Oct", "Hex"];

  const buttonConfig: ButtonConfig[] = [
    // Row 1
    { label: "History", value: "History", variant: "link" },
    { label: "Settings", value: "Settings", variant: "link" },
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
    { label: "AC", value: "AC", variant: "link", className: "text-destructive" },
    { label: "Exit", value: "Exit", variant: "link", className: "text-destructive" },

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
    { label: "x!", value: "x!", variant: "ghost" },
    { label: "log", value: "log", variant: "ghost" },
    { label: "ln", value: "ln", variant: "ghost" },
    { label: "|x|", value: "|x|", variant: "ghost" },

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
    { label: "(", value: "(", variant: "ghost" },
    { label: ")", value: ")", variant: "ghost" },
    { label: "π", value: "π", variant: "ghost" },
    { label: "e", value: "e", variant: "ghost" },
    { label: "i", value: "i", variant: "ghost" },
    { label: "%", value: "%", variant: "ghost" },

    // Row 7
    { label: "7", value: "7", variant: "outline" },
    { label: "8", value: "8", variant: "outline" },
    { label: "9", value: "9", variant: "outline" },
    { label: "÷", value: "/", variant: "outline" },
    { label: "nPr", value: "nPr", variant: "ghost" },
    { label: "nCr", value: "nCr", variant: "ghost" },

    // Row 8
    { label: "4", value: "4", variant: "outline" },
    { label: "5", value: "5", variant: "outline" },
    { label: "6", value: "6", variant: "outline" },
    { label: "×", value: "*", variant: "outline" },
    { label: "Mod", value: "Mod", variant: "ghost" },
    { label: "Ran#", value: "Ran#", variant: "ghost" },

    // Row 9
    { label: "1", value: "1", variant: "outline" },
    { label: "2", value: "2", variant: "outline" },
    { label: "3", value: "3", variant: "outline" },
    { label: "-", value: "-", variant: "outline" },
    { label: "Ans", value: "Ans", variant: "ghost" },
    { label: "DEL", value: "DEL", variant: "ghost", className: "text-destructive" },

    // Row 10
    { label: "0", value: "0", variant: "outline" },
    { label: ".", value: ".", variant: "outline" },
    {
      label: (
        <span>
          ×10<sup>n</sup>
        </span>
      ),
      value: "*10^n",
      variant: "outline",
    },
    { label: "+", value: "+", variant: "outline" },
    { label: "=", value: "=", variant: "outline", className: "col-span-2" },
  ];

  const renderButton = (button: ButtonConfig, index: number) => {
    if (button.dropdownOptions) {
      return (
        <DropdownMenu key={index}>
          <DropdownMenuTrigger asChild>
            <Button
              variant={button.variant}
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
        variant={button.variant}
        className={`font-semibold text-xs sm:text-sm h-full w-full ${button.className || ""}`}
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
