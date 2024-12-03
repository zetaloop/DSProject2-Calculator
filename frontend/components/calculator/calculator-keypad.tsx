import React, { PropsWithChildren } from "react";
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
    { label: "History", variant: "link" },
    { label: "Settings", variant: "link" },
    {
      label: angleMode,
      variant: "link",
      dropdownOptions: angleModes,
      onSelect: onAngleModeChange,
    },
    {
      label: numberBase,
      variant: "link",
      dropdownOptions: numberBases,
      onSelect: onNumberBaseChange,
    },
    { label: "AC", variant: "link", className: "text-destructive" },
    { label: "Exit", variant: "link", className: "text-destructive" },

    // Row 2
    { label: "M+", variant: "ghost" },
    { label: "M-", variant: "ghost" },
    { label: "MR", variant: "ghost" },
    { label: "MC", variant: "ghost" },
    { label: "S⇔D", variant: "ghost" },
    { label: "SCI", variant: "ghost" },

    // Row 3
    {
      label: (
        <span>
          x<sup>2</sup>
        </span>
      ),
      variant: "ghost",
    },
    {
      label: (
        <span>
          x<sup>3</sup>
        </span>
      ),
      variant: "ghost",
    },
    {
      label: (
        <span>
          x<sup>y</sup>
        </span>
      ),
      variant: "ghost",
    },
    {
      label: (
        <span>
          x<sup>-1</sup>
        </span>
      ),
      variant: "ghost",
    },
    { label: "√", variant: "ghost" },
    { label: "∛", variant: "ghost" },

    // Row 4
    {
      label: (
        <span>
          10<sup>x</sup>
        </span>
      ),
      variant: "ghost",
    },
    {
      label: (
        <span>
          e<sup>x</sup>
        </span>
      ),
      variant: "ghost",
    },
    { label: "x!", variant: "ghost" },
    { label: "log", variant: "ghost" },
    { label: "ln", variant: "ghost" },
    { label: "|x|", variant: "ghost" },

    // Row 5
    { label: "sin", variant: "ghost" },
    { label: "cos", variant: "ghost" },
    { label: "tan", variant: "ghost" },
    {
      label: (
        <span>
          sin<sup>-1</sup>
        </span>
      ),
      variant: "ghost",
    },
    {
      label: (
        <span>
          cos<sup>-1</sup>
        </span>
      ),
      variant: "ghost",
    },
    {
      label: (
        <span>
          tan<sup>-1</sup>
        </span>
      ),
      variant: "ghost",
    },

    // Row 6
    { label: "(", variant: "ghost" },
    { label: ")", variant: "ghost" },
    { label: "π", variant: "ghost" },
    { label: "e", variant: "ghost" },
    { label: "i", variant: "ghost" },
    { label: "%", variant: "ghost" },

    // Row 7
    { label: "7", variant: "outline" },
    { label: "8", variant: "outline" },
    { label: "9", variant: "outline" },
    { label: "÷", variant: "outline" },
    { label: "nPr", variant: "ghost" },
    { label: "nCr", variant: "ghost" },

    // Row 8
    { label: "4", variant: "outline" },
    { label: "5", variant: "outline" },
    { label: "6", variant: "outline" },
    { label: "×", variant: "outline" },
    { label: "Mod", variant: "ghost" },
    { label: "Ran#", variant: "ghost" },

    // Row 9
    { label: "1", variant: "outline" },
    { label: "2", variant: "outline" },
    { label: "3", variant: "outline" },
    { label: "-", variant: "outline" },
    { label: "Ans", variant: "ghost" },
    { label: "DEL", variant: "ghost", className: "text-destructive" },

    // Row 10
    { label: "0", variant: "outline" },
    { label: ".", variant: "outline" },
    {
      label: (
        <span>
          ×10<sup>n</sup>
        </span>
      ),
      variant: "outline",
    },
    { label: "+", variant: "outline" },
    { label: "=", variant: "outline", className: "col-span-2" },
  ];

  const DropdownMenuTriggerWithChildren = DropdownMenuTrigger as React.FC<
    PropsWithChildren<{ asChild?: boolean }>
  >;

  const DropdownMenuRadioGroupWithChildren = DropdownMenuRadioGroup as React.FC<
    PropsWithChildren<{
      value: string;
      onValueChange: (value: string) => void;
    }>
  >;

  const DropdownMenuRadioItemWithChildren = DropdownMenuRadioItem as React.FC<
    PropsWithChildren<{
      value: string;
    }>
  >;

  const renderButton = (button: ButtonConfig, index: number) => {
    if (button.dropdownOptions) {
      return (
        <DropdownMenu key={index}>
          <DropdownMenuTriggerWithChildren asChild>
            <Button
              variant={button.variant}
              className={`font-semibold text-xs sm:text-sm ${
                button.className || ""
              }`}
            >
              {button.label}
            </Button>
          </DropdownMenuTriggerWithChildren>
          <DropdownMenuContent>
            <DropdownMenuRadioGroupWithChildren
              value={button.label.toString()}
              onValueChange={(value) => {
                button.onSelect && button.onSelect(value);
              }}
            >
              {button.dropdownOptions.map((option) => (
                <DropdownMenuRadioItemWithChildren key={option} value={option}>
                  {option}
                </DropdownMenuRadioItemWithChildren>
              ))}
            </DropdownMenuRadioGroupWithChildren>
          </DropdownMenuContent>
        </DropdownMenu>
      );
    }

    return (
      <Button
        key={index}
        variant={button.variant}
        className={`font-semibold text-xs sm:text-sm ${button.className || ""}`}
        onClick={() => onKeyPress(button.label.toString())}
      >
        {button.label}
      </Button>
    );
  };

  return (
    <div className="grid grid-cols-6 gap-1 p-2">
      {buttonConfig.map((button, index) => renderButton(button, index))}
    </div>
  );
}
