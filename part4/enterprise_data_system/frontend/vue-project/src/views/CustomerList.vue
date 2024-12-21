<template>
  <el-container>
    <el-header>
      <el-row justify="space-between" align="middle">
        <el-col :span="12">
          <h2>Customer Management</h2>
        </el-col>
        <el-col :span="12" style="text-align: right">
          <el-button type="primary" @click="handleAdd">Add Customer</el-button>
        </el-col>
      </el-row>
    </el-header>

    <el-main>
      <el-table :data="customers" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="Name" width="120" />
        <el-table-column prop="email" label="Email" />
        <el-table-column prop="phone" label="Phone" width="120" />
        <el-table-column prop="status" label="Status" width="100" />
        <el-table-column label="Actions" width="200">
          <template #default="scope">
            <el-button-group>
              <el-button type="primary" @click="handleEdit(scope.row)">Edit</el-button>
              <el-button type="success" @click="handleQuote(scope.row)">Quote</el-button>
              <el-button type="danger" @click="handleDelete(scope.row)">Delete</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const customers = ref([])

const fetchCustomers = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/customers/')
    customers.value = response.data
  } catch (error) {
    ElMessage.error('Failed to fetch customers')
  }
}

const handleAdd = () => {
  router.push('/customers/new')
}

const handleEdit = (row: any) => {
  router.push(`/customers/${row.id}/edit`)
}

const handleQuote = (row: any) => {
  router.push(`/quote?customer=${row.id}`)
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('Are you sure you want to delete this customer?')
    await axios.delete(`http://localhost:8000/api/customers/${row.id}/`)
    ElMessage.success('Customer deleted')
    await fetchCustomers()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to delete customer')
    }
  }
}

onMounted(() => {
  fetchCustomers()
})
</script>
