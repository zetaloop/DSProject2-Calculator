import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
} from "@/components/ui/dropdown-menu";

export default function ScientificCalculator() {
  // 状态管理
  const [angleMode, setAngleMode] = useState("Deg");
  const [numberBase, setNumberBase] = useState("Dec");

  const angleModes = ["Deg", "Rad", "Hyp"];
  const numberBases = ["Dec", "Bin", "Oct", "Hex"];

  const buttonConfig = [
    // Row 1
    { label: "History", variant: "link" },
    { label: "Settings", variant: "link" },
    {
      label: angleMode,
      variant: "link",
      dropdownOptions: angleModes,
      onSelect: setAngleMode,
    },
    {
      label: numberBase,
      variant: "link",
      dropdownOptions: numberBases,
      onSelect: setNumberBase,
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

  return (
    <div className="max-w-md mx-auto bg-background rounded-xl shadow-lg overflow-hidden">
      <div className="p-4 pb-2">
        <div className="text-sm mb-1">Scientific Calculator</div>
        <Card>
          <CardHeader className="pb-2">
            <div
              className="text-right text-2xl font-mono h-8 mb-1"
              aria-live="polite"
            >
              0
            </div>
          </CardHeader>
          <CardContent>
            <div
              className="text-right text-sm font-mono h-4 text-muted-foreground"
              aria-live="polite"
            >
              Ans = 0
            </div>
          </CardContent>
        </Card>
      </div>
      <div className="grid grid-cols-6 gap-1 p-2">
        {buttonConfig.map((button, index) =>
          button.dropdownOptions ? (
            <DropdownMenu key={index}>
              <DropdownMenuTrigger asChild>
                <Button
                  variant={button.variant}
                  className={`font-semibold text-xs sm:text-sm ${
                    button.className || ""
                  }`}
                >
                  {button.label}
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuRadioGroup
                  value={button.label}
                  onValueChange={(value) => button.onSelect(value)}
                >
                  {button.dropdownOptions.map((option) => (
                    <DropdownMenuRadioItem key={option} value={option}>
                      {option}
                    </DropdownMenuRadioItem>
                  ))}
                </DropdownMenuRadioGroup>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <Button
              key={index}
              variant={button.variant}
              className={`font-semibold text-xs sm:text-sm ${
                button.className || ""
              }`}
            >
              {button.label}
            </Button>
          )
        )}
      </div>
    </div>
  );
}
