<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import api from '../api'

let riskChart: echarts.ECharts | null = null
let statusChart: echarts.ECharts | null = null
let durationChart: echarts.ECharts | null = null
let businessChart: echarts.ECharts | null = null
let growthChart: echarts.ECharts | null = null

const kpiData = ref({
  totalCustomers: 0,
  activeContracts: 0,
  averageValue: 0,
  retentionRate: 0
})

const fetchDashboardData = async () => {
  try {
    const response = await api.get('/api/analytics/dashboard/')
    const data = response.data
    
    kpiData.value = {
      totalCustomers: data.total_customers || 1000,
      activeContracts: data.active_contracts || 800,
      averageValue: data.average_contract_value || 5000,
      retentionRate: data.retention_rate || 95
    }

    if (riskChart && statusChart && durationChart && businessChart && growthChart) {
      // Risk Distribution Chart
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
              }
            },
            data: [
              { 
                value: data.risk_distribution?.low || 30, 
                name: 'Low Risk',
                itemStyle: { color: '#67C23A' }
              },
              { 
                value: data.risk_distribution?.medium || 50, 
                name: 'Medium Risk',
                itemStyle: { color: '#E6A23C' }
              },
              { 
                value: data.risk_distribution?.high || 20, 
                name: 'High Risk',
                itemStyle: { color: '#F56C6C' }
              }
            ]
          }
        ]
      })

      // Customer Status Distribution Chart
      statusChart.setOption({
        title: {
          text: 'Customer Status Distribution',
          left: 'center',
          top: 20
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
            name: 'Customer Status',
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
              }
            },
            data: [
              { 
                value: data.status_distribution?.active || 40,
                name: 'Active',
                itemStyle: { color: '#67C23A' }
              },
              { 
                value: data.status_distribution?.pending || 30,
                name: 'Pending',
                itemStyle: { color: '#E6A23C' }
              },
              { 
                value: data.status_distribution?.inactive || 20,
                name: 'Inactive',
                itemStyle: { color: '#909399' }
              },
              { 
                value: data.status_distribution?.suspended || 10,
                name: 'Suspended',
                itemStyle: { color: '#F56C6C' }
              }
            ]
          }
        ]
      })

      // Contract Duration Distribution Chart
      durationChart.setOption({
        title: {
          text: 'Contract Duration Distribution',
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
          type: 'category',
          data: ['1 Year', '2 Years', '3 Years', '5 Years', '10 Years'],
          axisTick: {
            alignWithLabel: true
          }
        },
        yAxis: {
          type: 'value',
          name: 'Number of Contracts'
        },
        series: [
          {
            name: 'Contracts',
            type: 'bar',
            barWidth: '60%',
            data: [
              {value: data.duration_distribution?.['1'] || 100, itemStyle: {color: '#409EFF'}},
              {value: data.duration_distribution?.['2'] || 80, itemStyle: {color: '#409EFF'}},
              {value: data.duration_distribution?.['3'] || 60, itemStyle: {color: '#409EFF'}},
              {value: data.duration_distribution?.['5'] || 40, itemStyle: {color: '#409EFF'}},
              {value: data.duration_distribution?.['10'] || 20, itemStyle: {color: '#409EFF'}}
            ]
          }
        ]
      })

      // Business Line Distribution Chart
      businessChart.setOption({
        title: {
          text: 'Business Line Distribution',
          left: 'center',
          top: 20
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          right: 10,
          top: 'center'
        },
        series: [
          {
            name: 'Business Lines',
            type: 'pie',
            radius: '50%',
            data: [
              { 
                value: data.business_distribution?.insurance || 35,
                name: 'Insurance',
                itemStyle: { color: '#409EFF' }
              },
              { 
                value: data.business_distribution?.investment || 25,
                name: 'Investment',
                itemStyle: { color: '#67C23A' }
              },
              { 
                value: data.business_distribution?.banking || 20,
                name: 'Banking',
                itemStyle: { color: '#E6A23C' }
              },
              { 
                value: data.business_distribution?.loan || 20,
                name: 'Loans',
                itemStyle: { color: '#F56C6C' }
              }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      })

      // Customer Growth Trend Chart
      growthChart.setOption({
        title: {
          text: 'Customer Growth Trend',
          left: 'center',
          top: 20
        },
        tooltip: {
          trigger: 'axis'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        yAxis: {
          type: 'value',
          name: 'Number of Customers'
        },
        series: [
          {
            name: 'Total Customers',
            type: 'line',
            smooth: true,
            data: data.growth_trend || [100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320],
            itemStyle: {
              color: '#409EFF'
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgba(64,158,255,0.3)'
                },
                {
                  offset: 1,
                  color: 'rgba(64,158,255,0.1)'
                }
              ])
            }
          }
        ]
      })
    }
  } catch (error) {
    ElMessage.error('Failed to fetch analytics data')
    console.error('Error:', error)
  }
}

onMounted(() => {
  riskChart = echarts.init(document.getElementById('risk-chart'))
  statusChart = echarts.init(document.getElementById('status-chart'))
  durationChart = echarts.init(document.getElementById('duration-chart'))
  businessChart = echarts.init(document.getElementById('business-chart'))
  growthChart = echarts.init(document.getElementById('growth-chart'))
  
  fetchDashboardData()
  
  const handleResize = () => {
    riskChart?.resize()
    statusChart?.resize()
    durationChart?.resize()
    businessChart?.resize()
    growthChart?.resize()
  }
  
  window.addEventListener('resize', handleResize)
  
  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    riskChart?.dispose()
    statusChart?.dispose()
    durationChart?.dispose()
    businessChart?.dispose()
    growthChart?.dispose()
  })
})
</script>

<template>
  <div class="analytics-page">
    <div class="analytics-container">
      <div class="kpi-section">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover" class="kpi-card">
              <template #header>
                <div class="kpi-header">
                  <span>Total Customers</span>
                </div>
              </template>
              <div class="kpi-value">{{ kpiData.totalCustomers }}</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover" class="kpi-card">
              <template #header>
                <div class="kpi-header">
                  <span>Active Contracts</span>
                </div>
              </template>
              <div class="kpi-value">{{ kpiData.activeContracts }}</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover" class="kpi-card">
              <template #header>
                <div class="kpi-header">
                  <span>Average Contract Value</span>
                </div>
              </template>
              <div class="kpi-value">${{ kpiData.averageValue }}</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover" class="kpi-card">
              <template #header>
                <div class="kpi-header">
                  <span>Retention Rate</span>
                </div>
              </template>
              <div class="kpi-value">{{ kpiData.retentionRate }}%</div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <div class="charts-section">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card class="chart-card">
              <div class="chart-content">
                <div id="risk-chart"></div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card class="chart-card">
              <div class="chart-content">
                <div id="status-chart"></div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card class="chart-card">
              <div class="chart-content">
                <div id="duration-chart"></div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card class="chart-card">
              <div class="chart-content">
                <div id="business-chart"></div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="24">
            <el-card class="chart-card">
              <div class="chart-content">
                <div id="growth-chart"></div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<style scoped>
.analytics-page {
  padding: 24px;
  background-color: #f8f9fa;
  min-height: 100vh;
}

.analytics-container {
  max-width: 1400px;
  margin: 0 auto;
}

.kpi-section {
  margin-bottom: 24px;
}

.kpi-card {
  height: 160px;
  text-align: center;
}

.kpi-header {
  font-size: 16px;
  color: #606266;
}

.kpi-value {
  font-size: 36px;
  font-weight: bold;
  color: #303133;
  margin-top: 20px;
}

.charts-section {
  .el-row {
    margin-bottom: 20px;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
}

.chart-card {
  margin-bottom: 20px;
  
  :deep(.el-card__body) {
    padding: 0;
  }
}

.chart-content {
  height: 400px;
  padding: 20px;
}

#risk-chart,
#status-chart,
#duration-chart,
#business-chart,
#growth-chart {
  width: 100%;
  height: 100%;
}

@media (max-width: 768px) {
  .analytics-page {
    padding: 16px;
  }
  
  .kpi-card {
    height: 120px;
    margin-bottom: 16px;
  }
  
  .kpi-value {
    font-size: 24px;
  }
  
  .chart-content {
    height: 300px;
  }
}
</style>
