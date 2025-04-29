<template>
  <div class="dashboard-view">
    <div class="container-fluid py-4">
      <h1 class="h3 mb-4">Dashboard</h1>
      
      <!-- Loading state -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading dashboard data...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
        <button class="btn btn-sm btn-outline-danger ms-3" @click="fetchDashboardData">
          Try Again
        </button>
      </div>

      <!-- Dashboard content -->
      <div v-else>
        <div class="row">
          <!-- Summary Cards -->
          <div class="col-md-3 mb-4">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">Applications</h5>
                <h2 class="display-4">{{ dashboardData.applicationVolume?.total_applications || 0 }}</h2>
                <p class="text-muted">Total applications</p>
                <div class="d-grid">
                  <router-link to="/applications" class="btn btn-sm btn-outline-primary">
                    View Applications
                  </router-link>
                </div>
              </div>
            </div>
          </div>
          
          <div class="col-md-3 mb-4">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">Active Loans</h5>
                <h2 class="display-4">{{ dashboardData.applicationStatus?.total_active || 0 }}</h2>
                <p class="text-muted">Active loans</p>
                <div class="d-grid">
                  <router-link to="/applications?stage=funded" class="btn btn-sm btn-outline-primary">
                    View Active Loans
                  </router-link>
                </div>
              </div>
            </div>
          </div>
          
          <div class="col-md-3 mb-4">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">Total Loan Amount</h5>
                <h2 class="display-4">${{ formatCurrency(dashboardData.applicationVolume?.total_loan_amount || 0) }}</h2>
                <p class="text-muted">Total loan value</p>
                <div class="d-grid">
                  <router-link to="/applications" class="btn btn-sm btn-outline-primary">
                    View Applications
                  </router-link>
                </div>
              </div>
            </div>
          </div>
          
          <div class="col-md-3 mb-4">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">Repayment Compliance</h5>
                <h2 class="display-4">{{ Math.round(dashboardData.repaymentCompliance?.compliance_rate || 0) }}%</h2>
                <p class="text-muted">On-time payment rate</p>
                <div class="d-grid">
                  <router-link to="/repayments" class="btn btn-sm btn-outline-primary">
                    View Repayments
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="row">
          <!-- Recent Applications -->
          <div class="col-md-6 mb-4">
            <div class="card h-100">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="card-title mb-0">Recent Applications</h5>
                <router-link to="/applications" class="btn btn-sm btn-outline-primary">
                  View All
                </router-link>
              </div>
              <div class="card-body">
                <div v-if="loadingApplications" class="text-center py-4">
                  <div class="spinner-border spinner-border-sm" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
                <div v-else-if="recentApplications.length === 0" class="text-center py-4">
                  <p class="text-muted mb-0">No recent applications</p>
                </div>
                <div v-else class="table-responsive">
                  <table class="table table-hover">
                    <thead>
                      <tr>
                        <th>Reference</th>
                        <th>Type</th>
                        <th>Amount</th>
                        <th>Stage</th>
                        <th>Created</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="app in recentApplications" :key="app.id" @click="navigateToApplication(app.id)" style="cursor: pointer;">
                        <td>{{ app.reference_number }}</td>
                        <td>{{ app.application_type }}</td>
                        <td>${{ formatCurrency(app.loan_amount) }}</td>
                        <td>
                          <span class="badge" :class="getStageClass(app.stage)">
                            {{ app.stage_display || app.stage }}
                          </span>
                        </td>
                        <td>{{ formatDate(app.created_at) }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Recent Notifications -->
          <div class="col-md-6 mb-4">
            <div class="card h-100">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="card-title mb-0">Recent Notifications</h5>
                <router-link to="/notifications" class="btn btn-sm btn-outline-primary">
                  View All
                </router-link>
              </div>
              <div class="card-body">
                <div v-if="loadingNotifications" class="text-center py-4">
                  <div class="spinner-border spinner-border-sm" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
                <div v-else-if="recentNotifications.length === 0" class="text-center py-4">
                  <p class="text-muted mb-0">No recent notifications</p>
                </div>
                <div v-else class="list-group">
                  <a 
                    v-for="notification in recentNotifications" 
                    :key="notification.id" 
                    href="#" 
                    class="list-group-item list-group-item-action"
                    :class="{ 'list-group-item-light': !notification.is_read }"
                    @click.prevent="viewNotification(notification)"
                  >
                    <div class="d-flex w-100 justify-content-between">
                      <h6 class="mb-1">{{ notification.title }}</h6>
                      <small>{{ formatTimeAgo(notification.created_at) }}</small>
                    </div>
                    <p class="mb-1">{{ notification.message }}</p>
                    <small>{{ notification.notification_type_display || notification.notification_type }}</small>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="row">
          <!-- Quick Actions -->
          <div class="col-md-6 mb-4">
            <div class="card h-100">
              <div class="card-header">
                <h5 class="card-title mb-0">Quick Actions</h5>
              </div>
              <div class="card-body">
                <div class="row g-3">
                  <div class="col-md-6">
                    <div class="d-grid">
                      <router-link to="/applications/create" class="btn btn-primary">
                        <i class="bi bi-plus-circle me-2"></i> New Application
                      </router-link>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="d-grid">
                      <router-link to="/borrowers/create" class="btn btn-outline-primary">
                        <i class="bi bi-person-plus me-2"></i> New Borrower
                      </router-link>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="d-grid">
                      <router-link to="/documents/upload" class="btn btn-outline-primary">
                        <i class="bi bi-upload me-2"></i> Upload Document
                      </router-link>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="d-grid">
                      <router-link to="/notes/create" class="btn btn-outline-primary">
                        <i class="bi bi-journal-plus me-2"></i> Add Note
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Upcoming Repayments -->
          <div class="col-md-6 mb-4">
            <div class="card h-100">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="card-title mb-0">Upcoming Repayments</h5>
                <router-link to="/repayments" class="btn btn-sm btn-outline-primary">
                  View All
                </router-link>
              </div>
              <div class="card-body">
                <div v-if="loadingRepayments" class="text-center py-4">
                  <div class="spinner-border spinner-border-sm" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
                <div v-else-if="upcomingRepayments.length === 0" class="text-center py-4">
                  <p class="text-muted mb-0">No upcoming repayments</p>
                </div>
                <div v-else class="table-responsive">
                  <table class="table table-hover">
                    <thead>
                      <tr>
                        <th>Application</th>
                        <th>Amount</th>
                        <th>Due Date</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="repayment in upcomingRepayments" :key="repayment.id">
                        <td>{{ getApplicationReference(repayment.application) }}</td>
                        <td>${{ formatCurrency(repayment.amount) }}</td>
                        <td>{{ formatDate(repayment.due_date) }}</td>
                        <td>
                          <span class="badge" :class="getRepaymentStatusClass(repayment.status)">
                            {{ formatRepaymentStatus(repayment.status) }}
                          </span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useApplicationStore } from '@/store/application'
import { useNotificationStore } from '@/store/notification'
import { useRepaymentStore } from '@/store/repayment'
import dashboardService from '@/services/dashboard.service'

export default {
  name: 'DashboardView',
  setup() {
    const router = useRouter()
    const applicationStore = useApplicationStore()
    const notificationStore = useNotificationStore()
    const repaymentStore = useRepaymentStore()
    
    // State
    const loading = ref(false)
    const loadingApplications = ref(false)
    const loadingNotifications = ref(false)
    const loadingRepayments = ref(false)
    const error = ref(null)
    const dashboardData = ref({})
    const recentApplications = ref([])
    const recentNotifications = ref([])
    const upcomingRepayments = ref([])
    
    // Methods
    const fetchDashboardData = async () => {
      loading.value = true
      error.value = null
      
      try {
        // Try to fetch dashboard data from the reports endpoints
        dashboardData.value = await dashboardService.getDashboardData()
        fetchRecentApplications()
        fetchRecentNotifications()
        fetchUpcomingRepayments()
      } catch (err) {
        // If dashboard data fetch fails, continue with other data
        console.error('Error fetching dashboard data:', err)
        // Set dashboardData to default values to prevent errors
        dashboardData.value = {
          applicationVolume: {
            total_applications: 0,
            total_loan_amount: 0,
            average_loan_amount: 0,
            stage_breakdown: {},
            time_breakdown: [],
            bd_breakdown: [],
            type_breakdown: {}
          },
          applicationStatus: {
            total_active: 0,
            total_settled: 0,
            total_declined: 0,
            total_withdrawn: 0,
            active_by_stage: {},
            avg_time_in_stage: {},
            inquiry_to_approval_rate: 0,
            approval_to_settlement_rate: 0,
            overall_success_rate: 0
          },
          repaymentCompliance: {
            total_repayments: 0,
            paid_on_time: 0,
            paid_late: 0,
            missed: 0,
            compliance_rate: 0,
            average_days_late: 0,
            total_amount_due: 0,
            total_amount_paid: 0,
            payment_rate: 0,
            monthly_breakdown: []
          }
        }
        
        // Continue with other data fetches
        fetchRecentApplications()
        fetchRecentNotifications()
        fetchUpcomingRepayments()
      } finally {
        loading.value = false
      }
    }
    
    const fetchRecentApplications = async () => {
      loadingApplications.value = true
      
      try {
        const params = {
          page: 1,
          limit: 5,
          sort: '-created_at'
        }
        
        const response = await applicationStore.fetchApplications(params)
        recentApplications.value = response.results || []
      } catch (err) {
        console.error('Error fetching recent applications:', err)
        recentApplications.value = []
      } finally {
        loadingApplications.value = false
      }
    }
    
    const fetchRecentNotifications = async () => {
      loadingNotifications.value = true
      
      try {
        const params = {
          page: 1,
          limit: 5,
          sort: '-created_at'
        }
        
        const response = await notificationStore.fetchNotifications(params)
        // Ensure we have a results array even if the response is unexpected
        recentNotifications.value = response && response.results ? response.results : []
      } catch (err) {
        console.error('Error fetching recent notifications:', err)
        recentNotifications.value = []
      } finally {
        loadingNotifications.value = false
      }
    }
    
    const fetchUpcomingRepayments = async () => {
      loadingRepayments.value = true
      
      try {
        const params = {
          page: 1,
          limit: 5,
          is_paid: false,
          sort: 'due_date'
        }
        
        const response = await repaymentStore.fetchRepayments(params)
        upcomingRepayments.value = response.results || []
      } catch (err) {
        console.error('Error fetching upcoming repayments:', err)
        upcomingRepayments.value = []
      } finally {
        loadingRepayments.value = false
      }
    }
    
    const navigateToApplication = (id) => {
      router.push(`/applications/${id}`)
    }
    
    const viewNotification = async (notification) => {
      if (!notification.is_read) {
        try {
          await notificationStore.markAsRead(notification.id)
        } catch (error) {
          console.error('Error marking notification as read:', error)
        }
      }
      
      // Handle navigation based on notification type
      if (notification.related_object_type === 'application' && notification.related_object_id) {
        router.push(`/applications/${notification.related_object_id}`)
      } else {
        router.push('/notifications')
      }
    }
    
    const getApplicationReference = (applicationId) => {
      const app = recentApplications.value.find(app => app.id === applicationId)
      return app ? app.reference_number : `App #${applicationId}`
    }
    
    const formatCurrency = (value) => {
      return value ? value.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 }) : '0'
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
    }
    
    const formatTimeAgo = (dateString) => {
      if (!dateString) return ''
      
      const date = new Date(dateString)
      const now = new Date()
      const diffMs = now - date
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMins / 60)
      const diffDays = Math.floor(diffHours / 24)
      
      if (diffMins < 1) {
        return 'Just now'
      } else if (diffMins < 60) {
        return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`
      } else if (diffHours < 24) {
        return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`
      } else if (diffDays < 7) {
        return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`
      } else {
        return formatDate(dateString)
      }
    }
    
    const getStageClass = (stage) => {
      const stageClasses = {
        'inquiry': 'bg-secondary',
        'pre_approval': 'bg-info',
        'valuation': 'bg-primary',
        'formal_approval': 'bg-warning',
        'settlement': 'bg-success',
        'funded': 'bg-success',
        'declined': 'bg-danger',
        'withdrawn': 'bg-dark'
      }
      
      return stageClasses[stage] || 'bg-secondary'
    }
    
    const getRepaymentStatusClass = (status) => {
      if (!status) return 'bg-secondary'
      
      if (status === 'paid') {
        return 'bg-success'
      } else if (status.includes('overdue')) {
        return 'bg-danger'
      } else if (status.includes('due_soon')) {
        return 'bg-warning'
      } else {
        return 'bg-info'
      }
    }
    
    const formatRepaymentStatus = (status) => {
      if (!status) return 'Unknown'
      
      if (status === 'paid') {
        return 'Paid'
      } else if (status === 'scheduled') {
        return 'Scheduled'
      } else if (status.includes('overdue')) {
        const days = status.split('_').pop()
        return `Overdue (${days} days)`
      } else if (status.includes('due_soon')) {
        const days = status.split('_').pop()
        return `Due Soon (${days} days)`
      } else {
        return status
      }
    }
    
    // Fetch data on component mount
    onMounted(() => {
      fetchDashboardData()
    })
    
    return {
      loading,
      loadingApplications,
      loadingNotifications,
      loadingRepayments,
      error,
      dashboardData,
      recentApplications,
      recentNotifications,
      upcomingRepayments,
      fetchDashboardData,
      navigateToApplication,
      viewNotification,
      getApplicationReference,
      formatCurrency,
      formatDate,
      formatTimeAgo,
      getStageClass,
      getRepaymentStatusClass,
      formatRepaymentStatus
    }
  }
}
</script>

<style scoped>
.dashboard-view {
  min-height: 100vh;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.list-group-item-light {
  background-color: #f8f9fa;
  border-left: 3px solid #0d6efd;
}
</style>
