<template>
  <div class="container-fluid mt-4">
    <h2 class="text-dark text-center">Return Book</h2>

    <!-- For each user group -->
    <div v-for="group in groupedTx" :key="group.user" class="mb-5">
      <h4 class="text-secondary">User: {{ userMap[group.user] }}</h4>

      <div class="table-responsive">
        <table class="table table-hover table-bordered table-striped text-center align-middle">
          <thead class="table-light">
            <tr>
              <th>Book</th>
              <th>Author</th>
              <th>Borrow Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tx in group.txs" :key="tx.id">
              <td>{{ bookMap[tx.book] }}</td>
              <td>{{ bookAuthorMap[tx.book] }}</td>
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
                  :max="today" required />
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
import { ref, computed, onMounted } from 'vue';
import { fetchTransactions, fetchUsers, fetchBooks, returnBook } from '../services/api';
import { Modal } from 'bootstrap';

// compute today's date
const today = (() => {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
})();

const transactions = ref([]);
const users = ref([]);
const books = ref([]);
const userMap = ref({});
const bookMap = ref({});
const bookAuthorMap = ref({});
const selected = ref({});
const form = ref({ return_date: '' });
const errorMsg = ref('');
let modal;

// load data
onMounted(async () => {
  const [txRes, uRes, bRes] = await Promise.all([
    fetchTransactions(),
    fetchUsers(),
    fetchBooks()
  ]);
  // only still-borrowed
  transactions.value = txRes.data.filter(tx => tx.status === 'borrowed');
  users.value = uRes.data;
  books.value = bRes.data;
  users.value.forEach(u => userMap.value[u.id] = u.username);
  books.value.forEach(b => {
    bookMap.value[b.id] = b.title;
    bookAuthorMap.value[b.id] = b.author;
  });
  modal = new Modal(document.getElementById('returnModal'));
});

// grouping by user
const groupedTx = computed(() => {
  const map = {};
  transactions.value.forEach(tx => {
    if (!map[tx.user]) map[tx.user] = [];
    map[tx.user].push(tx);
  });
  // convert to array of { user, txs }
  return Object.entries(map).map(([user, txs]) => ({ user, txs }));
});

const openModal = (tx) => {
  selected.value = tx;
  form.value.return_date = today;   // default to today
  errorMsg.value = '';
  modal.show();
};

const submitReturn = async () => {
  try {
    await returnBook(selected.value.id, form.value);
    // remove returned tx from list
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
