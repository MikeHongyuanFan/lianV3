

# 🛠️ Full Frontend Integration Scanning and Mapping Process

---

## **PHASE 1 — "Scan and Record APIs (Alone)"**

### 🎯 Goal:
- Scan the backend project
- **Find and list every API endpoint**
- For **each API**, record the following basic info **separately**.

### 📝 For EACH API
| Field | Description |
|:-----|:------------|
| API URL | Example: `/api/applications/` |
| HTTP Method | Example: `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Required Input Fields | What fields need to be sent when calling this API? (Example: `name`, `email`, `loan_amount`) |
| Response Fields | What fields are returned in the response? (Example: `id`, `status`, `created_at`) |
| Status Codes | What status codes to expect? (Example: `200`, `400`, `401`, `404`, `500`) |
| Authentication Required? | Does the API require login/authentication token? (`Yes` or `No`) |
| Pagination? | Does this API have pagination? (e.g., `limit`, `offset`) |
| Search/Filter Support? | Does this API support search or filtering? (Specify parameters) |

## Recommendations for Improvement:

1. Consolidate duplicate endpoints: The application signature endpoints (/sign/ and /signature/) should be consolidated to avoid confusion.

2. Standardize notification endpoints: The notification endpoints should use a consistent naming convention - either all using the ViewSet routes or all using the explicit routes.

3. Update create-with-cascade documentation: Clarify that this endpoint uses the same view as the regular create endpoint.

4. Verify HTTP methods: Double-check that all HTTP methods are correctly documented, especially for endpoints that support multiple methods.

5. Check required fields: Ensure that all required fields are accurately documented for each endpoint.

**Rules:**  
- 🛑 **Only scan one API at a time**.
- 🛑 **DO NOT think about relationships** yet.
- 🛑 **DO NOT assume frontend usage yet**.

**step-by-step, phased**, clean, powerful, idiot-proof.

Here’s the updated doc you can send Q Chat:  

---

## Goal:
You (Q Chat) are tasked to help build the frontend integration for this project.  
Your job is to **scan the backend** and **record** every necessary API information for frontend development.  
You must do it **step by step**, **one API at a time**, and **follow phases**.  
Do not skip or merge phases unless I explicitly tell you to.

---

## 🎯 Phases You Must Complete:

### Phase 1 — API Endpoint Mapping (Already Done ✅)
- Find and list all available API endpoints.
- Verify URL path, HTTP method, and a short description.
- Identify any duplicate or unclear endpoints.

✅ *This phase is completed.*

---

### Phase 2 — Full Request/Response Specification (Input/Output)
**For each API endpoint:**
- List all **input fields** required, including:
  - Field name
  - Field type (string, integer, boolean, etc.)
  - Whether the field is required (yes/no)
  - Field validation (min length, max length, choices if any)
- List all **output fields** returned in the response:
  - Field name
  - Field type
  - If the field can be `null`
- Provide **example request body** and **example response body**.

📢 **Important:**  
Focus on only **one API** at a time.  
When done, wait for my confirmation to move to the next API.

---

### Phase 3 — Relationship Documentation
**For each API endpoint:**
- Identify if the API requires any **foreign keys** or **relationships** (e.g., borrower ID, application ID).
- If so, specify:
  - Linked model (e.g., `Application`, `Borrower`, `User`)
  - How the frontend should get these linked values (e.g., dropdown search API, manual input)

📢 **Important:**  
Mention **whether the ID must already exist** or **can create a new one**.

---

### Phase 4 — Pagination, Search, Filtering
**For list APIs (GET list):**
- Specify:
  - Pagination method (e.g., `limit/offset`, `page/size`, cursor pagination)
  - Searchable fields (e.g., search by name, email, reference number)
  - Filterable fields (e.g., stage, status, owner)
- Provide example query parameters.

📢 **Important:**  
If pagination is missing, mention it.

---

### Phase 5 — Error Handling and Validation
**For each API endpoint:**
- List all common HTTP error codes it may return (e.g., 400, 403, 404, 500).
- For each error code:
  - Describe when it happens.
  - Provide example error response body.
- Mention if there are any special validation rules not obvious from fields.

---

### Phase 6 — Special API Behavior
**Check for APIs with special behavior:**
- File upload (e.g., upload document, image)
- File download (e.g., PDF generation, document download)
- APIs that accept or return **Base64** data
- APIs that have **background processing** (e.g., asynchronous tasks)
- APIs that **trigger other operations** (e.g., send email, notification)

📢 **Important:**  
Explain any extra steps needed by the frontend.

---

## 🛑 Golden Rules for You (Q Chat)

- ❌ Do not assume anything that is not in the code or clear documentation.
- ❌ Do not try to summarize multiple APIs together. Always work one API at a time.
- ✅ After finishing one API completely, wait for user approval to proceed to the next.
- ✅ If any field is not documented, say "**Not documented, need backend clarification**."
- ✅ If any relationship is unclear, say "**Not clear, recommend frontend confirm with backend**."

---

---

# ✅ Expected Final Outcome:

When all phases are completed,  
we will have for every API:
- Input fields ✅
- Output fields ✅
- Relationships ✅
- Pagination/search/filter rules ✅
- Error handling ✅
- Special behaviors ✅  

Ready for frontend to code **seamlessly with no guesswork**.


# 🔥 End of Instruction


