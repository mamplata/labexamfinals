<template>
  <div class="container-fluid mt-4">
    <h2 class="text-dark text-center">Borrowing Transactions</h2>
    <div class="table-responsive">
      <table class="table table-hover table-bordered table-striped text-center align-middle">
        <thead class="table-light">
          <tr>
            <th>#ID</th>
            <th>User</th>
            <th>Book</th>
            <th>Borrow Date</th>
            <th>Return Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tx in transactions" :key="tx.id">
            <td>{{ tx.id }}</td>
            <td>{{ userMap[tx.user] }}</td>
            <td>
              <span v-if="bookMap[tx.book]">{{ bookMap[tx.book] }}</span>
              <span v-else class="text-muted fst-italic">Not available</span>
            </td>
            <td>{{ tx.borrow_date }}</td>
            <td>
              <span v-if="tx.return_date">{{ tx.return_date }}</span>
              <span v-else class="text-muted fst-italic">Not yet returned</span>
            </td>
            <td>
              <span :class="['badge', tx.status === 'borrowed' ? 'bg-warning' : 'bg-success']">
                {{ tx.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { fetchTransactions, fetchUsers, fetchBooks } from '../services/api';

const transactions = ref([]);
const userMap = ref({});
const bookMap = ref({});

onMounted(async () => {
  const [txRes, uRes, bRes] = await Promise.all([
    fetchTransactions(),
    fetchUsers(),
    fetchBooks()
  ]);
  transactions.value = txRes.data;
  uRes.data.forEach(u => userMap.value[u.id] = u.username);
  bRes.data.forEach(b => bookMap.value[b.id] = b.title);
});
</script>

<style scoped>
h2 {
  color: #4b3e30;
  margin-bottom: 1rem;
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
</style>
