<template>
  <el-container class="customer-form-container">
    <el-header>
      <el-row justify="space-between" align="middle">
        <el-col :span="12">
          <h2>{{ isEdit ? 'Edit Customer' : 'Add Customer' }}</h2>
        </el-col>
        <el-col :span="12" style="text-align: right">
          <el-button @click="$router.back()">
            <el-icon><ArrowLeft /></el-icon>
            Back
          </el-button>
        </el-col>
      </el-row>
    </el-header>

    <el-main>
      <el-card class="form-card" v-loading="loading">
        <el-form 
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="120px"
          label-position="left"
        >
          <!-- Basic Information -->
          <h3>Basic Information</h3>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="First Name" prop="first_name">
                <el-input 
                  v-model="form.first_name"
                  placeholder="Enter first name"
                  :maxlength="100"
                  show-word-limit
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="Last Name" prop="last_name">
                <el-input 
                  v-model="form.last_name"
                  placeholder="Enter last name"
                  :maxlength="100"
                  show-word-limit
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="Middle Initial" prop="middle_init">
                <el-input 
                  v-model="form.middle_init"
                  placeholder="MI"
                  :maxlength="1"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="Suffix" prop="suffix">
                <el-select v-model="form.suffix" placeholder="Select suffix" clearable>
                  <el-option label="Jr." value="Jr." />
                  <el-option label="Sr." value="Sr." />
                  <el-option label="II" value="II" />
                  <el-option label="III" value="III" />
                  <el-option label="IV" value="IV" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="Salutation" prop="salutation">
                <el-select v-model="form.salutation" placeholder="Select salutation" clearable>
                  <el-option label="Mr." value="Mr." />
                  <el-option label="Mrs." value="Mrs." />
                  <el-option label="Ms." value="Ms." />
                  <el-option label="Dr." value="Dr." />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="Gender" prop="gender">
                <el-select v-model="form.gender" placeholder="Select gender">
                  <el-option label="Male" value="M" />
                  <el-option label="Female" value="F" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="Language" prop="language">
                <el-select v-model="form.language" placeholder="Select language">
                  <el-option label="English" value="EN" />
                  <el-option label="Spanish" value="ES" />
                  <el-option label="French" value="FR" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="Status" prop="status">
                <el-select v-model="form.status" placeholder="Select status">
                  <el-option label="Active" value="A" />
                  <el-option label="Pending" value="P" />
                  <el-option label="Inactive" value="I" />
                  <el-option label="Suspended" value="S" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <!-- Contact Information -->
          <h3>Contact Information</h3>
          <el-form-item label="Email" prop="identity.email">
            <el-input 
              v-model="form.identity.email"
              placeholder="Enter email address"
              type="email"
            />
          </el-form-item>

          <el-form-item label="Phone" prop="identity.phone">
            <el-input 
              v-model="form.identity.phone"
              placeholder="Enter phone number"
              :maxlength="50"
            />
          </el-form-item>

          <!-- Identity Information -->
          <h3>Identity Information</h3>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="Date of Birth" prop="identity.dob">
                <el-date-picker
                  v-model="form.identity.dob"
                  type="date"
                  placeholder="Select date"
                  style="width: 100%"
                  :disabled-date="disableFutureDates"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="SSN" prop="identity.ssn">
                <el-input 
                  v-model="form.identity.ssn"
                  placeholder="Enter SSN"
                  :maxlength="11"
                  show-password
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="SSN Type" prop="identity.ssn_type">
                <el-select v-model="form.identity.ssn_type" placeholder="Select SSN type">
                  <el-option label="Social Security" value="S" />
                  <el-option label="Tax ID" value="T" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="Withholding" prop="identity.withholding">
                <el-select v-model="form.identity.withholding" placeholder="Select withholding">
                  <el-option label="Yes" value="Y" />
                  <el-option label="No" value="N" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item>
            <div class="form-buttons">
              <el-button 
                type="primary" 
                :loading="saving"
                size="large"
                @click="handleSubmit"
              >
                {{ isEdit ? 'Update Customer' : 'Create Customer' }}
              </el-button>
              <el-button 
                @click="handleReset"
                size="large"
                :disabled="saving"
              >
                Reset
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import api from '../api'

interface CustomerIdentity {
  email: string
  phone: string
  dob: string
  ssn: string
  ssn_type: string
  withholding: string
}

interface CustomerForm {
  first_name: string
  last_name: string
  middle_init: string
  suffix: string
  salutation: string
  gender: string
  language: string
  status: string
  identity: CustomerIdentity
}

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()

const isEdit = computed(() => route.params.id !== undefined)
const customerId = computed(() => route.params.id)

const loading = ref(false)
const saving = ref(false)

const form = reactive<CustomerForm>({
  first_name: '',
  last_name: '',
  middle_init: '',
  suffix: '',
  salutation: '',
  gender: '',
  language: 'EN',
  status: 'A',
  identity: {
    email: '',
    phone: '',
    dob: '',
    ssn: '',
    ssn_type: 'S',
    withholding: 'Y'
  }
})

const validatePhone = (rule: any, value: string, callback: Function) => {
  const phoneRegex = /^[\d\s-()]+$/
  if (!value) {
    callback(new Error('Please enter phone number'))
  } else if (!phoneRegex.test(value)) {
    callback(new Error('Please enter valid phone number'))
  } else {
    callback()
  }
}

const validateSSN = (rule: any, value: string, callback: Function) => {
  const ssnRegex = /^\d{3}-?\d{2}-?\d{4}$/
  if (!value) {
    callback(new Error('Please enter SSN'))
  } else if (!ssnRegex.test(value)) {
    callback(new Error('Please enter valid SSN (XXX-XX-XXXX)'))
  } else {
    callback()
  }
}

const rules: FormRules = {
  first_name: [
    { required: true, message: 'Please enter first name', trigger: 'blur' },
    { min: 2, max: 100, message: 'Length should be 2 to 100 characters', trigger: 'blur' }
  ],
  last_name: [
    { required: true, message: 'Please enter last name', trigger: 'blur' },
    { min: 2, max: 100, message: 'Length should be 2 to 100 characters', trigger: 'blur' }
  ],
  middle_init: [
    { max: 1, message: 'Maximum 1 character', trigger: 'blur' }
  ],
  gender: [
    { required: true, message: 'Please select gender', trigger: 'change' }
  ],
  language: [
    { required: true, message: 'Please select language', trigger: 'change' }
  ],
  status: [
    { required: true, message: 'Please select status', trigger: 'change' }
  ],
  'identity.email': [
    { required: true, message: 'Please enter email address', trigger: 'blur' },
    { type: 'email', message: 'Please enter valid email address', trigger: 'blur' }
  ],
  'identity.phone': [
    { required: true, validator: validatePhone, trigger: 'blur' }
  ],
  'identity.dob': [
    { required: true, message: 'Please select date of birth', trigger: 'change' }
  ],
  'identity.ssn': [
    { required: true, validator: validateSSN, trigger: 'blur' }
  ],
  'identity.ssn_type': [
    { required: true, message: 'Please select SSN type', trigger: 'change' }
  ],
  'identity.withholding': [
    { required: true, message: 'Please select withholding', trigger: 'change' }
  ]
}

const disableFutureDates = (date: Date) => {
  return date > new Date()
}

const fetchCustomer = async () => {
  if (!isEdit.value) return
  
  loading.value = true
  try {
    const response = await api.get(`/api/customers/${customerId.value}/`)
    const { identity, ...customerData } = response.data
    Object.assign(form, customerData)
    if (identity) {
      Object.assign(form.identity, identity)
    }
  } catch (err: any) {
    const message = err.response?.data?.message || err.message || 'Failed to fetch customer'
    ElMessage.error({
      message,
      duration: 5000,
      showClose: true
    })
    router.push('/customers')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    saving.value = true
    const data = {
      ...form,
      identity: {
        ...form.identity,
        dob: form.identity.dob ? new Date(form.identity.dob).toISOString().split('T')[0] : null
      }
    }

    if (isEdit.value) {
      await api.put(`/api/customers/${customerId.value}/`, data)
      ElMessage.success('Customer updated successfully')
    } else {
      await api.post('/api/customers/', data)
      ElMessage.success('Customer created successfully')
    }
    router.push('/customers')
  } catch (err: any) {
    if (err === false) {
      // Form validation failed
      return
    }
    const message = err.response?.data?.message || err.message || 
      (isEdit.value ? 'Failed to update customer' : 'Failed to create customer')
    ElMessage.error({
      message,
      duration: 5000,
      showClose: true
    })
    console.error('Error:', err)
  } finally {
    saving.value = false
  }
}

const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

onMounted(() => {
  fetchCustomer()
})
</script>

<style scoped>
.customer-form-container {
  padding: 24px;
  background-color: #f8f9fa;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.el-header {
  padding: 0;
  height: auto;
  margin-bottom: 24px;
  background-color: transparent;
  width: 100%;
  max-width: 800px;
}

.el-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
}

.el-main {
  padding: 0;
  background-color: transparent;
  width: 100%;
  display: flex;
  justify-content: center;
}

.form-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px;
}

.form-card h3 {
  margin: 24px 0 16px;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.form-card h3:first-child {
  margin-top: 0;
}

.form-buttons {
  display: flex;
  gap: 12px;
  justify-content: flex-start;
  margin-top: 32px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

@media (max-width: 768px) {
  .customer-form-container {
    padding: 16px;
  }
  
  .form-buttons {
    flex-direction: column;
  }
  
  .form-buttons .el-button {
    width: 100%;
  }

  .el-row {
    margin-left: 0 !important;
    margin-right: 0 !important;
  }

  .el-col {
    padding-left: 0 !important;
    padding-right: 0 !important;
  }
}
</style>
