<template>
  <div class="app">
    <AppNavbar v-if="showNavbar" />
    <router-view />
    <footer class="footer">
      <p>Created by Jinze Huang (jh9108) - {{ currentDate }}</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppNavbar from './components/AppNavbar.vue'

const route = useRoute()
const showNavbar = computed(() => route.name !== 'login')
const currentDate = new Date().toLocaleDateString('en-US', {
  year: 'numeric',
  month: 'long',
  day: 'numeric'
})
</script>

<style>
.app {
  min-height: 100vh;
  background-color: #f8f9fa;
}

:root {
  --el-color-primary: #409eff;
  --el-color-success: #67c23a;
  --el-color-warning: #e6a23c;
  --el-color-danger: #f56c6c;
  --el-color-info: #909399;
  
  --el-border-radius-base: 4px;
  --el-font-size-base: 14px;
}

html {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji',
    'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  margin: 0;
  padding: 0;
}

#app {
  width: 100%;
  height: 100%;
}

/* Element Plus Overrides */
.el-button {
  font-weight: 500;
}

.el-button--primary {
  --el-button-hover-bg-color: #66b1ff;
  --el-button-hover-border-color: #66b1ff;
}

.el-button--success {
  --el-button-hover-bg-color: #85ce61;
  --el-button-hover-border-color: #85ce61;
}

.el-button--warning {
  --el-button-hover-bg-color: #ebb563;
  --el-button-hover-border-color: #ebb563;
}

.el-button--danger {
  --el-button-hover-bg-color: #f78989;
  --el-button-hover-border-color: #f78989;
}

.el-form-item__label {
  font-weight: 500;
}

.el-card {
  --el-card-border-color: #e4e7ed;
  --el-card-border-radius: 8px;
}

.el-menu {
  --el-menu-hover-bg-color: #f5f7fa;
  --el-menu-active-color: var(--el-color-primary);
}

.el-table {
  --el-table-border-color: #e4e7ed;
  --el-table-header-bg-color: #f5f7fa;
  --el-table-row-hover-bg-color: #f5f7fa;
}

.el-pagination {
  --el-pagination-button-bg-color: #fff;
  --el-pagination-hover-color: var(--el-color-primary);
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(10px);
  opacity: 0;
}

.footer {
  text-align: center;
  padding: 20px;
  color: #606266;
  font-size: 14px;
  border-top: 1px solid #e4e7ed;
  margin-top: 40px;
  background-color: white;
}

.footer p {
  margin: 0;
}
</style>
