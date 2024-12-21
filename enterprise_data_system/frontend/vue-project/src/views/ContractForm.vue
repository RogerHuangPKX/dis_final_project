<template>
  <div class="contract-form">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <h2>New Contract</h2>
        </div>
      </template>

      <el-form 
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        v-loading="loading"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Customer" prop="customer_id">
              <el-select 
                v-model="form.customer_id" 
                placeholder="Select customer" 
                class="w-100"
                filterable
              >
                <el-option
                  v-for="customer in customers"
                  :key="customer.id"
                  :label="`${customer.first_name} ${customer.last_name}`"
                  :value="customer.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Contract Number" prop="contract_num">
              <el-input v-model="form.contract_num" placeholder="Enter contract number" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Business Type" prop="business">
              <el-select v-model="form.business" placeholder="Select business type" class="w-100">
                <el-option label="Life Insurance" value="life" />
                <el-option label="Health Insurance" value="health" />
                <el-option label="Property Insurance" value="property" />
                <el-option label="Auto Insurance" value="auto" />
                <el-option label="Investment Products" value="investment" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Duration (Years)" prop="duration">
              <el-input-number 
                v-model="form.duration"
                :min="1"
                :max="30"
                class="w-100"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Coverage Amount" prop="coverage">
              <el-input-number 
                v-model="form.coverage"
                :min="0"
                :step="1000"
                class="w-100"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Premium" prop="premium">
              <el-input-number 
                v-model="form.premium"
                :min="0"
                :step="100"
                class="w-100"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Payment Method" prop="payment_method">
              <el-select v-model="form.payment_method" placeholder="Select payment method" class="w-100">
                <el-option label="Monthly" value="Monthly" />
                <el-option label="Quarterly" value="Quarterly" />
                <el-option label="Annually" value="Annually" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Auto Payment" prop="auto_payment">
              <el-switch
                v-model="form.auto_payment"
                active-text="Enable"
                inactive-text="Disable"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">Save</el-button>
          <el-button @click="$router.back()">Cancel</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import api from '../api'

const router = useRouter()
const formRef = ref<FormInstance>()

interface Customer {
  id: number
  first_name: string
  last_name: string
}

interface ContractForm {
  contract_num: string
  business: string
  coverage: number
  duration: number
  customer_id: number
  payment_method: string
  premium: number
  auto_payment: boolean
}

const customers = ref<Customer[]>([])
const loading = ref(false)

const form = reactive<ContractForm>({
  contract_num: '',
  business: '',
  coverage: 0,
  duration: 1,
  customer_id: 0,
  payment_method: '',
  premium: 0,
  auto_payment: false
})

const rules: FormRules = {
  customer_id: [
    { required: true, message: 'Please select a customer', trigger: 'change' }
  ],
  contract_num: [
    { required: true, message: 'Please enter contract number', trigger: 'blur' },
    { min: 3, max: 20, message: 'Length should be 3 to 20 characters', trigger: 'blur' }
  ],
  business: [
    { required: true, message: 'Please select business type', trigger: 'change' }
  ],
  coverage: [
    { required: true, message: 'Please enter coverage amount', trigger: 'blur' }
  ],
  duration: [
    { required: true, message: 'Please enter duration', trigger: 'blur' }
  ],
  payment_method: [
    { required: true, message: 'Please select payment method', trigger: 'change' }
  ],
  premium: [
    { required: true, message: 'Please enter premium amount', trigger: 'blur' }
  ]
}

const fetchCustomers = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/customers/')
    customers.value = response.data.results
  } catch (error) {
    console.error('Error fetching customers:', error)
    ElMessage.error('Failed to fetch customers')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    const contractData = {
      ...form,
      payment: {
        bill_method: form.payment_method,
        premium: form.premium,
        auto_loan: form.auto_payment ? 'Y' : 'N'
      }
    }
    
    const response = await api.post('/api/contracts/', contractData)
    ElMessage.success('Contract created successfully')
    router.push('/contracts')
  } catch (error: any) {
    if (error === false) {
      // Form validation failed
      return
    }
    ElMessage.error(error.response?.data?.message || 'Failed to create contract')
    console.error('Error:', error)
  }
}

onMounted(() => {
  fetchCustomers()
})
</script>

<style scoped>
.contract-form {
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
}

.form-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

.w-100 {
  width: 100%;
}

@media (max-width: 768px) {
  .contract-form {
    padding: 16px;
  }
}
</style>
