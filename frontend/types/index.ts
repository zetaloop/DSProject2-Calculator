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
  ans: number | null;
  previous_ans: number | null;
}

export interface CalculatorResponse {
  expression: string[];
  result: string;
  state: CalculatorState;
}
