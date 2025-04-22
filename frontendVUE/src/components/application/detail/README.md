# Application Detail Components

This directory contains all the components used in the Application Detail page, which is part of Phase 4 implementation.

## Components Overview

1. **ApplicationOverview.vue** - Displays general application information including property details, valuer information, QS information, and signature details.

2. **BorrowersTab.vue** - Shows all borrowers and guarantors associated with the application, including their personal/company details.

3. **DocumentsTab.vue** - Manages document uploads and displays a list of all documents associated with the application.

4. **NotesTab.vue** - Allows adding notes with optional reminders and displays a timeline of all notes.

5. **RepaymentsTab.vue** - Manages the repayment schedule, allows adding new repayments and recording payments.

6. **FeesTab.vue** - Manages application fees, allows adding new fees and displays all fees.

7. **LedgerTab.vue** - Displays a financial ledger with all transactions, including a summary of fees, payments, and balance.

## Usage

These components are used in the ApplicationDetailView.vue page, which implements a tabbed interface to navigate between different aspects of the application.

```vue
<template>
  <div>
    <!-- Tab Navigation -->
    <nav>
      <button @click="activeTab = 'overview'">Overview</button>
      <button @click="activeTab = 'borrowers'">Borrowers</button>
      <!-- Other tab buttons -->
    </nav>
    
    <!-- Tab Content -->
    <div>
      <application-overview v-if="activeTab === 'overview'" :application="application" />
      <borrowers-tab v-if="activeTab === 'borrowers'" :borrowers="application.borrowers" :guarantors="application.guarantors" />
      <!-- Other tab contents -->
    </div>
  </div>
</template>
```

## Data Requirements

These components expect the application object to include all related entities as specified in the Phase 4 requirements:

- Borrowers and Guarantors
- Broker, BD, Branch
- Documents and Notes
- Repayments, Fees, Ledger entries
- Property and valuation information
- Signature and PDF data

The backend ApplicationDetailSerializer has been enhanced to include all these related entities.
