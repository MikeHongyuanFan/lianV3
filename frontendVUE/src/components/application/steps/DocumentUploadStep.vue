<template>
  <div class="document-upload-step">
    <h2 class="step-title">Document Upload & Signature</h2>
    
    <div class="form-section">
      <h3>Required Documents</h3>
      <p class="section-description">
        Please upload all required documents for your loan application. Accepted formats: PDF, JPG, PNG.
      </p>
      
      <div class="document-list">
        <div v-for="(docType, index) in requiredDocumentTypes" :key="index" class="document-item">
          <div class="document-type">
            <h4>{{ docType.label }} <span class="required-badge">Required</span></h4>
            <p>{{ docType.description }}</p>
          </div>
          
          <div class="document-upload">
            <div v-if="getDocumentByType(docType.value)" class="document-preview">
              <div class="document-info">
                <span class="document-name">{{ getDocumentByType(docType.value).file.name }}</span>
                <span class="document-size">{{ formatFileSize(getDocumentByType(docType.value).file.size) }}</span>
              </div>
              <button @click="removeDocument(docType.value)" class="btn btn-danger btn-sm">
                Remove
              </button>
            </div>
            <div v-else class="upload-container">
              <label :for="`document-${index}`" class="upload-label">
                <span class="upload-icon">📄</span>
                <span class="upload-text">Click to upload</span>
              </label>
              <input 
                :id="`document-${index}`" 
                type="file" 
                class="file-input" 
                @change="(e) => handleFileUpload(e, docType.value)"
                accept=".pdf,.jpg,.jpeg,.png"
              />
            </div>
          </div>
        </div>
      </div>
      
      <h3 class="mt-6">Additional Documents</h3>
      <p class="section-description">
        Upload any additional documents that may support your application.
      </p>
      
      <div class="additional-documents">
        <div v-for="(doc, index) in additionalDocuments" :key="index" class="document-item">
          <div class="document-type">
            <select 
              v-model="doc.type" 
              class="form-control"
              @change="validateForm"
            >
              <option value="">Select document type</option>
              <option v-for="option in additionalDocumentTypes" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </div>
          
          <div class="document-upload">
            <div v-if="doc.file" class="document-preview">
              <div class="document-info">
                <span class="document-name">{{ doc.file.name }}</span>
                <span class="document-size">{{ formatFileSize(doc.file.size) }}</span>
              </div>
              <button @click="removeAdditionalDocument(index)" class="btn btn-danger btn-sm">
                Remove
              </button>
            </div>
            <div v-else class="upload-container">
              <label :for="`additional-document-${index}`" class="upload-label">
                <span class="upload-icon">📄</span>
                <span class="upload-text">Click to upload</span>
              </label>
              <input 
                :id="`additional-document-${index}`" 
                type="file" 
                class="file-input" 
                @change="(e) => handleAdditionalFileUpload(e, index)"
                accept=".pdf,.jpg,.jpeg,.png"
              />
            </div>
          </div>
        </div>
        
        <button @click="addAdditionalDocument" class="btn btn-secondary mt-3">
          Add Another Document
        </button>
      </div>
      
      <h3 class="mt-6">Electronic Signature</h3>
      <p class="section-description">
        Please sign below to confirm that all information provided in this application is true and correct.
      </p>
      
      <div class="signature-section">
        <div v-if="!localFormData.signature" class="signature-pad-container">
          <div ref="signaturePad" class="signature-pad"></div>
          <div class="signature-actions">
            <button @click="clearSignature" class="btn btn-secondary btn-sm">Clear</button>
            <button @click="saveSignature" class="btn btn-primary btn-sm">Save Signature</button>
          </div>
        </div>
        <div v-else class="signature-preview">
          <img :src="localFormData.signature" alt="Signature" class="signature-image" />
          <button @click="resetSignature" class="btn btn-secondary btn-sm">Reset Signature</button>
        </div>
        
        <div class="form-group mt-3">
          <label for="signatureDate">Signature Date*</label>
          <input 
            type="date" 
            id="signatureDate" 
            v-model="localFormData.signature_date" 
            class="form-control"
            :max="today"
            required
            @input="validateForm"
          />
        </div>
        
        <div class="declaration">
          <input 
            type="checkbox" 
            id="declaration" 
            v-model="declarationChecked" 
            @change="validateForm"
          />
          <label for="declaration">
            I declare that the information provided in this application is true and correct to the best of my knowledge.
            I understand that providing false or misleading information may result in the rejection of my application.
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onBeforeUnmount } from 'vue';
import SignaturePad from 'signature_pad';

const props = defineProps({
  formData: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['update:formData', 'validate']);

// Create a local copy of the form data to work with
const localFormData = reactive({
  documents: [],
  signature: null,
  signature_date: ''
});

const signaturePad = ref(null);
const signaturePadElement = ref(null);
const declarationChecked = ref(false);
const additionalDocuments = ref([{ type: '', file: null }]);

// Today's date for max signature date
const today = computed(() => {
  return new Date().toISOString().split('T')[0];
});

// Required document types
const requiredDocumentTypes = [
  { 
    value: 'id_verification', 
    label: 'ID Verification', 
    description: 'Driver\'s license, passport, or other government-issued ID' 
  },
  { 
    value: 'income_proof', 
    label: 'Proof of Income', 
    description: 'Recent pay slips, tax returns, or bank statements' 
  },
  { 
    value: 'property_details', 
    label: 'Property Details', 
    description: 'Property valuation, purchase contract, or title deed' 
  }
];

// Additional document types
const additionalDocumentTypes = [
  { value: 'bank_statement', label: 'Bank Statement' },
  { value: 'tax_return', label: 'Tax Return' },
  { value: 'employment_letter', label: 'Employment Letter' },
  { value: 'insurance_policy', label: 'Insurance Policy' },
  { value: 'business_financials', label: 'Business Financial Statements' },
  { value: 'trust_deed', label: 'Trust Deed' },
  { value: 'other', label: 'Other Document' }
];

// Initialize the local form data from props
onMounted(() => {
  if (props.formData) {
    if (props.formData.documents && props.formData.documents.length > 0) {
      localFormData.documents = [...props.formData.documents];
    }
    localFormData.signature = props.formData.signature || null;
    localFormData.signature_date = props.formData.signature_date || '';
  }
  
  // Initialize signature pad
  if (!localFormData.signature) {
    initSignaturePad();
  }
  
  validateForm();
});

onBeforeUnmount(() => {
  // Clean up signature pad
  if (signaturePad.value) {
    signaturePad.value.off();
  }
});

// Watch for changes in the local form data and emit updates
watch(localFormData, (newValue) => {
  emit('update:formData', {
    documents: newValue.documents,
    signature: newValue.signature,
    signature_date: newValue.signature_date
  });
}, { deep: true });

// Watch for changes in additional documents
watch(additionalDocuments, () => {
  updateDocuments();
}, { deep: true });

// Initialize signature pad
function initSignaturePad() {
  nextTick(() => {
    if (signaturePadElement.value) {
      signaturePad.value = new SignaturePad(signaturePadElement.value, {
        backgroundColor: 'rgb(255, 255, 255)',
        penColor: 'rgb(0, 0, 0)'
      });
    }
  });
}

// Clear signature pad
function clearSignature() {
  if (signaturePad.value) {
    signaturePad.value.clear();
  }
  validateForm();
}

// Save signature from pad
function saveSignature() {
  if (signaturePad.value && !signaturePad.value.isEmpty()) {
    localFormData.signature = signaturePad.value.toDataURL();
    validateForm();
  }
}

// Reset signature
function resetSignature() {
  localFormData.signature = null;
  nextTick(() => {
    initSignaturePad();
  });
  validateForm();
}

// Handle file upload for required documents
function handleFileUpload(event, documentType) {
  const file = event.target.files[0];
  if (file) {
    // Remove existing document of the same type if it exists
    const existingIndex = localFormData.documents.findIndex(doc => doc.type === documentType);
    if (existingIndex !== -1) {
      localFormData.documents.splice(existingIndex, 1);
    }
    
    // Add the new document
    localFormData.documents.push({
      type: documentType,
      file: file
    });
    
    validateForm();
  }
}

// Handle file upload for additional documents
function handleAdditionalFileUpload(event, index) {
  const file = event.target.files[0];
  if (file) {
    additionalDocuments.value[index].file = file;
    validateForm();
  }
}

// Add an additional document slot
function addAdditionalDocument() {
  additionalDocuments.value.push({ type: '', file: null });
}

// Remove a required document
function removeDocument(documentType) {
  const index = localFormData.documents.findIndex(doc => doc.type === documentType);
  if (index !== -1) {
    localFormData.documents.splice(index, 1);
    validateForm();
  }
}

// Remove an additional document
function removeAdditionalDocument(index) {
  additionalDocuments.value.splice(index, 1);
  if (additionalDocuments.value.length === 0) {
    addAdditionalDocument();
  }
}

// Update documents array with additional documents
function updateDocuments() {
  // Filter out additional documents from the current documents array
  const requiredDocs = localFormData.documents.filter(doc => 
    requiredDocumentTypes.some(type => type.value === doc.type)
  );
  
  // Add valid additional documents
  const validAdditionalDocs = additionalDocuments.value
    .filter(doc => doc.type && doc.file)
    .map(doc => ({
      type: doc.type,
      file: doc.file
    }));
  
  // Update the documents array
  localFormData.documents = [...requiredDocs, ...validAdditionalDocs];
  
  validateForm();
}

// Get document by type
function getDocumentByType(type) {
  return localFormData.documents.find(doc => doc.type === type);
}

// Format file size
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Validate the form
function validateForm() {
  let isValid = true;
  
  // Check if all required documents are uploaded
  for (const docType of requiredDocumentTypes) {
    if (!getDocumentByType(docType.value)) {
      isValid = false;
      break;
    }
  }
  
  // Check if signature exists
  if (!localFormData.signature) {
    isValid = false;
  }
  
  // Check if signature date is provided
  if (!localFormData.signature_date) {
    isValid = false;
  }
  
  // Check if declaration is checked
  if (!declarationChecked.value) {
    isValid = false;
  }
  
  // Check if additional documents have both type and file
  for (const doc of additionalDocuments.value) {
    if ((doc.type && !doc.file) || (!doc.type && doc.file)) {
      isValid = false;
      break;
    }
  }
  
  emit('validate', isValid);
}
</script>

<style scoped>
.document-upload-step {
  padding: 1rem 0;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #2d3748;
}

.form-section {
  background-color: #f7fafc;
  border-radius: 8px;
  padding: 1.5rem;
}

h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.mt-6 {
  margin-top: 1.5rem;
}

.mt-3 {
  margin-top: 0.75rem;
}

.section-description {
  color: #4a5568;
  margin-bottom: 1.5rem;
}

.document-list {
  margin-bottom: 2rem;
}

.document-item {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  padding: 1rem;
  background-color: white;
  border-radius: 4px;
  margin-bottom: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.document-type {
  flex: 1;
  min-width: 250px;
  padding-right: 1rem;
}

.document-type h4 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
}

.required-badge {
  background-color: #e53e3e;
  color: white;
  font-size: 0.75rem;
  padding: 0.1rem 0.5rem;
  border-radius: 9999px;
  margin-left: 0.5rem;
}

.document-type p {
  font-size: 0.875rem;
  color: #718096;
  margin: 0;
}

.document-upload {
  flex: 1;
  min-width: 250px;
}

.upload-container {
  border: 2px dashed #cbd5e0;
  border-radius: 4px;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-container:hover {
  border-color: #4299e1;
}

.upload-label {
  display: block;
  cursor: pointer;
}

.upload-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 0.5rem;
}

.upload-text {
  color: #4a5568;
  font-weight: 500;
}

.file-input {
  display: none;
}

.document-preview {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #edf2f7;
  padding: 0.75rem;
  border-radius: 4px;
}

.document-info {
  overflow: hidden;
}

.document-name {
  display: block;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
}

.document-size {
  font-size: 0.75rem;
  color: #718096;
}

.signature-section {
  margin-top: 1.5rem;
}

.signature-pad-container {
  margin-bottom: 1rem;
}

.signature-pad {
  border: 1px solid #cbd5e0;
  border-radius: 4px;
  background-color: white;
  width: 100%;
  height: 200px;
}

.signature-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
  gap: 0.5rem;
}

.signature-preview {
  margin-bottom: 1rem;
}

.signature-image {
  max-width: 100%;
  max-height: 200px;
  border: 1px solid #cbd5e0;
  border-radius: 4px;
  background-color: white;
}

.form-group {
  margin-bottom: 1rem;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #cbd5e0;
  border-radius: 4px;
  font-size: 1rem;
}

.declaration {
  display: flex;
  align-items: flex-start;
  margin-top: 1.5rem;
}

.declaration input {
  margin-top: 0.25rem;
  margin-right: 0.5rem;
}

.declaration label {
  font-size: 0.875rem;
  color: #4a5568;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-primary {
  background-color: #4299e1;
  color: white;
}

.btn-primary:hover {
  background-color: #3182ce;
}

.btn-secondary {
  background-color: #a0aec0;
  color: white;
}

.btn-secondary:hover {
  background-color: #718096;
}

.btn-danger {
  background-color: #e53e3e;
  color: white;
}

.btn-danger:hover {
  background-color: #c53030;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.additional-documents {
  margin-bottom: 2rem;
}
</style>
