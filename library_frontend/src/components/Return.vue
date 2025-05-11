<template>
  <div class="container-fluid mt-4">
    <h2 class="text-dark text-center">Return Book</h2>
    <div class="table-responsive">
      <table class="table table-hover table-bordered table-striped text-center align-middle">
        <thead class="table-light">
          <tr>
            <th>User</th>
            <th>Book</th>
            <th>Borrow Date</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tx in transactions" :key="tx.id">
            <td>{{ userMap[tx.user] || tx.user }}</td>
            <td>{{ bookMap[tx.book] || tx.book }}</td>
            <td>{{ tx.borrow_date }}</td>
            <td>
              <button class="btn btn-sm btn-success" @click="openModal(tx)">
                <i class="fas fa-undo me-2"></i> Return
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Return Modal -->
    <div class="modal fade" id="returnModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Return Transaction #{{ selected.id }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
            <form @submit.prevent="submitReturn">
              <div class="mb-3">
                <label for="return_date" class="form-label text-dark">
                  <i class="fas fa-calendar-day me-2"></i> Return Date
                </label>
                <input v-model="form.return_date" type="date" class="form-control" :min="selected.borrow_date"
                  required />
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                  <i class="fas fa-times me-2"></i>Cancel
                </button>
                <button type="submit" class="btn btn-success">
                  <i class="fas fa-undo me-2"></i>Submit
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { fetchTransactions, fetchUsers, fetchBooks, returnBook } from '../services/api';
import { Modal } from 'bootstrap';

const transactions = ref([]);
const users = ref([]);
const books = ref([]);
const userMap = ref({});
const bookMap = ref({});
const selected = ref({});
const form = ref({ return_date: '' });
const errorMsg = ref('');
let modal;

onMounted(async () => {
  const [txRes, uRes, bRes] = await Promise.all([
    fetchTransactions(),
    fetchUsers(),
    fetchBooks()
  ]);
  transactions.value = txRes.data.filter(tx => tx.status === 'borrowed');
  users.value = uRes.data;
  books.value = bRes.data;
  users.value.forEach(u => userMap.value[u.id] = u.username);
  books.value.forEach(b => bookMap.value[b.id] = b.title);
  modal = new Modal(document.getElementById('returnModal'));
});

const openModal = (tx) => {
  selected.value = tx;
  form.value.return_date = '';
  errorMsg.value = '';
  modal.show();
};

const submitReturn = async () => {
  try {
    await returnBook(selected.value.id, form.value);
    transactions.value = transactions.value.filter(tx => tx.id !== selected.value.id);
    modal.hide();
  } catch (e) {
    errorMsg.value = e.response?.data.detail || 'Error returning book';
  }
};
</script>

<style scoped>
h2 {
  color: #4b3e30;
  margin-bottom: 1rem;
}

.btn-success {
  background-color: #6c9e46;
  border: none;
}


.table {
  background-color: #ffffff;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  font-size: 0.9rem;
}

.table th,
.table td {
  padding: 0.75rem;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: #f9f5ec;
}

.table-hover tbody tr:hover {
  background-color: #f1e8d6;
}

.table th {
  background-color: #f0e6d6;
  font-weight: bold;
  color: #4b3e30;
}

.modal-content {
  background-color: #f3ede3;
}

.modal-header {
  background-color: #d5b97b;
  color: white;
}

.form-control {
  border-radius: 6px;
  font-size: 0.9rem;
}

.form-label {
  color: #4b3e30;
}
</style>
