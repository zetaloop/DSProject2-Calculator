import { CalculatorResponse } from "@/types";

const API_BASE_URL = "";

export const sendInput = async (
  key: string,
  expression: string[]
): Promise<CalculatorResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/input`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      key,
      expression,
    }),
  });

  if (!response.ok) {
    throw new Error("计算失败");
  }

  return response.json();
};
