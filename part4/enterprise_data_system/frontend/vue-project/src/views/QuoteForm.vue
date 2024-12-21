<template>
  <el-container>
    <el-header>
      <h2>Insurance Quote</h2>
    </el-header>

    <el-main>
      <el-form :model="form" label-width="120px">
        <el-form-item label="Customer">
          <el-select v-model="form.customerId" placeholder="Select Customer" @change="loadRiskData">
            <el-option v-for="item in customers" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>

        <el-form-item label="Insurance Type">
          <el-select v-model="form.insuranceType">
            <el-option label="Life Insurance" value="life" />
            <el-option label="Health Insurance" value="health" />
            <el-option label="Property Insurance" value="property" />
          </el-select>
        </el-form-item>

        <el-form-item label="Coverage Amount">
          <el-input-number v-model="form.coverage" :min="1000" :max="1000000" :step="1000" />
        </el-form-item>

        <el-form-item label="Duration (Years)">
          <el-input-number v-model="form.duration" :min="1" :max="30" :step="1" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">Calculate Quote</el-button>
          <el-button @click="handleReset">Reset</el-button>
        </el-form-item>
      </el-form>

      <el-row v-if="riskData" :gutter="20" class="risk-analysis">
        <el-col :span="8">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>Disease Risk</span>
              </div>
            </template>
            <div class="risk-score">
              <el-progress type="dashboard" :percentage="riskData.diseaseRisk * 100" />
              <p>Risk Score: {{ riskData.diseaseRisk }}</p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>Churn Risk</span>
              </div>
            </template>
            <div class="risk-score">
              <el-progress type="dashboard" :percentage="riskData.churnRisk * 100" />
              <p>Risk Score: {{ riskData.churnRisk }}</p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>Sentiment Analysis</span>
              </div>
            </template>
            <div class="risk-score">
              <el-progress type="dashboard" :percentage="riskData.sentiment * 100" status="success" />
              <p>Score: {{ riskData.sentiment }}</p>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-card v-if="quoteResult" class="quote-result">
        <template #header>
          <div class="card-header">
            <span>Quote Result</span>
          </div>
        </template>
        <div class="quote-details">
          <p>Monthly Premium: ${{ quoteResult.monthlyPremium }}</p>
          <p>Annual Premium: ${{ quoteResult.annualPremium }}</p>
          <p>Risk Score: {{ quoteResult.riskScore }}</p>
          <el-button type="success" @click="handleAccept">Accept Quote</el-button>
        </div>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { Customer, QuoteForm, QuoteResult } from '../types'

const router = useRouter()

interface RiskData {
  diseaseRisk: number
  churnRisk: number
  sentiment: number
}

const customers = ref<Customer[]>([])
const quoteResult = ref<QuoteResult | null>(null)
const riskData = ref<RiskData | null>(null)

const form = reactive<QuoteForm>({
  customerId: '',
  insuranceType: '',
  coverage: 100000,
  duration: 1
})

const loadRiskData = async (customerId: number) => {
  try {
    const response = await fetch(`/api/customer/${customerId}/risk-analysis`)
    riskData.value = await response.json()
  } catch (error) {
    console.error('Failed to load risk data:', error)
  }
}

const handleSubmit = async () => {
  try {
    const response = await fetch('/api/quote/calculate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        customer_id: form.customerId,
        insurance_type: form.insuranceType,
        coverage_amount: form.coverage,
        duration_years: form.duration,
        risk_data: riskData.value
      })
    })
    
    if (!response.ok) {
      throw new Error('Failed to calculate quote')
    }
    
    quoteResult.value = await response.json()
  } catch (error) {
    ElMessage.error('Failed to calculate quote')
    console.error('Quote calculation error:', error)
  }
}

const handleReset = () => {
  form.customerId = ''
  form.insuranceType = ''
  form.coverage = 100000
  form.duration = 1
  riskData.value = null
  quoteResult.value = null
}

const handleAccept = async () => {
  try {
    const response = await fetch('/api/quote/accept', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        customer_id: form.customerId,
        quote_result: quoteResult.value
      })
    })
    
    if (!response.ok) {
      throw new Error('Failed to accept quote')
    }
    
    ElMessage.success('Quote accepted successfully')
    router.push('/contracts')
  } catch (error) {
    ElMessage.error('Failed to accept quote')
    console.error('Quote acceptance error:', error)
  }
}
</script>

<style scoped>
.risk-analysis {
  margin: 20px 0;
}
.risk-score {
  text-align: center;
}
.quote-result {
  margin-top: 20px;
}
.quote-details {
  font-size: 16px;
}
</style>
