<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="login-header">
          <h2>Enterprise Data System</h2>
          <p>Please sign in to continue</p>
        </div>
      </template>

      <el-form 
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        @keyup.enter="handleLogin"
      >
        <el-form-item label="Username" prop="username">
          <el-input 
            v-model="form.username"
            placeholder="Enter your username"
            prefix-icon="User"
            :maxlength="50"
          />
        </el-form-item>

        <el-form-item label="Password" prop="password">
          <el-input 
            v-model="form.password"
            type="password"
            placeholder="Enter your password"
            prefix-icon="Lock"
            show-password
            :maxlength="50"
          />
        </el-form-item>

        <div class="login-options">
          <el-checkbox v-model="form.remember">Remember me</el-checkbox>
          <el-link type="primary">Forgot password?</el-link>
        </div>

        <el-button 
          type="primary" 
          class="login-button"
          :loading="loading"
          @click="handleLogin"
        >
          Sign In
        </el-button>

        <div class="login-footer">
          <p>Don't have an account? <el-link type="primary">Contact administrator</el-link></p>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import api from '../api'

interface LoginForm {
  username: string
  password: string
  remember: boolean
}

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive<LoginForm>({
  username: '',
  password: '',
  remember: false
})

const rules: FormRules = {
  username: [
    { required: true, message: 'Please enter username', trigger: 'blur' },
    { min: 3, max: 50, message: 'Length should be 3 to 50 characters', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please enter password', trigger: 'blur' },
    { min: 6, max: 50, message: 'Length should be 6 to 50 characters', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    
    loading.value = true
    const response = await api.post('auth/login/', {
      username: form.username,
      password: form.password
    })

    // Store token in localStorage if remember me is checked
    if (form.remember) {
      localStorage.setItem('token', response.data.token)
    } else {
      sessionStorage.setItem('token', response.data.token)
    }

    // Store user info
    const userData = {
      username: response.data.username,
      is_staff: response.data.is_staff
    }
    localStorage.setItem('user', JSON.stringify(userData))

    ElMessage.success('Login successful')
    
    // 检查是否有重定向路径
    const redirect = router.currentRoute.value.query.redirect as string
    router.push(redirect || '/')
  } catch (err: any) {
    if (err === false) {
      // Form validation failed
      return
    }
    const message = err.response?.data?.error || err.message || 'Login failed'
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
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8f9fa;
  padding: 24px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
}

.login-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
}

.login-header p {
  margin: 8px 0 0;
  color: #606266;
  font-size: 14px;
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.login-button {
  width: 100%;
  padding: 12px;
  font-size: 16px;
}

.login-footer {
  margin-top: 24px;
  text-align: center;
}

.login-footer p {
  margin: 0;
  font-size: 14px;
  color: #606266;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  padding-bottom: 4px;
}

:deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #dcdfe6 inset;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #c0c4cc inset;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px var(--el-color-primary) inset !important;
}

@media (max-width: 768px) {
  .login-container {
    padding: 16px;
  }
}
</style>
