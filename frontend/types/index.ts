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
  state: {
    showing_answer: boolean;
    [key: string]: any;
  };
}
