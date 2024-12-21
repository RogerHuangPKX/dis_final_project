<template>
  <el-container>
    <el-header>
      <h2>Insurance Contracts</h2>
    </el-header>

    <el-main>
      <el-table :data="contracts" border>
        <el-table-column prop="contract_num" label="Contract No." width="120" />
        <el-table-column prop="customer.name" label="Customer" width="120" />
        <el-table-column prop="business.name" label="Insurance Type" width="150" />
        <el-table-column prop="coverage" label="Coverage" width="120">
          <template #default="scope">
            ${{ scope.row.coverage }}
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="Duration" width="100">
          <template #default="scope">
            {{ scope.row.duration }} Years
          </template>
        </el-table-column>
        <el-table-column prop="status" label="Status" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status_date" label="Status Date" width="120" />
        <el-table-column label="Actions" width="200">
          <template #default="scope">
            <el-button-group>
              <el-button type="primary" @click="handleView(scope.row)">View</el-button>
              <el-button type="warning" @click="handleRenew(scope.row)">Renew</el-button>
              <el-button type="danger" @click="handleCancel(scope.row)">Cancel</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <el-dialog v-model="dialogVisible" title="Contract Details" width="50%">
        <div v-if="selectedContract">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="Contract No.">{{ selectedContract.contract_num }}</el-descriptions-item>
            <el-descriptions-item label="Customer">{{ selectedContract.customer?.name }}</el-descriptions-item>
            <el-descriptions-item label="Insurance Type">{{ selectedContract.business?.name }}</el-descriptions-item>
            <el-descriptions-item label="Coverage">${{ selectedContract.coverage }}</el-descriptions-item>
            <el-descriptions-item label="Duration">{{ selectedContract.duration }} Years</el-descriptions-item>
            <el-descriptions-item label="Status">{{ selectedContract.status }}</el-descriptions-item>
          </el-descriptions>
        </div>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'

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

const contracts = ref<Contract[]>([])
const dialogVisible = ref(false)
const selectedContract = ref<Contract | null>(null)

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    active: 'success',
    pending: 'warning',
    cancelled: 'danger',
    expired: 'info'
  }
  return types[status.toLowerCase()] || 'info'
}

const handleView = (contract: Contract) => {
  selectedContract.value = contract
  dialogVisible.value = true
}

const handleRenew = (contract: Contract) => {}
const handleCancel = (contract: Contract) => {}
</script>
