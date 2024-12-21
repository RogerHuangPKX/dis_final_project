<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import api from '../api'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { User, Document, Money, DataLine, Bell, Calendar, Setting, TrendCharts } from '@element-plus/icons-vue'

interface DashboardData {
  total_customers: number
  active_contracts: number
  total_premium: number
  risk_distribution: {
    low: number
    medium: number
    high: number
  }
  recent_activities: Array<{
    id: number
    type: string
    description: string
    timestamp: string
  }>
  performance_metrics: {
    revenue_growth: number
    customer_satisfaction: number
    contract_renewal_rate: number
    response_time: number
  }
}

const dashboardData = ref<DashboardData>({
  total_customers: 0,
  active_contracts: 0,
  total_premium: 0,
  risk_distribution: {
    low: 0,
    medium: 0,
    high: 0
  },
  recent_activities: [],
  performance_metrics: {
    revenue_growth: 0,
    customer_satisfaction: 0,
    contract_renewal_rate: 0,
    response_time: 0
  }
})

const loading = ref(false)
const windowWidth = ref(window.innerWidth)
const navbarHeight = 70
const containerPadding = 32
const cardGap = 16

const quickActions = [
  { name: 'New Contract', icon: Document, route: '/contracts/new' },
  { name: 'Add Customer', icon: User, route: '/customers/new' },
  { name: 'Create Quote', icon: Money, route: '/quotes/new' },
  { name: 'Schedule Meeting', icon: Calendar, route: '/calendar' }
]

// Calculate card width
const cardWidth = computed(() => {
  const availableWidth = windowWidth.value - (containerPadding * 2) - (cardGap * 2)
  return Math.floor(availableWidth / 3)
})

const handleWindowResize = () => {
  windowWidth.value = window.innerWidth
  if (riskChart && performanceChart) {
    riskChart.resize()
    performanceChart.resize()
  }
}

const fetchDashboardData = async () => {
  loading.value = true
  try {
    const [customersRes, contractListRes] = await Promise.all([
      api.get('/api/customers/'),
      api.get('/api/contracts/')
    ])
    
    const totalPremium = contractListRes.data.results.reduce((sum: number, contract: any) => sum + contract.premium, 0);
    
    dashboardData.value = {
      total_customers: customersRes.data.count || 0,
      active_contracts: contractListRes.data.results.filter((c: any) => c.status === 'A').length,
      total_premium: totalPremium,
      risk_distribution: {
        low: 30,
        medium: 50,
        high: 20
      },
      recent_activities: contractListRes.data.results.map((contract: any, index: number) => ({
        id: index + 1,
        type: 'contract',
        description: `Contract ${contract.contract_num}: ${contract.customer} - $${contract.premium.toLocaleString()}`,
        timestamp: new Date().toISOString()
      })),
      performance_metrics: {
        revenue_growth: 15.8,
        customer_satisfaction: 92,
        contract_renewal_rate: 88,
        response_time: 2.5
      }
    }
    
    initCharts()
  } catch (error) {
    ElMessage.error('Failed to fetch dashboard data')
    console.error('Error:', error)
  } finally {
    loading.value = false
  }
}

let riskChart: echarts.ECharts | null = null
let performanceChart: echarts.ECharts | null = null

const initCharts = () => {
  if (riskChart) {
    riskChart.dispose()
  }
  if (performanceChart) {
    performanceChart.dispose()
  }

  // Risk Distribution Chart
  riskChart = echarts.init(document.getElementById('risk-chart'))
  riskChart.setOption({
    title: {
      text: 'Risk Distribution',
      left: 'center',
      top: 20,
      textStyle: {
        fontSize: 18,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'horizontal',
      bottom: 20,
      icon: 'circle'
    },
    series: [
      {
        name: 'Risk Distribution',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['50%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 6,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold'
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { 
            value: dashboardData.value.risk_distribution.low, 
            name: 'Low Risk',
            itemStyle: { color: '#67C23A' }
          },
          { 
            value: dashboardData.value.risk_distribution.medium, 
            name: 'Medium Risk',
            itemStyle: { color: '#E6A23C' }
          },
          { 
            value: dashboardData.value.risk_distribution.high, 
            name: 'High Risk',
            itemStyle: { color: '#F56C6C' }
          }
        ]
      }
    ]
  })

  // Performance Metrics Chart
  performanceChart = echarts.init(document.getElementById('performance-chart'))
  performanceChart.setOption({
    title: {
      text: 'Performance Metrics',
      left: 'center',
      top: 20
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      max: 100
    },
    yAxis: {
      type: 'category',
      data: ['Response Time', 'Renewal Rate', 'Satisfaction', 'Revenue Growth']
    },
    series: [
      {
        name: 'Value',
        type: 'bar',
        data: [
          {
            value: dashboardData.value.performance_metrics.response_time * 10,
            itemStyle: { color: '#409EFF' }
          },
          {
            value: dashboardData.value.performance_metrics.contract_renewal_rate,
            itemStyle: { color: '#67C23A' }
          },
          {
            value: dashboardData.value.performance_metrics.customer_satisfaction,
            itemStyle: { color: '#E6A23C' }
          },
          {
            value: dashboardData.value.performance_metrics.revenue_growth,
            itemStyle: { color: '#F56C6C' }
          }
        ],
        label: {
          show: true,
          position: 'right',
          formatter: (params: any) => {
            if (params.dataIndex === 0) {
              return params.value / 10 + ' hrs'
            }
            return params.value + '%'
          }
        }
      }
    ]
  })
}

onMounted(() => {
  fetchDashboardData()
  window.addEventListener('resize', handleWindowResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleWindowResize)
  if (riskChart) {
    riskChart.dispose()
    riskChart = null
  }
  if (performanceChart) {
    performanceChart.dispose()
    performanceChart = null
  }
})
</script>

<template>
  <div class="dashboard">
    <!-- Stats Section -->
    <div class="stats-container" :style="{ padding: `${containerPadding}px` }">
      <div 
        v-for="(item, index) in ['customers', 'contracts', 'premium']" 
        :key="item"
        class="stat-card"
        :style="{ 
          width: `${cardWidth}px`,
          marginLeft: index > 0 ? `${cardGap}px` : '0'
        }"
      >
        <div class="stat-content">
          <div class="stat-icon">
            <el-icon v-if="item === 'customers'"><User /></el-icon>
            <el-icon v-else-if="item === 'contracts'"><Document /></el-icon>
            <el-icon v-else><Money /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-label">
              {{ item === 'customers' ? 'Total Customers' : 
                 item === 'contracts' ? 'Active Contracts' : 'Total Premium' }}
            </div>
            <div class="stat-value">
              {{ item === 'customers' ? dashboardData.total_customers :
                 item === 'contracts' ? dashboardData.active_contracts :
                 '$' + dashboardData.total_premium?.toLocaleString() }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions Section -->
    <div class="quick-actions" :style="{ margin: `0 ${containerPadding}px` }">
      <h2 class="section-title">Quick Actions</h2>
      <div class="actions-grid">
        <el-button
          v-for="action in quickActions"
          :key="action.name"
          type="primary"
          class="action-button"
          @click="$router.push(action.route)"
        >
          <el-icon class="action-icon">
            <component :is="action.icon" />
          </el-icon>
          <span>{{ action.name }}</span>
        </el-button>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="charts-section" :style="{ margin: `${cardGap}px ${containerPadding}px` }">
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="chart-card">
            <div class="chart-header">
              <span class="chart-title">Risk Distribution</span>
              <el-icon><DataLine /></el-icon>
            </div>
            <div class="chart-content">
              <div id="risk-chart"></div>
            </div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="chart-card">
            <div class="chart-header">
              <span class="chart-title">Performance Metrics</span>
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="chart-content">
              <div id="performance-chart"></div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- Recent Activities Section -->
    <div class="activities-section" :style="{ margin: `0 ${containerPadding}px` }">
      <h2 class="section-title">Recent Activities</h2>
      <el-timeline>
        <el-timeline-item
          v-for="activity in dashboardData.recent_activities"
          :key="activity.id"
          :timestamp="activity.timestamp"
          :type="activity.type === 'contract' ? 'primary' : 
                activity.type === 'customer' ? 'success' : 'warning'"
        >
          {{ activity.description }}
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  width: 100%;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding-top: v-bind('navbarHeight + "px"');
  box-sizing: border-box;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
}

.stats-container {
  display: flex;
  box-sizing: border-box;
}

.stat-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.stat-content {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #409EFF;
}

.stat-icon .el-icon {
  font-size: 24px;
  color: white;
}

.stat-info {
  flex-grow: 1;
}

.stat-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  line-height: 1.2;
}

.quick-actions {
  margin-top: 24px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.action-button {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 16px;
}

.action-icon {
  font-size: 20px;
}

.chart-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.chart-header {
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.chart-header .el-icon {
  font-size: 20px;
  color: #409EFF;
}

.chart-content {
  padding: 20px;
  height: 400px;
}

#risk-chart,
#performance-chart {
  height: 100%;
  width: 100%;
}

.activities-section {
  margin-top: 24px;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .dashboard {
    padding-top: 60px;
  }

  .stats-container {
    flex-direction: column;
    padding: 16px !important;
  }

  .stat-card {
    width: 100% !important;
    margin: 0 0 16px 0 !important;
  }

  .stat-content {
    padding: 16px;
  }

  .stat-value {
    font-size: 20px;
  }

  .chart-content {
    height: 300px;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .action-button {
    height: 50px;
    font-size: 14px;
  }

  .section-title {
    font-size: 18px;
    margin-bottom: 16px;
  }
}
</style>
