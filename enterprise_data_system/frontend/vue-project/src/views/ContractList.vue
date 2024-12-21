<template>
  <el-container class="contract-container">
    <el-header>
      <el-row justify="space-between" align="middle">
        <el-col :span="12">
          <h2>Insurance Contracts</h2>
        </el-col>
        <el-col :span="12" style="text-align: right">
          <el-button type="primary" size="large" @click="$router.push('/contracts/new')">
            <el-icon><Plus /></el-icon>
            New Contract
          </el-button>
        </el-col>
      </el-row>
    </el-header>

    <el-main>
      <el-card class="table-card">
        <el-table 
          :data="contracts" 
          border 
          v-loading="loading"
          style="width: 100%"
        >
          <el-table-column prop="contract_num" label="Contract No." min-width="120" />
          <el-table-column prop="customer.name" label="Customer" min-width="120" />
          <el-table-column prop="business.name" label="Insurance Type" min-width="150" />
          <el-table-column prop="coverage" label="Coverage" min-width="120">
            <template #default="scope">
              ${{ scope.row.coverage?.toLocaleString() }}
            </template>
          </el-table-column>
          <el-table-column prop="duration" label="Duration" min-width="100">
            <template #default="scope">
              {{ scope.row.duration }} Years
            </template>
          </el-table-column>
          <el-table-column prop="status" label="Status" min-width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status_date" label="Status Date" min-width="120" />
          <el-table-column label="Actions" width="250" fixed="right">
            <template #default="scope">
              <div class="action-buttons">
                <el-button type="primary" size="small" @click="handleView(scope.row)">
                  View
                </el-button>
                <el-button type="warning" size="small" @click="handleRenew(scope.row)">
                  Renew
                </el-button>
                <el-button type="danger" size="small" @click="handleCancel(scope.row)">
                  Cancel
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <el-dialog 
        v-model="dialogVisible" 
        title="Contract Details" 
        width="600px"
        destroy-on-close
      >
        <div v-if="selectedContract" class="contract-details">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="Contract No.">
              {{ selectedContract.contract_num }}
            </el-descriptions-item>
            <el-descriptions-item label="Customer">
              {{ selectedContract.customer?.name }}
            </el-descriptions-item>
            <el-descriptions-item label="Insurance Type">
              {{ selectedContract.business?.name }}
            </el-descriptions-item>
            <el-descriptions-item label="Coverage">
              ${{ selectedContract.coverage?.toLocaleString() }}
            </el-descriptions-item>
            <el-descriptions-item label="Duration">
              {{ selectedContract.duration }} Years
            </el-descriptions-item>
            <el-descriptions-item label="Status">
              <el-tag :type="getStatusType(selectedContract.status)">
                {{ selectedContract.status }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </div>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="dialogVisible = false">Close</el-button>
            <el-button type="primary" @click="handleEdit(selectedContract)">
              Edit Contract
            </el-button>
          </div>
        </template>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

interface Contract {
  id: number
  contract_num: string
  customer: { name: string }
  business: { name: string }
  coverage: number
  duration: number
  status: string
  status_date: string
}

const router = useRouter()
const contracts = ref<Contract[]>([])
const dialogVisible = ref(false)
const selectedContract = ref<Contract | null>(null)
const loading = ref(false)

const fetchContracts = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/contracts/')
    contracts.value = Array.isArray(response.data.results) 
      ? response.data.results 
      : response.data.results 
        ? [response.data.results]
        : []
  } catch (error) {
    ElMessage.error('Failed to fetch contracts')
    console.error('Error:', error)
  } finally {
    loading.value = false
  }
}

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    active: 'success',
    pending: 'warning',
    cancelled: 'danger',
    expired: 'info'
  }
  return types[status?.toLowerCase()] || 'info'
}

const handleView = (contract: Contract) => {
  selectedContract.value = contract
  dialogVisible.value = true
}

const handleEdit = (contract: Contract | null) => {
  if (contract) {
    router.push(`/contracts/${contract.id}/edit`)
  }
}

const handleRenew = async (contract: Contract) => {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to renew this contract?',
      'Warning',
      {
        confirmButtonText: 'Renew',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )
    await api.post(`/api/contracts/${contract.id}/renew/`)
    ElMessage.success('Contract renewed successfully')
    await fetchContracts()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to renew contract')
      console.error('Error:', error)
    }
  }
}

const handleCancel = async (contract: Contract) => {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to cancel this contract?',
      'Warning',
      {
        confirmButtonText: 'Cancel Contract',
        cancelButtonText: 'Keep',
        type: 'warning'
      }
    )
    await api.post(`/api/contracts/${contract.id}/cancel/`)
    ElMessage.success('Contract cancelled successfully')
    await fetchContracts()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to cancel contract')
      console.error('Error:', error)
    }
  }
}

onMounted(() => {
  fetchContracts()
})
</script>

<style scoped>
.contract-container {
  padding: 24px;
  background-color: #f8f9fa;
}

.el-header {
  padding: 0;
  height: auto;
  margin-bottom: 24px;
  background-color: transparent;
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
}

.table-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.table-card :deep(.el-card__body) {
  padding: 0;
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: 600;
  height: 48px;
}

:deep(.el-table td) {
  padding: 12px 0;
}

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
}

:deep(.el-button--small) {
  padding: 8px 16px;
  font-size: 13px;
}

:deep(.el-tag) {
  text-transform: capitalize;
}

:deep(.el-loading-mask) {
  border-radius: 8px;
}

.contract-details {
  padding: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 20px;
}

:deep(.el-descriptions) {
  padding: 0;
}

:deep(.el-descriptions__cell) {
  padding: 12px 16px;
}
</style>
