<template>
  <div class="broker-list-placeholder">
    <div class="container-fluid py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Brokers</h1>
        <button class="btn btn-primary">
          <i class="bi bi-plus-circle me-2"></i> Add Broker
        </button>
      </div>

      <!-- Search and filters -->
      <div class="card mb-4">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-6">
              <div class="input-group">
                <span class="input-group-text">
                  <i class="bi bi-search"></i>
                </span>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Search by name, email, or phone"
                />
              </div>
            </div>
            <div class="col-md-4">
              <select class="form-select">
                <option value="">All Branches</option>
                <option value="1">Sydney Branch</option>
                <option value="2">Melbourne Branch</option>
                <option value="3">Brisbane Branch</option>
              </select>
            </div>
            <div class="col-md-2">
              <button class="btn btn-outline-secondary w-100">
                Clear Filters
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Broker list -->
      <div class="row">
        <div class="col-md-4 mb-4">
          <div class="card">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="card-title mb-0">John Smith</h5>
                <div>
                  <button class="btn btn-sm btn-outline-primary me-2">
                    <i class="bi bi-eye"></i> View
                  </button>
                  <button class="btn btn-sm btn-outline-secondary">
                    <i class="bi bi-pencil"></i> Edit
                  </button>
                </div>
              </div>
              <p class="mb-1">
                <i class="bi bi-envelope me-2"></i>
                john.smith@example.com
              </p>
              <p class="mb-1">
                <i class="bi bi-telephone me-2"></i>
                +61 2 1234 5678
              </p>
              <p class="mb-1">
                <i class="bi bi-building me-2"></i>
                Sydney Branch
              </p>
              <p class="mb-1">
                <i class="bi bi-briefcase me-2"></i>
                License: BRK12345
              </p>
            </div>
          </div>
        </div>

        <div class="col-md-4 mb-4">
          <div class="card">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="card-title mb-0">Jane Doe</h5>
                <div>
                  <button class="btn btn-sm btn-outline-primary me-2">
                    <i class="bi bi-eye"></i> View
                  </button>
                  <button class="btn btn-sm btn-outline-secondary">
                    <i class="bi bi-pencil"></i> Edit
                  </button>
                </div>
              </div>
              <p class="mb-1">
                <i class="bi bi-envelope me-2"></i>
                jane.doe@example.com
              </p>
              <p class="mb-1">
                <i class="bi bi-telephone me-2"></i>
                +61 3 9876 5432
              </p>
              <p class="mb-1">
                <i class="bi bi-building me-2"></i>
                Melbourne Branch
              </p>
              <p class="mb-1">
                <i class="bi bi-briefcase me-2"></i>
                License: BRK67890
              </p>
            </div>
          </div>
        </div>

        <div class="col-md-4 mb-4">
          <div class="card">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="card-title mb-0">Michael Johnson</h5>
                <div>
                  <button class="btn btn-sm btn-outline-primary me-2">
                    <i class="bi bi-eye"></i> View
                  </button>
                  <button class="btn btn-sm btn-outline-secondary">
                    <i class="bi bi-pencil"></i> Edit
                  </button>
                </div>
              </div>
              <p class="mb-1">
                <i class="bi bi-envelope me-2"></i>
                michael.johnson@example.com
              </p>
              <p class="mb-1">
                <i class="bi bi-telephone me-2"></i>
                +61 7 5555 1234
              </p>
              <p class="mb-1">
                <i class="bi bi-building me-2"></i>
                Brisbane Branch
              </p>
              <p class="mb-1">
                <i class="bi bi-briefcase me-2"></i>
                License: BRK24680
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div class="d-flex justify-content-between align-items-center mt-4">
        <div>
          Showing 1 to 3 of 3 brokers
        </div>
        <nav aria-label="Broker pagination">
          <ul class="pagination mb-0">
            <li class="page-item disabled">
              <a class="page-link" href="#" tabindex="-1" aria-disabled="true">Previous</a>
            </li>
            <li class="page-item active"><a class="page-link" href="#">1</a></li>
            <li class="page-item">
              <a class="page-link" href="#">Next</a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BrokerListPlaceholder'
}
</script>

<style scoped>
.broker-list-placeholder {
  min-height: 100vh;
}

.card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>
