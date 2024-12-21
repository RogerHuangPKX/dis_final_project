export interface Customer {
  id: number
  name: string
  email: string
  phone: string
  status: string
}

export interface QuoteForm {
  customerId: string | number
  insuranceType: string
  coverage: number
  duration: number
}

export interface QuoteResult {
  monthlyPremium: number
  annualPremium: number
  riskScore: number
}
