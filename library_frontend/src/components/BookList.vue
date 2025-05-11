<template>
  <div class="container-fluid mt-4">
    <h2 class="text-dark text-center">Books</h2>
    <button class="btn btn-success mb-3" @click="openAddModal">
      <i class="fas fa-book me-2"></i> Add Book
    </button>
    <transition name="fade">
      <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
    </transition>
    <!-- Book Table -->
    <div class="table-responsive">
      <table class="table table-hover table-bordered table-striped text-center align-middle">
        <thead class="table-light">
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>ISBN</th>
            <th>Copies</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in books" :key="b.id">
            <td>{{ b.title }}</td>
            <td>{{ b.author }}</td>
            <td>{{ b.isbn }}</td>
            <td>{{ b.copies_available }}</td>
            <td>
              <div class="btn-group" role="group">
                <button class="btn btn-sm btn-warning me-2 rounded" @click="openEditModal(b)">
                  <i class="fas fa-edit"></i> Edit
                </button>
                <button class="btn btn-sm btn-danger rounded" @click="removeBook(b.id)" :disabled="b.is_borrowed"
                  title="Cannot delete while some copies are borrowed">
                  <i class="fas fa-trash"></i> Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>


    <!-- Add/Edit Modal -->
    <div class="modal fade" id="bookModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas" :class="isEditing ? 'fa-edit' : 'fa-plus'"></i> {{ isEditing ? 'Edit Book' :
                'Add Book' }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
            <form @submit.prevent="saveBook">
              <div class="mb-3">
                <label class="form-label">
                  <i class="fas fa-book me-2"></i> Title
                </label>
                <input v-model="form.title" class="form-control" required />
                <div v-if="form.errors.title" class="text-danger">{{ form.errors.title }}</div>
              </div>
              <div class="mb-3">
                <label class="form-label">
                  <i class="fas fa-user me-2"></i> Author
                </label>
                <input v-model="form.author" class="form-control" required />
                <div v-if="form.errors.author" class="text-danger">{{ form.errors.author }}</div>
              </div>
              <div class="mb-3">
                <label class="form-label">
                  <i class="fas fa-barcode me-2"></i> ISBN
                </label>
                <input v-model="form.isbn" class="form-control" required />
                <div v-if="form.errors.isbn" class="text-danger">{{ form.errors.isbn }}</div>
              </div>
              <div class="mb-3">
                <label class="form-label">
                  <i class="fas fa-copy me-2"></i> Copies Available
                </label>
                <input v-model.number="form.copies_available" type="number" min="0" class="form-control" required
                  @input="validateCopiesAvailable" />
                <div v-if="form.errors.copies_available" class="text-danger">{{
                  form.errors.copies_available }}</div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              <i class="fas fa-times me-2"></i>Cancel
            </button>
            <button type="button" class="btn btn-success" @click="saveBook">
              <i class="fas fa-check me-2"></i>{{ isEditing ? 'Save' : 'Add' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { fetchBooks, createBook, updateBook, deleteBook } from '../services/api';
import { Modal } from 'bootstrap';

const books = ref([]);
const form = ref({
  title: '',
  author: '',
  isbn: '',
  copies_available: 1,
  errors: {}
});
const isEditing = ref(false);
const editId = ref(null);
const errorMsg = ref('');
let modal;

const showError = (message, timeout = 4000) => {
  errorMsg.value = message;
  setTimeout(() => {
    errorMsg.value = '';
  }, timeout);
};

const loadBooks = async () => {
  try {
    books.value = (await fetchBooks()).data;
  } catch {
    showError('Failed to load books');
  }
};

onMounted(() => {
  loadBooks();
  modal = new Modal(document.getElementById('bookModal'));
});

const openAddModal = () => {
  isEditing.value = false;
  form.value = {
    title: '',
    author: '',
    isbn: '',
    copies_available: 1,
    errors: {}
  };
  errorMsg.value = '';
  modal.show();
};

const openEditModal = (b) => {
  isEditing.value = true;
  editId.value = b.id;
  form.value = {
    ...b,
    errors: {}
  };
  errorMsg.value = '';
  modal.show();
};

const saveBook = async () => {
  form.value.errors = {}; // Clear previous errors
  try {
    if (isEditing.value) {
      await updateBook(editId.value, form.value);
    } else {
      await createBook(form.value);
    }
    modal.hide();
    loadBooks();
  } catch (e) {
    if (e.response && e.response.data) {
      const errors = e.response.data;
      Object.keys(errors).forEach(field => {
        form.value.errors[field] = errors[field].join(', ');
      });
    } else {
      showError(e.response?.data?.detail || 'Error saving book');
    }
  }
};

const removeBook = async (id) => {
  if (!confirm('Delete this book?')) return;
  try {
    await deleteBook(id);
    loadBooks();
  } catch (e) {
    if (e.response && e.response.data && e.response.data.message) {
      showError(e.response.data.message);
    } else {
      showError('Error deleting book');
    }
  }
};

const validateCopiesAvailable = () => {
  if (form.value.copies_available < 0) {
    form.value.copies_available = 0;
  }
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

h2 {
  color: #4b3e30;
  margin-bottom: 1rem;
}

.btn-success {
  background-color: #6c9e46;
  border: none;
}

.btn-warning {
  background-color: #f0ad4e;
  border: none;
}

.btn-danger {
  background-color: #d9534f;
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
