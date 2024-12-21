<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../api'
import { ElMessage } from 'element-plus'

interface Payment {
  id: number
  contract_num: string
  customer: string
  premium: number
  bill_method: string
  auto_loan: string
  payment_limit: number
}

const payments = ref<Payment[]>([])
const loading = ref(false)

const fetchPayments = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/contracts/')
    payments.value = response.data.results.map((contract: any) => ({
      id: contract.id,
      contract_num: contract.contract_num,
      customer: contract.customer,
      premium: contract.premium,
      bill_method: 'Monthly',
      auto_loan: 'N',
      payment_limit: contract.premium * 12
    }))
  } catch (error) {
    ElMessage.error('Failed to fetch payments')
    console.error('Error:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchPayments()
})
</script>

<template>
  <div class="payment-view">
    <div class="header">
      <h1>Payment Management</h1>
      <el-button type="primary" @click="fetchPayments">
        <el-icon><Refresh /></el-icon>
        Refresh
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="payments"
      style="width: 100%"
      border
    >
      <el-table-column
        prop="contract_num"
        label="Contract Number"
        width="150"
      />
      <el-table-column
        prop="customer"
        label="Customer"
        min-width="200"
      />
      <el-table-column
        prop="premium"
        label="Premium"
        width="150"
      >
        <template #default="{ row }">
          ${{ row.premium.toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column
        prop="bill_method"
        label="Billing Method"
        width="150"
      />
      <el-table-column
        prop="auto_loan"
        label="Auto Loan"
        width="120"
      >
        <template #default="{ row }">
          <el-tag :type="row.auto_loan === 'Y' ? 'success' : 'info'">
            {{ row.auto_loan === 'Y' ? 'Yes' : 'No' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        prop="payment_limit"
        label="Payment Limit"
        width="150"
      >
        <template #default="{ row }">
          ${{ row.payment_limit.toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column
        label="Actions"
        width="200"
        fixed="right"
      >
        <template #default="{ row }">
          <el-button-group>
            <el-button type="primary" size="small">
              Pay
            </el-button>
            <el-button type="info" size="small">
              History
            </el-button>
            <el-button type="warning" size="small">
              Settings
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<style scoped>
.payment-view {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h1 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}
</style>
