<template>
  <el-container>
    <el-header>
      <h2>Analytics Dashboard</h2>
    </el-header>

    <el-main>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>Customer Risk Distribution</span>
              </div>
            </template>
            <div id="riskChart" style="height: 300px"></div>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>Sentiment Analysis</span>
              </div>
            </template>
            <div id="sentimentChart" style="height: 300px"></div>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>Churn Prediction</span>
              </div>
            </template>
            <div id="churnChart" style="height: 300px"></div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="12">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>Top Risk Factors</span>
              </div>
            </template>
            <el-table :data="riskFactors" border>
              <el-table-column prop="factor" label="Risk Factor" />
              <el-table-column prop="impact" label="Impact Score">
                <template #default="scope">
                  <el-progress :percentage="scope.row.impact * 100" />
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>Product Recommendations</span>
              </div>
            </template>
            <el-table :data="recommendations" border>
              <el-table-column prop="product" label="Product" />
              <el-table-column prop="score" label="Match Score">
                <template #default="scope">
                  <el-progress :percentage="scope.row.score * 100" status="success" />
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

const riskFactors = ref([])
const recommendations = ref([])
let charts = {
  risk: null as echarts.ECharts | null,
  sentiment: null as echarts.ECharts | null,
  churn: null as echarts.ECharts | null
}

const fetchAnalyticsData = async () => {
  try {
    const response = await fetch('/api/analytics/dashboard')
    const data = await response.json()
    
    updateCharts(data)
    riskFactors.value = data.riskFactors
    recommendations.value = data.recommendations
  } catch (error) {
    ElMessage.error('Failed to fetch analytics data')
    console.error('Analytics data error:', error)
  }
}

const updateCharts = (data: any) => {
  if (charts.risk) {
    charts.risk.setOption({
      title: { text: 'Risk Distribution' },
      tooltip: {},
      xAxis: { type: 'category', data: ['Low', 'Medium', 'High'] },
      yAxis: { type: 'value' },
      series: [{ type: 'bar', data: data.riskDistribution }]
    })
  }

  if (charts.sentiment) {
    charts.sentiment.setOption({
      title: { text: 'Customer Sentiment' },
      tooltip: {},
      series: [{
        type: 'pie',
        data: [
          { value: data.sentiment.positive, name: 'Positive' },
          { value: data.sentiment.neutral, name: 'Neutral' },
          { value: data.sentiment.negative, name: 'Negative' }
        ]
      }]
    })
  }

  if (charts.churn) {
    charts.churn.setOption({
      title: { text: 'Churn Risk' },
      tooltip: {},
      series: [{
        type: 'gauge',
        progress: { show: true },
        detail: { valueAnimation: true, formatter: '{value}%' },
        data: [{ value: data.churnRisk }]
      }]
    })
  }
}

onMounted(() => {
  charts.risk = echarts.init(document.getElementById('riskChart'))
  charts.sentiment = echarts.init(document.getElementById('sentimentChart'))
  charts.churn = echarts.init(document.getElementById('churnChart'))
  
  fetchAnalyticsData()
  
  // Refresh data every 5 minutes
  setInterval(fetchAnalyticsData, 300000)
  
  // Handle window resize
  window.addEventListener('resize', () => {
    Object.values(charts).forEach(chart => chart?.resize())
  })
})
</script>

<style scoped>
.el-header {
  margin-bottom: 20px;
}
</style>
