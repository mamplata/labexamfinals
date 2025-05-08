<template>
  <div class="main-wrapper">
    <nav class="navbar navbar-expand-lg shadow-sm bg-navbar py-3">
      <div class="container-fluid d-flex justify-content-between align-items-center">
        <a class="navbar-brand fw-semibold fs-4 text-dark" href="#" @click.prevent="view = 'books'">
          <img src="@/assets/library_logo.png" alt="Library Logo" style="height: 65px;" />
          Library Management System
        </a>
        <!-- Toggler button to show or hide navbar -->
        <button class="navbar-toggler" type="button" @click="toggleNavbar"
          aria-expanded="isNavbarCollapsed ? 'false' : 'true'" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <!-- Collapse content -->
        <div :class="['collapse', 'navbar-collapse', { 'show': !isNavbarCollapsed }]" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item" v-for="item in navItems" :key="item.view">
              <a href="#" class="nav-link custom-nav-link" :class="{ active: view === item.view }"
                @click.prevent="view = item.view">
                <i :class="item.icon + ' me-2'"></i> <!-- Font Awesome Icon -->
                {{ item.label }}
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container-fluid py-5 d-flex justify-content-center align-items-center" v-if="loading">
      <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div class="container-fluid" v-else>
      <component :is="currentComponent" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import BookList from './components/BookList.vue';
import TransactionList from './components/TransactionList.vue';
import Borrow from './components/Borrow.vue';
import Return from './components/Return.vue';

const view = ref('books');
const isNavbarCollapsed = ref(true); // state to manage navbar
const loading = ref(true); // state to manage loading spinner

watch(view, () => {
  loading.value = true;
  setTimeout(() => {
    loading.value = false;
  }, 500);
});

// Initial loading
setTimeout(() => {
  loading.value = false;
}, 500);

const navItems = [
  { label: 'Books', view: 'books', icon: 'fas fa-book-open' },
  { label: 'Transactions', view: 'transactions', icon: 'fas fa-handshake' },
  { label: 'Borrow', view: 'borrow', icon: 'fas fa-arrow-right' },
  { label: 'Return', view: 'return', icon: 'fas fa-arrow-left' }
];

const currentComponent = computed(() => {
  return {
    books: BookList,
    transactions: TransactionList,
    borrow: Borrow,
    return: Return
  }[view.value];
});

// Toggle function for navbar collapse
const toggleNavbar = () => {
  isNavbarCollapsed.value = !isNavbarCollapsed.value;
};
</script>

<style scoped>
/* Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

* {
  font-family: 'Inter', sans-serif;
}

/* Body Background */
.main-wrapper {
  background-color: #fdfaf5;
  min-height: 100vh;
}

/* Navbar Style */
.bg-navbar {
  background-color: #f3ede3;
}

.navbar-brand {
  color: #4b3e30;
  font-weight: 600;
  transition: color 0.3s ease, transform 0.2s ease;
}

.navbar-nav {
  margin-bottom: 0;
}

.custom-nav-link {
  color: #4b3e30;
  font-weight: 500;
  position: relative;
  padding: 0.5rem 0;
  transition: color 0.2s ease;
  text-decoration: none;
}

.custom-nav-link::after {
  content: "";
  display: block;
  height: 2px;
  background: #d5b97b;
  transition: width 0.3s ease;
  width: 0;
  margin-top: 4px;
}

.custom-nav-link:hover {
  color: #3b3226;
}

.custom-nav-link:hover::after,
.custom-nav-link.active::after {
  width: 100%;
}

.custom-nav-link.active {
  font-weight: 600;
  color: #3b3226;
}

/* Responsive Navbar */
@media (max-width: 992px) {
  .navbar-nav {
    text-align: center;
    margin-top: 1rem;
  }

  .navbar-nav .nav-item {
    margin-bottom: 0.5rem;
  }
}

@media (max-width: 576px) {
  .navbar-brand {
    font-size: 1.25rem;
  }

}
</style>
