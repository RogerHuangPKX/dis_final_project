<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete, Money } from '@element-plus/icons-vue'

interface Customer {
  id: number
  name: string
  email: string
  phone: string
  status: string
  avatar?: string
}

const router = useRouter()
const customers = ref<Customer[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const fetchCustomers = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await api.get('/api/customers/')
    customers.value = response.data.results || []
  } catch (err: any) {
    const message = err.response?.data?.message || err.message || 'Failed to fetch customers'
    error.value = message
    ElMessage.error({
      message,
      duration: 5000,
      showClose: true
    })
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  router.push('/customers/new')
}

const handleEdit = (row: Customer) => {
  router.push(`/customers/${row.id}/edit`)
}

const handleQuote = (row: Customer) => {
  router.push(`/quotes/new?customer=${row.id}`)
}

const handleDelete = async (row: Customer) => {
  try {
    await ElMessageBox.confirm(
      `Are you sure you want to delete customer "${row.name}"?`,
      'Warning',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning',
        icon: Delete
      }
    )
    
    loading.value = true
    await api.delete(`/api/customers/${row.id}/`)
    
    ElMessage.success({
      message: `Customer "${row.name}" deleted successfully`,
      duration: 3000
    })
    
    await fetchCustomers()
  } catch (err: any) {
    if (err !== 'cancel') {
      const message = err.response?.data?.message || err.message || 'Failed to delete customer'
      ElMessage.error({
        message,
        duration: 5000,
        showClose: true
      })
      console.error('Error:', err)
    }
  } finally {
    loading.value = false
  }
}

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    active: 'success',
    pending: 'warning',
    inactive: 'info',
    suspended: 'danger'
  }
  return types[status?.toLowerCase()] || 'info'
}

onMounted(() => {
  fetchCustomers()
})
</script>

<template>
  <el-container class="customer-container">
    <el-header>
      <el-row justify="space-between" align="middle">
        <el-col :span="12">
          <h2>Customer Management</h2>
        </el-col>
        <el-col :span="12" style="text-align: right">
          <el-button type="primary" size="large" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            Add Customer
          </el-button>
        </el-col>
      </el-row>
    </el-header>

    <el-main>
      <el-card class="table-card" v-loading="loading" element-loading-text="Loading customers...">
        <template #header v-if="error">
          <el-alert
            :title="error"
            type="error"
            show-icon
            :closable="false"
            class="error-alert"
          />
        </template>

        <el-table 
          :data="customers" 
          border 
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="Name" min-width="150">
            <template #default="{ row }">
              <div class="name-cell">
                <el-avatar :size="32" :src="row.avatar">
                  {{ row.name?.charAt(0).toUpperCase() }}
                </el-avatar>
                <span>{{ row.name }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="email" label="Email" min-width="200" />
          <el-table-column prop="phone" label="Phone" min-width="150" />
          <el-table-column prop="status" label="Status" width="120">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" v-if="row.status">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="Actions" width="320" fixed="right">
            <template #default="scope">
              <div class="action-buttons">
                <el-tooltip content="Edit customer details" placement="top">
                  <el-button 
                    type="primary" 
                    size="small" 
                    @click="handleEdit(scope.row)"
                  >
                    <el-icon><Edit /></el-icon>
                    Edit
                  </el-button>
                </el-tooltip>
                <el-tooltip content="Create new quote" placement="top">
                  <el-button 
                    type="success" 
                    size="small" 
                    @click="handleQuote(scope.row)"
                  >
                    <el-icon><Money /></el-icon>
                    Quote
                  </el-button>
                </el-tooltip>
                <el-tooltip content="Delete customer" placement="top">
                  <el-button 
                    type="danger" 
                    size="small" 
                    @click="handleDelete(scope.row)"
                  >
                    <el-icon><Delete /></el-icon>
                    Delete
                  </el-button>
                </el-tooltip>
              </div>
            </template>
          </el-table-column>

          <template #empty>
            <div class="empty-state">
              <el-empty 
                :image-size="200"
                description="No customers found"
              >
                <template #description>
                  <div class="empty-description">
                    <p>No customers found</p>
                    <p class="empty-subtitle">Get started by adding your first customer</p>
                  </div>
                </template>
                <el-button type="primary" @click="handleAdd">
                  <el-icon><Plus /></el-icon>
                  Add Customer
                </el-button>
              </el-empty>
            </div>
          </template>
        </el-table>
      </el-card>
    </el-main>
  </el-container>
</template>

<style scoped>
.customer-container {
  padding: 24px;
  background-color: #f8f9fa;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
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
  width: 100%;
}

.table-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.table-card :deep(.el-card__body) {
  padding: 0;
}

.error-alert {
  margin: -1px -1px 0;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
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

.name-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: flex-start;
  flex-wrap: nowrap;
  min-width: 300px;
}

:deep(.el-button--small) {
  padding: 8px 16px;
  font-size: 13px;
  white-space: nowrap;
}

:deep(.el-button--small .el-icon) {
  margin-right: 4px;
}

:deep(.el-tag) {
  text-transform: capitalize;
}

:deep(.el-loading-mask) {
  border-radius: 8px;
}

.empty-state {
  padding: 40px 0;
}

.empty-description {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
}

.empty-description p {
  margin: 0;
  color: #606266;
}

.empty-subtitle {
  font-size: 14px;
  color: #909399 !important;
}

@media (max-width: 768px) {
  .customer-container {
    padding: 16px;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 4px;
    min-width: auto;
  }
  
  :deep(.el-button--small) {
    width: 100%;
  }
  
  .name-cell {
    gap: 8px;
  }
}
</style>
