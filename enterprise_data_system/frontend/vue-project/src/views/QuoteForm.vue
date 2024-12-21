<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { List, InfoFilled } from '@element-plus/icons-vue'
import api from '../api'
import type { Customer, QuoteForm, QuoteResult } from '../types'

const router = useRouter()
const formRef = ref<FormInstance>()

interface RiskData {
  diseaseRisk: number
  churnRisk: number
  sentiment: number
}

const customers = ref<Customer[]>([])
const quoteResult = ref<QuoteResult | null>(null)
const riskData = ref<RiskData | null>(null)
const loading = ref(false)
const calculating = ref(false)
const accepting = ref(false)

const form = reactive<QuoteForm>({
  customerId: '',
  insuranceType: '',
  coverage: 100000,
  duration: 1
})

const rules = reactive<FormRules>({
  customerId: [
    { required: true, message: 'Please select a customer', trigger: 'change' }
  ],
  insuranceType: [
    { required: true, message: 'Please select insurance type', trigger: 'change' }
  ],
  coverage: [
    { required: true, message: 'Please enter coverage amount', trigger: 'blur' },
    { type: 'number', min: 10000, message: 'Minimum coverage is $10,000', trigger: 'blur' }
  ],
  duration: [
    { required: true, message: 'Please enter duration', trigger: 'blur' },
    { type: 'number', min: 1, max: 30, message: 'Duration must be between 1-30 years', trigger: 'blur' }
  ]
})

const loadCustomers = async () => {
  try {
    const response = await api.get('/api/customers/')
    customers.value = response.data.results || []
  } catch (error) {
    ElMessage.error('Failed to load customers')
    console.error('Error:', error)
  }
}

const loadRiskData = async (customerId: number) => {
  loading.value = true
  try {
    const response = await api.get(`/api/customers/${customerId}/risk-analysis/`)
    riskData.value = response.data
  } catch (error) {
    ElMessage.error('Failed to load risk data')
    console.error('Error:', error)
  } finally {
    loading.value = false
  }
}

const handleSubmit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  
  await formEl.validate(async (valid) => {
    if (valid) {
      calculating.value = true
      try {
        const response = await api.post('/api/quotes/calculate/', {
          customer_id: form.customerId,
          insurance_type: form.insuranceType,
          coverage_amount: form.coverage,
          duration_years: form.duration,
          risk_data: riskData.value
        })
        quoteResult.value = response.data
      } catch (error) {
        ElMessage.error('Failed to calculate quote')
        console.error('Error:', error)
      } finally {
        calculating.value = false
      }
    }
  })
}

const handleReset = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
  riskData.value = null
  quoteResult.value = null
}

const handleRecalculate = () => {
  quoteResult.value = null
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handleAccept = async () => {
  accepting.value = true
  try {
    await api.post('/api/quotes/accept/', {
      customer_id: form.customerId,
      quote_result: quoteResult.value
    })
    ElMessage.success('Quote accepted successfully')
    router.push('/contracts')
  } catch (error) {
    ElMessage.error('Failed to accept quote')
    console.error('Error:', error)
  } finally {
    accepting.value = false
  }
}

const getRiskColor = (value: number) => {
  if (value <= 0.3) return '#67C23A'
  if (value <= 0.7) return '#E6A23C'
  return '#F56C6C'
}

const getSentimentColor = (value: number) => {
  if (value >= 0.7) return '#67C23A'
  if (value >= 0.3) return '#E6A23C'
  return '#F56C6C'
}

const getRiskLevel = (score: number) => {
  if (score <= 0.3) return 'success'
  if (score <= 0.7) return 'warning'
  return 'danger'
}

const getRiskText = (score: number) => {
  if (score <= 0.3) return 'Low Risk'
  if (score <= 0.7) return 'Medium Risk'
  return 'High Risk'
}

onMounted(() => {
  loadCustomers()
})
</script>

<template>
  <div class="quote-page">
    <div class="quote-container">
      <div class="content-wrapper">
        <el-card class="quote-form-card">
          <template #header>
            <h2>Insurance Quote</h2>
          </template>
          
          <el-form 
            ref="formRef"
            :model="form" 
            :rules="rules"
            label-width="160px"
            label-position="left"
            v-loading="loading"
            class="quote-form"
          >
            <el-form-item label="Customer" prop="customerId">
              <el-select 
                v-model="form.customerId" 
                placeholder="Select Customer" 
                @change="loadRiskData"
              >
                <el-option 
                  v-for="item in customers" 
                  :key="item.id" 
                  :label="item.name" 
                  :value="item.id" 
                >
                  <div class="customer-option">
                    <el-avatar :size="24">
                      {{ item.name?.charAt(0).toUpperCase() }}
                    </el-avatar>
                    <div class="customer-info">
                      <div class="customer-name">{{ item.name }}</div>
                      <div class="customer-email">{{ item.email }}</div>
                    </div>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="Insurance Type" prop="insuranceType">
              <el-select v-model="form.insuranceType">
                <el-option label="Life Insurance" value="life" />
                <el-option label="Health Insurance" value="health" />
                <el-option label="Property Insurance" value="property" />
              </el-select>
            </el-form-item>

            <el-form-item label="Coverage Amount" prop="coverage">
              <el-input-number 
                v-model="form.coverage" 
                :min="10000" 
                :max="10000000" 
                :step="10000"
              />
            </el-form-item>

            <el-form-item label="Duration (Years)" prop="duration">
              <el-input-number 
                v-model="form.duration" 
                :min="1" 
                :max="30" 
                :step="1"
              />
            </el-form-item>

            <el-form-item>
              <div class="form-buttons">
                <el-button 
                  type="primary" 
                  size="large"
                  :loading="calculating" 
                  @click="handleSubmit(formRef)"
                >
                  Calculate Quote
                </el-button>
                <el-button 
                  size="large"
                  @click="handleReset(formRef)"
                >
                  Reset
                </el-button>
              </div>
            </el-form-item>
          </el-form>
        </el-card>

        <div v-if="riskData" class="analysis-section">
          <el-row :gutter="24">
            <el-col :xs="24" :sm="24" :md="8">
              <el-card class="risk-card">
                <template #header>
                  <div class="card-header">
                    <span>Disease Risk</span>
                    <el-tooltip content="Predicted risk of chronic diseases">
                      <el-icon><InfoFilled /></el-icon>
                    </el-tooltip>
                  </div>
                </template>
                <div class="risk-score">
                  <el-progress 
                    type="dashboard" 
                    :percentage="Math.round(riskData.diseaseRisk * 100)"
                    :color="getRiskColor(riskData.diseaseRisk)"
                  />
                  <p>Risk Score: {{ (riskData.diseaseRisk * 100).toFixed(1) }}%</p>
                </div>
              </el-card>
            </el-col>
            
            <el-col :xs="24" :sm="24" :md="8">
              <el-card class="risk-card">
                <template #header>
                  <div class="card-header">
                    <span>Churn Risk</span>
                    <el-tooltip content="Likelihood of policy cancellation">
                      <el-icon><InfoFilled /></el-icon>
                    </el-tooltip>
                  </div>
                </template>
                <div class="risk-score">
                  <el-progress 
                    type="dashboard" 
                    :percentage="Math.round(riskData.churnRisk * 100)"
                    :color="getRiskColor(riskData.churnRisk)"
                  />
                  <p>Risk Score: {{ (riskData.churnRisk * 100).toFixed(1) }}%</p>
                </div>
              </el-card>
            </el-col>
            
            <el-col :xs="24" :sm="24" :md="8">
              <el-card class="risk-card">
                <template #header>
                  <div class="card-header">
                    <span>Customer Sentiment</span>
                    <el-tooltip content="Analysis of customer interactions">
                      <el-icon><InfoFilled /></el-icon>
                    </el-tooltip>
                  </div>
                </template>
                <div class="risk-score">
                  <el-progress 
                    type="dashboard" 
                    :percentage="Math.round(riskData.sentiment * 100)"
                    :color="getSentimentColor(riskData.sentiment)"
                  />
                  <p>Score: {{ (riskData.sentiment * 100).toFixed(1) }}%</p>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>

        <el-card v-if="quoteResult" class="quote-result">
          <template #header>
            <div class="card-header">
              <span>Quote Result</span>
              <el-tag :type="getRiskLevel(quoteResult.riskScore)">
                {{ getRiskText(quoteResult.riskScore) }}
              </el-tag>
            </div>
          </template>
          <div class="quote-details">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="Monthly Premium">
                ${{ quoteResult.monthlyPremium.toLocaleString() }}
              </el-descriptions-item>
              <el-descriptions-item label="Annual Premium">
                ${{ quoteResult.annualPremium.toLocaleString() }}
              </el-descriptions-item>
              <el-descriptions-item label="Total Premium">
                ${{ (quoteResult.annualPremium * form.duration).toLocaleString() }}
              </el-descriptions-item>
              <el-descriptions-item label="Risk Score">
                {{ (quoteResult.riskScore * 100).toFixed(1) }}%
              </el-descriptions-item>
            </el-descriptions>
            
            <div class="quote-actions">
              <el-button 
                type="success" 
                size="large"
                :loading="accepting"
                @click="handleAccept"
              >
                Accept Quote
              </el-button>
              <el-button 
                type="primary" 
                size="large"
                plain
                @click="handleRecalculate"
              >
                Recalculate
              </el-button>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<style>
.el-input-number {
  width: 100% !important;
}

.el-input-number .el-input__wrapper {
  width: 100% !important;
}

.el-select {
  width: 100% !important;
}

.el-select-dropdown__item {
  height: auto !important;
  padding: 8px 12px !important;
}
</style>

<style scoped>
.quote-page {
  width: 100%;
  min-height: 100vh;
  background-color: #f8f9fa;
  box-sizing: border-box;
}

.quote-container {
  width: 100%;
  box-sizing: border-box;
}

.content-wrapper {
  max-width: none;
  padding: 0 24px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

.quote-form-card {
  margin: 24px 0;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.quote-form-card :deep(.el-card__header) {
  padding: 20px 32px;
  border-bottom: 1px solid #e4e7ed;
}

.quote-form-card :deep(.el-card__header) h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
}

.quote-form {
  width: 100%;
}

.form-buttons {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.customer-option {
  display: flex;
  align-items: center;
  gap: 12px;
}

.customer-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.customer-name {
  font-weight: 500;
  color: #2c3e50;
}

.customer-email {
  font-size: 12px;
  color: #909399;
}

.analysis-section {
  margin: 24px 0;
}

.risk-card {
  margin-bottom: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-header .el-icon {
  font-size: 16px;
  color: #909399;
  cursor: help;
}

.risk-score {
  padding: 20px;
  text-align: center;
}

.risk-score p {
  margin: 16px 0 0;
  font-size: 16px;
  color: #606266;
}

.quote-result {
  margin: 24px 0;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.quote-details {
  padding: 20px;
}

.quote-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

:deep(.el-form-item) {
  margin-bottom: 24px;
}

:deep(.el-descriptions__cell) {
  padding: 16px 24px;
}

:deep(.el-descriptions__label) {
  font-weight: 500;
  color: #606266;
}

:deep(.el-descriptions__content) {
  font-size: 16px;
  color: #2c3e50;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 16px;
  }
  
  .quote-form-card :deep(.el-card__header) {
    padding: 16px;
  }
  
  .quote-form-card :deep(.el-card__body) {
    padding: 16px;
  }
  
  .form-buttons {
    flex-direction: column;
  }
  
  .quote-actions {
    flex-direction: column;
  }
  
  :deep(.el-descriptions__cell) {
    padding: 12px 16px;
  }
}
</style>
