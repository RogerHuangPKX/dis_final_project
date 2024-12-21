<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import api from '../api'

let feedbackChart: echarts.ECharts | null = null
let callChart: echarts.ECharts | null = null
let riskChart: echarts.ECharts | null = null
let churnChart: echarts.ECharts | null = null

const aiMetrics = ref({
  totalFeedbacks: 0,
  averageSentiment: 0,
  totalCalls: 0,
  averageRiskScore: 0
})

const fetchAIAnalytics = async () => {
  try {
    console.log('Fetching AI analytics data...')
    const response = await api.get('/api/analytics/ai/')
    console.log('AI analytics response:', response.data)
    const data = response.data
    
    aiMetrics.value = {
      totalFeedbacks: data.feedback_analytics.total_feedbacks,
      averageSentiment: data.feedback_analytics.average_sentiment,
      totalCalls: data.call_analytics.total_calls,
      averageRiskScore: data.risk_analytics.average_risk_score
    }

    if (feedbackChart && callChart && riskChart && churnChart) {
      // Feedback Sentiment Trend Chart
      feedbackChart.setOption({
        title: {
          text: 'Customer Feedback Sentiment Trend',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: data.feedback_analytics.sentiment_trend.map((item: any) => item.date)
        },
        yAxis: {
          type: 'value',
          name: 'Sentiment Score'
        },
        series: [{
          name: 'Sentiment Score',
          type: 'line',
          smooth: true,
          data: data.feedback_analytics.sentiment_trend.map((item: any) => item.score),
          itemStyle: {
            color: '#409EFF'
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(64,158,255,0.3)' },
              { offset: 1, color: 'rgba(64,158,255,0.1)' }
            ])
          }
        }]
      })

      // Call Analytics Chart
      callChart.setOption({
        title: {
          text: 'Call Sentiment Distribution',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        series: [{
          name: 'Call Sentiment',
          type: 'pie',
          radius: '50%',
          data: [
            { value: data.call_analytics.total_calls, name: 'Total Calls' }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }]
      })

      // Disease Risk Distribution Chart
      riskChart.setOption({
        title: {
          text: 'Disease Risk Distribution',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [{
          name: 'Risk Level',
          type: 'pie',
          radius: '50%',
          data: [
            { 
              value: data.risk_analytics.risk_distribution.high,
              name: 'High Risk',
              itemStyle: { color: '#F56C6C' }
            },
            {
              value: data.risk_analytics.risk_distribution.medium,
              name: 'Medium Risk',
              itemStyle: { color: '#E6A23C' }
            },
            {
              value: data.risk_analytics.risk_distribution.low,
              name: 'Low Risk',
              itemStyle: { color: '#67C23A' }
            }
          ]
        }]
      })

      // Churn Prediction Chart
      churnChart.setOption({
        title: {
          text: 'Churn Risk Distribution',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [{
          name: 'Churn Risk',
          type: 'pie',
          radius: '50%',
          data: [
            {
              value: data.churn_analytics.churn_distribution.high,
              name: 'High Risk',
              itemStyle: { color: '#F56C6C' }
            },
            {
              value: data.churn_analytics.churn_distribution.medium,
              name: 'Medium Risk',
              itemStyle: { color: '#E6A23C' }
            },
            {
              value: data.churn_analytics.churn_distribution.low,
              name: 'Low Risk',
              itemStyle: { color: '#67C23A' }
            }
          ]
        }]
      })
    }
  } catch (error: any) {
    console.error('Error fetching AI analytics:', error)
    ElMessage.error(error.response?.data?.error || 'Failed to fetch AI analytics data')
  }
}

const handleResize = () => {
  feedbackChart?.resize()
  callChart?.resize()
  riskChart?.resize()
  churnChart?.resize()
}

onMounted(() => {
  try {
    console.log('Initializing charts...')
    feedbackChart = echarts.init(document.getElementById('feedback-chart'))
    callChart = echarts.init(document.getElementById('call-chart'))
    riskChart = echarts.init(document.getElementById('risk-chart'))
    churnChart = echarts.init(document.getElementById('churn-chart'))
    
    window.addEventListener('resize', handleResize)
    fetchAIAnalytics()
  } catch (error) {
    console.error('Error initializing charts:', error)
    ElMessage.error('Failed to initialize charts')
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  try {
    feedbackChart?.dispose()
    callChart?.dispose()
    riskChart?.dispose()
    churnChart?.dispose()
  } catch (error) {
    console.error('Error disposing charts:', error)
  }
})
</script>

<template>
  <div class="ai-analytics-page">
    <div class="ai-analytics-container">
      <div class="metrics-section">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover" class="metric-card">
              <template #header>
                <div class="metric-header">
                  <span>Total Feedbacks</span>
                </div>
              </template>
              <div class="metric-value">{{ aiMetrics.totalFeedbacks }}</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover" class="metric-card">
              <template #header>
                <div class="metric-header">
                  <span>Average Sentiment</span>
                </div>
              </template>
              <div class="metric-value">{{ aiMetrics.averageSentiment }}</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover" class="metric-card">
              <template #header>
                <div class="metric-header">
                  <span>Total Calls</span>
                </div>
              </template>
              <div class="metric-value">{{ aiMetrics.totalCalls }}</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover" class="metric-card">
              <template #header>
                <div class="metric-header">
                  <span>Average Risk Score</span>
                </div>
              </template>
              <div class="metric-value">{{ aiMetrics.averageRiskScore }}</div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <div class="charts-section">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card class="chart-card">
              <div class="chart-content">
                <div id="feedback-chart"></div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card class="chart-card">
              <div class="chart-content">
                <div id="call-chart"></div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
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
                <div id="churn-chart"></div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ai-analytics-page {
  padding: 24px;
  background-color: #f8f9fa;
  min-height: 100vh;
}

.ai-analytics-container {
  max-width: 1400px;
  margin: 0 auto;
}

.metrics-section {
  margin-bottom: 24px;
}

.metric-card {
  height: 160px;
  text-align: center;
}

.metric-header {
  font-size: 16px;
  color: #606266;
}

.metric-value {
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

#feedback-chart,
#call-chart,
#risk-chart,
#churn-chart {
  width: 100%;
  height: 100%;
}

@media (max-width: 768px) {
  .ai-analytics-page {
    padding: 16px;
  }
  
  .metric-card {
    height: 120px;
    margin-bottom: 16px;
  }
  
  .metric-value {
    font-size: 24px;
  }
  
  .chart-content {
    height: 300px;
  }
}
</style>
