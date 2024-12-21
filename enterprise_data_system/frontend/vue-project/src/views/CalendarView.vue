<template>
  <div class="calendar-view">
    <el-card class="calendar-card">
      <template #header>
        <div class="card-header">
          <h2>Schedule Meeting</h2>
        </div>
      </template>

      <el-calendar v-model="currentDate">
        <template #header="{ date }">
          <el-row type="flex" justify="space-between" align="middle">
            <el-col :span="8">
              <el-button-group>
                <el-button size="small" @click="selectDate('prev-month')">
                  Previous Month
                </el-button>
                <el-button size="small" @click="selectDate('today')">
                  Today
                </el-button>
                <el-button size="small" @click="selectDate('next-month')">
                  Next Month
                </el-button>
              </el-button-group>
            </el-col>
            <el-col :span="8" class="text-center">
              <h3 class="month-title">{{ date.format('MMMM YYYY') }}</h3>
            </el-col>
            <el-col :span="8" class="text-right">
              <el-button type="primary" @click="showMeetingDialog">
                Schedule Meeting
              </el-button>
            </el-col>
          </el-row>
        </template>

        <template #dateCell="{ data }">
          <div class="calendar-cell">
            <p :class="{ 'is-today': isToday(data.day) }">
              {{ data.day.split('-').slice(-1)[0] }}
            </p>
            <div class="meeting-dots">
              <span 
                v-for="meeting in getMeetings(data.day)"
                :key="meeting.id"
                class="meeting-dot"
                :style="{ backgroundColor: meeting.type === 'customer' ? '#409EFF' : '#67C23A' }"
                @click.stop="showMeetingDetails(meeting)"
              ></span>
            </div>
          </div>
        </template>
      </el-calendar>
    </el-card>

    <!-- Meeting Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="editingMeeting ? 'Edit Meeting' : 'Schedule New Meeting'"
      width="500px"
    >
      <el-form
        ref="meetingFormRef"
        :model="meetingForm"
        :rules="rules"
        label-position="top"
      >
        <el-form-item label="Title" prop="title">
          <el-input v-model="meetingForm.title" placeholder="Enter meeting title" />
        </el-form-item>

        <el-form-item label="Type" prop="type">
          <el-select v-model="meetingForm.type" placeholder="Select meeting type" class="w-100">
            <el-option label="Customer Meeting" value="customer" />
            <el-option label="Internal Meeting" value="internal" />
          </el-select>
        </el-form-item>

        <el-form-item label="Date & Time" prop="datetime">
          <el-date-picker
            v-model="meetingForm.datetime"
            type="datetime"
            placeholder="Select date and time"
            class="w-100"
          />
        </el-form-item>

        <el-form-item label="Description" prop="description">
          <el-input
            v-model="meetingForm.description"
            type="textarea"
            rows="3"
            placeholder="Enter meeting description"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSaveMeeting">
          {{ editingMeeting ? 'Update' : 'Schedule' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import dayjs from 'dayjs'

const currentDate = ref(new Date())
const dialogVisible = ref(false)
const meetingFormRef = ref<FormInstance>()
const editingMeeting = ref<any>(null)

interface Meeting {
  id: number
  title: string
  type: string
  datetime: Date
  description: string
}

interface MeetingForm {
  title: string
  type: string
  datetime: Date | null
  description: string
}

const meetings = ref<Meeting[]>([
  {
    id: 1,
    title: 'Customer Review',
    type: 'customer',
    datetime: new Date(),
    description: 'Annual policy review meeting'
  }
])

const meetingForm = reactive<MeetingForm>({
  title: '',
  type: '',
  datetime: null,
  description: ''
})

const rules: FormRules = {
  title: [
    { required: true, message: 'Please enter meeting title', trigger: 'blur' },
    { min: 3, max: 50, message: 'Length should be 3 to 50 characters', trigger: 'blur' }
  ],
  type: [
    { required: true, message: 'Please select meeting type', trigger: 'change' }
  ],
  datetime: [
    { required: true, message: 'Please select date and time', trigger: 'change' }
  ]
}


const selectDate = (type: string) => {
  const date = dayjs(currentDate.value)
  switch (type) {
    case 'prev-month':
      currentDate.value = date.subtract(1, 'month').toDate()
      break
    case 'today':
      currentDate.value = new Date()
      break
    case 'next-month':
      currentDate.value = date.add(1, 'month').toDate()
      break
  }
}

const isToday = (day: string) => {
  return day === dayjs().format('YYYY-MM-DD')
}

const getMeetings = (day: string) => {
  return meetings.value.filter(meeting => 
    dayjs(meeting.datetime).format('YYYY-MM-DD') === day
  )
}

const showMeetingDialog = () => {
  editingMeeting.value = null
  Object.assign(meetingForm, {
    title: '',
    type: '',
    datetime: new Date(),
    description: ''
  })
  dialogVisible.value = true
}

const showMeetingDetails = (meeting: any) => {
  editingMeeting.value = meeting
  Object.assign(meetingForm, {
    title: meeting.title,
    type: meeting.type,
    datetime: meeting.datetime,
    description: meeting.description
  })
  dialogVisible.value = true
}

const handleSaveMeeting = async () => {
  if (!meetingFormRef.value) return

  try {
    await meetingFormRef.value.validate()
    
    if (!meetingForm.datetime) {
      ElMessage.error('Please select date and time')
      return
    }

    if (editingMeeting.value) {
      const index = meetings.value.findIndex(m => m.id === editingMeeting.value.id)
      if (index !== -1) {
        meetings.value[index] = {
          id: editingMeeting.value.id,
          title: meetingForm.title,
          type: meetingForm.type,
          datetime: meetingForm.datetime,
          description: meetingForm.description
        }
      }
      ElMessage.success('Meeting updated successfully')
    } else {
      const newMeeting: Meeting = {
        id: meetings.value.length + 1,
        title: meetingForm.title,
        type: meetingForm.type,
        datetime: meetingForm.datetime,
        description: meetingForm.description
      }
      meetings.value.push(newMeeting)
      ElMessage.success('Meeting scheduled successfully')
    }
    
    dialogVisible.value = false
  } catch (error) {
    console.error('Error:', error)
  }
}
</script>

<style scoped>
.calendar-view {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.calendar-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.month-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.calendar-cell {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 4px;
}

.is-today {
  color: #409EFF;
  font-weight: bold;
}

.meeting-dots {
  display: flex;
  gap: 4px;
  justify-content: center;
  margin-top: 4px;
}

.meeting-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  cursor: pointer;
}

.text-center {
  text-align: center;
}

.text-right {
  text-align: right;
}

.w-100 {
  width: 100%;
}

@media (max-width: 768px) {
  .calendar-view {
    padding: 16px;
  }
}
</style>
