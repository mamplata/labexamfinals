<template>
  <div class="container mt-4">
    <h2 class="text-dark text-center">Borrow Book</h2>

    <!-- Result Message (Above the Form) -->
    <transition name="fade">
      <div v-if="result" class="alert alert-info mt-3 text-center">
        {{ result }}
      </div>
    </transition>

    <div class="borrow-book-container p-4 rounded shadow-sm">
      <form @submit.prevent="submit">
        <!-- User Selection -->
        <div class="mb-3">
          <label for="user" class="form-label text-dark">
            <i class="fas fa-user me-2"></i> User
          </label>
          <select v-model="form.user" class="form-select" id="user" required>
            <option value="" disabled>Select user</option>
            <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
          </select>
        </div>

        <!-- Book Selection -->
        <div class="mb-3">
          <label for="book" class="form-label text-dark">
            <i class="fas fa-book me-2"></i> Book
          </label>
          <select v-model="form.book" class="form-select" id="book" required>
            <option value="" disabled>Select book</option>
            <option v-for="b in books" :key="b.id" :value="b.id">{{ b.title }}</option>
          </select>
        </div>

        <!-- Borrow Date -->
        <div class="mb-3">
          <label for="borrow_date" class="form-label text-dark">
            <i class="fas fa-calendar-day me-2"></i> Borrow Date
          </label>
          <input v-model="form.borrow_date" type="date" class="form-control" id="borrow_date" :max="today" required />
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn btn-success w-100">
          <i class="fas fa-arrow-right me-2"></i> Borrow
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { fetchUsers, fetchBooks, borrowBook } from '../services/api';

const users = ref([]);
const books = ref([]);
const form = ref({ user: '', book: '', borrow_date: '' });
const result = ref(null);

onMounted(async () => {
  users.value = (await fetchUsers()).data;
  books.value = (await fetchBooks()).data;
});

// Set the max attribute of the date input to today's date
const today = (() => {
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, '0');
  const dd = String(now.getDate()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd}`;
})();


const submit = async () => {
  try {
    const res = await borrowBook(form.value);
    const user = users.value.find(u => u.id === form.value.user).username;
    const book = books.value.find(b => b.id === form.value.book).title;
    result.value = `${user} borrowed "${book}" (Transaction #${res.data.id})`;
    form.value = { user: '', book: '', borrow_date: '' };

    // Auto-clear message after 3 seconds
    setTimeout(() => {
      result.value = null;
    }, 3000);
  } catch (err) {
    result.value = err.response?.data.detail || 'Error';

    // Auto-clear error message after 5 seconds
    setTimeout(() => {
      result.value = null;
    }, 5000);
  }
};

</script>

<style scoped>
/* Main container styling */
.container {
  max-width: 800px;
  margin: auto;
}

/* Borrow book container styling */
.borrow-book-container {
  background-color: #f3ede3;
  border-radius: 12px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

/* Heading Style */
h2 {
  color: #4b3e30;
  margin-bottom: 1.5rem;
}

/* Form Inputs */
.form-select,
.form-control {
  border-radius: 6px;
  font-size: 0.9rem;
}

.form-label {
  color: #4b3e30;
}

.fas {
  font-size: 1.1rem;
}

.btn-success {
  background-color: #6c9e46;
  border: none;
}

/* Result Message */
.alert-info {
  background-color: #f3ede3;
  color: #4b3e30;
  font-weight: 500;
  transition: opacity 0.5s ease-in-out;
}

/* Fade Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

/* Margin for spacing */
.mb-3 {
  margin-bottom: 1.25rem;
}
</style>
