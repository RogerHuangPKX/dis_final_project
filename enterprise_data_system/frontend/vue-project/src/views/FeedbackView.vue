<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'

interface Feedback {
  id: number
  customer: number
  customer_name: string
  customer_email: string
  feedback_text: string
  sentiment_score: number
  key_topics: string[]
  created_at: string
}

const feedbacks = ref<Feedback[]>([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

const getSentimentColor = (score: number) => {
  if (score >= 0.7) return '#67C23A'  // Green
  if (score >= 0.4) return '#E6A23C'  // Yellow
  return '#F56C6C'  // Red
}

const getSentimentLabel = (score: number) => {
  if (score >= 0.7) return 'Positive'
  if (score >= 0.4) return 'Neutral'
  return 'Negative'
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString()
}

const fetchFeedbacks = async (page = 1) => {
  loading.value = true
  try {
    const response = await api.get('/api/feedbacks/', {
      params: {
        page,
        page_size: pageSize.value
      }
    })
    feedbacks.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('Error fetching feedbacks:', error)
    ElMessage.error('Failed to fetch feedback data')
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchFeedbacks(page)
}

onMounted(() => {
  fetchFeedbacks()
})
</script>

<template>
  <div class="feedback-view">
    <div class="header">
      <h2>Customer Feedback</h2>
      <el-button type="primary" @click="fetchFeedbacks">
        <el-icon><Refresh /></el-icon>
        Refresh
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="feedbacks"
      style="width: 100%"
      border
    >
      <el-table-column
        label="Customer"
        width="180"
      >
        <template #default="{ row }">
          <div>
            <div>{{ row.customer_name }}</div>
            <div class="customer-email">{{ row.customer_email }}</div>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column
        prop="feedback_text"
        label="Feedback"
        min-width="300"
      />
      
      <el-table-column
        label="Sentiment"
        width="120"
      >
        <template #default="{ row }">
          <el-tag
            :style="{ backgroundColor: getSentimentColor(row.sentiment_score) }"
            effect="dark"
          >
            {{ getSentimentLabel(row.sentiment_score) }}
            ({{ row.sentiment_score.toFixed(2) }})
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column
        label="Topics"
        width="200"
      >
        <template #default="{ row }">
          <el-tag
            v-for="topic in row.key_topics"
            :key="topic"
            class="topic-tag"
            size="small"
          >
            {{ topic }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column
        label="Created At"
        width="180"
      >
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        @size-change="() => fetchFeedbacks(1)"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<style scoped>
.feedback-view {
  padding: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.topic-tag {
  margin-right: 4px;
  margin-bottom: 4px;
}

.customer-email {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

:deep(.el-table) {
  margin-top: 16px;
}

@media (max-width: 768px) {
  .feedback-view {
    padding: 16px;
  }
}
</style>
