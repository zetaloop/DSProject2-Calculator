export interface ContactType {
  id: string;
  name: string;
  email: string;
  phone?: string;
  picture?: string;
  birthDate?: string;
  intro?: string;
}

export interface CalculatorResponse {
  expression: string[];
  result: string;
  state: CalculatorState;
}

export interface CalculatorState {
  showing_answer: boolean;
  ans: number;
  _current_ans: number;
  _predicted_ans: number;
  use_scientific: boolean;
  use_fraction: boolean;
  memory: number;
  number_base: "Dec" | "Bin" | "Oct" | "Hex";
}

export interface CalculatorResponse {
  expression: string[];
  result: string;
  state: CalculatorState;
}
