<template>
  <el-menu
    mode="horizontal"
    :router="true"
    class="app-navbar"
  >
    <el-menu-item index="/">
      <template #title>
        <el-icon><HomeFilled /></el-icon>
        <span>Home</span>
      </template>
    </el-menu-item>

    <el-menu-item index="/customers">
      <template #title>
        <el-icon><User /></el-icon>
        <span>Customers</span>
      </template>
    </el-menu-item>

    <el-menu-item index="/contracts">
      <template #title>
        <el-icon><Document /></el-icon>
        <span>Contracts</span>
      </template>
    </el-menu-item>

    <el-menu-item index="/analytics">
      <template #title>
        <el-icon><TrendCharts /></el-icon>
        <span>Analytics</span>
      </template>
    </el-menu-item>

    <el-menu-item index="/feedbacks">
      <template #title>
        <el-icon><ChatDotRound /></el-icon>
        <span>Feedback</span>
      </template>
    </el-menu-item>

    <el-menu-item index="/payments">
      <template #title>
        <el-icon><Money /></el-icon>
        <span>Payments</span>
      </template>
    </el-menu-item>

    <el-menu-item index="/ai-analytics">
      <template #title>
        <el-icon><Monitor /></el-icon>
        <span>AI Analytics</span>
      </template>
    </el-menu-item>

    <div class="navbar-right">
      <el-dropdown trigger="click" @command="handleCommand">
        <span class="user-dropdown">
          <el-avatar :size="32">
            {{ userInitials }}
          </el-avatar>
          <span class="user-name">{{ userName }}</span>
          <el-icon class="el-icon--right">
            <CaretBottom />
          </el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">
              <el-icon><UserFilled /></el-icon>
              Profile
            </el-dropdown-item>
            <el-dropdown-item command="settings">
              <el-icon><Setting /></el-icon>
              Settings
            </el-dropdown-item>
            <el-dropdown-item divided command="logout">
              <el-icon><SwitchButton /></el-icon>
              Sign Out
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </el-menu>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import {
  HomeFilled,
  User,
  Document,
  TrendCharts,
  Monitor,
  CaretBottom,
  UserFilled,
  Setting,
  SwitchButton,
  Money,
  ChatDotRound
} from '@element-plus/icons-vue'

const router = useRouter()

const user = computed(() => {
  const userStr = localStorage.getItem('user')
  return userStr ? JSON.parse(userStr) : null
})

const userName = computed(() => {
  return user.value?.username || 'User'
})

const userInitials = computed(() => {
  return userName.value.charAt(0).toUpperCase()
})

const handleCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      // TODO: Implement profile page
      break
    case 'settings':
      // TODO: Implement settings page
      break
    case 'logout':
      try {
        await ElMessageBox.confirm(
          'Are you sure you want to sign out?',
          'Sign Out',
          {
            confirmButtonText: 'Sign Out',
            cancelButtonText: 'Cancel',
            type: 'warning'
          }
        )
        
        // Clear auth data
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        sessionStorage.removeItem('token')
        
        // Redirect to login
        router.push('/login')
      } catch {
        // User cancelled
      }
      break
  }
}
</script>

<style scoped>
.app-navbar {
  padding: 0 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  height: 100%;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.user-dropdown:hover {
  background-color: #f5f7fa;
}

.user-name {
  font-size: 14px;
  color: #606266;
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.el-dropdown-menu__item .el-icon) {
  margin: 0;
}

@media (max-width: 768px) {
  .app-navbar {
    padding: 0 16px;
  }
  
  .user-name {
    display: none;
  }
}
</style>
