<template>
  <button 
    @click="exportReport"
    class="flex items-center bg-green-500 hover:bg-green-600 text-white font-medium py-2 px-4 rounded transition-colors"
  >
    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
    </svg>
    Export {{ format }}
  </button>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  reportData: {
    type: Object,
    required: true
  },
  reportName: {
    type: String,
    required: true
  },
  format: {
    type: String,
    default: 'CSV',
    validator: (value) => ['CSV', 'JSON', 'PDF'].includes(value)
  }
})

// Function to export report data
const exportReport = () => {
  if (props.format === 'CSV') {
    exportCSV()
  } else if (props.format === 'JSON') {
    exportJSON()
  } else if (props.format === 'PDF') {
    exportPDF()
  }
}

// Export as CSV
const exportCSV = () => {
  // Convert report data to CSV format
  let csvContent = ''
  
  // Handle different report types
  if (props.reportName === 'repayment-compliance') {
    // Header row
    csvContent = 'Month,Total Repayments,Paid On Time,Paid Late,Missed,Compliance Rate,Amount Due,Amount Paid,Payment Rate\n'
    
    // Data rows
    props.reportData.monthly_breakdown.forEach(month => {
      csvContent += `${month.month},${month.total_repayments},${month.paid_on_time},${month.paid_late},${month.missed},${month.compliance_rate}%,${month.amount_due},${month.amount_paid},${month.payment_rate}%\n`
    })
    
    // Summary row
    csvContent += `\nTotal,${props.reportData.total_repayments},${props.reportData.paid_on_time},${props.reportData.paid_late},${props.reportData.missed},${props.reportData.compliance_rate}%,${props.reportData.total_amount_due},${props.reportData.total_amount_paid},${props.reportData.payment_rate}%\n`
  } else if (props.reportName === 'application-volume') {
    // Header row for time breakdown
    csvContent = 'Period,Application Count,Total Amount\n'
    
    // Data rows for time breakdown
    props.reportData.time_breakdown.forEach(period => {
      csvContent += `${period.period},${period.count},${period.total_amount}\n`
    })
    
    // Add stage breakdown
    csvContent += '\nStage,Count\n'
    Object.entries(props.reportData.stage_breakdown).forEach(([stage, count]) => {
      csvContent += `${stage},${count}\n`
    })
    
    // Add BD breakdown
    csvContent += '\nBD Name,Applications,Total Amount\n'
    props.reportData.bd_breakdown.forEach(bd => {
      csvContent += `${bd.bd_name || 'No BD'},${bd.count},${bd.total_amount}\n`
    })
  } else if (props.reportName === 'application-status') {
    // Header row for status summary
    csvContent = 'Status,Count\n'
    csvContent += `Active,${props.reportData.total_active}\n`
    csvContent += `Settled,${props.reportData.total_settled}\n`
    csvContent += `Declined,${props.reportData.total_declined}\n`
    csvContent += `Withdrawn,${props.reportData.total_withdrawn}\n`
    
    // Add active by stage
    csvContent += '\nActive Stage,Count\n'
    Object.entries(props.reportData.active_by_stage).forEach(([stage, count]) => {
      csvContent += `${stage},${count}\n`
    })
    
    // Add conversion rates
    csvContent += '\nConversion Type,Rate\n'
    csvContent += `Inquiry to Approval,${props.reportData.inquiry_to_approval_rate}%\n`
    csvContent += `Approval to Settlement,${props.reportData.approval_to_settlement_rate}%\n`
    csvContent += `Overall Success,${props.reportData.overall_success_rate}%\n`
  }
  
  // Create a download link
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', `${props.reportName}-report.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Export as JSON
const exportJSON = () => {
  const jsonContent = JSON.stringify(props.reportData, null, 2)
  const blob = new Blob([jsonContent], { type: 'application/json;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', `${props.reportName}-report.json`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Export as PDF (placeholder - would typically use a library like jsPDF)
const exportPDF = () => {
  alert('PDF export functionality would be implemented with a library like jsPDF. This is a placeholder.')
  
  // In a real implementation, you would:
  // 1. Use jsPDF or similar library
  // 2. Create a PDF document
  // 3. Add report title, date, and data
  // 4. Add charts as images
  // 5. Save and download the PDF
}
</script>
