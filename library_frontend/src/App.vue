<template>
  <div class="main-wrapper">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg shadow-sm bg-navbar py-3">
      <div class="container-fluid d-flex justify-content-between align-items-center">
        <!-- Logo + Title -->
        <a class="navbar-brand d-flex align-items-center custom-logo" href="#" @click.prevent="selectView('books')">
          <img src="@/assets/library_logo.png" alt="Library Logo" class="logo-img" />
          <span class="d-none d-md-inline ms-2">Library Management System</span>
        </a>
        <!-- Toggler -->
        <button class="navbar-toggler" type="button" @click="toggleNavbar" :aria-expanded="!isNavbarCollapsed"
          aria-label="Toggle navigation">
          <span class="custom-toggler-icon">
            <i :class="isNavbarCollapsed ? 'fas fa-bars' : 'fas fa-times'"></i>
          </span>
        </button>

        <!-- Nav Items -->
        <div :class="['collapse', 'navbar-collapse', { show: !isNavbarCollapsed }]" id="navbarNav">
          <ul class="navbar-nav ms-auto text-center">
            <li v-for="item in navItems" :key="item.view" class="nav-item mx-2">
              <a href="#" class="nav-link custom-nav-link" :class="{ active: view === item.view }"
                @click.prevent="selectView(item.view)" :aria-current="view === item.view ? 'page' : undefined">
                <i :class="item.icon + ' me-2'"></i>
                {{ item.label }}
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Loading -->
    <div class="container-fluid py-5 d-flex justify-content-center align-items-center" v-if="loading">
      <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Content with fade transition -->
    <div class="container-fluid" v-else>
      <transition name="fade" mode="out-in">
        <component :is="currentComponent" key="view" />
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import BookList from './components/BookList.vue'
import TransactionList from './components/TransactionList.vue'
import Borrow from './components/Borrow.vue'
import Return from './components/Return.vue'

const view = ref('books')
const isNavbarCollapsed = ref(true)
const loading = ref(true)

// unified view selection
const selectView = (newView) => {
  if (view.value === newView) return
  view.value = newView
  loading.value = true
  setTimeout(() => { loading.value = false }, 400)
}

// initial load
setTimeout(() => { loading.value = false }, 400)

const navItems = [
  { label: 'Books', view: 'books', icon: 'fas fa-book-open' },
  { label: 'Transactions', view: 'transactions', icon: 'fas fa-handshake' },
  { label: 'Borrow', view: 'borrow', icon: 'fas fa-arrow-right' },
  { label: 'Return', view: 'return', icon: 'fas fa-arrow-left' }
]

const currentComponent = computed(() => ({
  books: BookList,
  transactions: TransactionList,
  borrow: Borrow,
  return: Return
}[view.value]))

const toggleNavbar = () => { isNavbarCollapsed.value = !isNavbarCollapsed.value }
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

* {
  font-family: 'Inter', sans-serif
}

.main-wrapper {
  background-color: #fdfaf5;
  min-height: 100vh
}

/* Navbar base */
.bg-navbar {
  background-color: #faf3e8
}

.navbar {
  transition: background-color 0.3s ease
}

.navbar:hover {
  background-color: #f2e8dc
}

/* Logo */
.custom-logo {
  transition: transform 0.2s ease;
}

.custom-logo:hover {
  transform: scale(1.05)
}

.logo-img {
  height: 50px;
  width: auto
}

/* Toggler */
.navbar-toggler {
  border: none;
  outline: none
}

.custom-toggler-icon i {
  font-size: 1.25rem;
  color: #4b3e30
}

/* Nav links */
.custom-nav-link {
  color: #4b3e30;
  font-weight: 500;
  position: relative;
  padding: 0.5rem;
  transition: all 0.2s ease
}

.custom-nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 3px;
  background: #d5b97b;
  transition: width 0.3s ease;
}

.custom-nav-link:hover {
  color: #3b3226;
}

.custom-nav-link:hover::after {
  width: 100%;
}

.custom-nav-link.active {
  color: #3b3226;
  font-weight: 600
}

.custom-nav-link.active::after {
  width: 100%;
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0
}

/* Responsive tweaks */
@media (max-width: 992px) {
  .navbar-nav {
    margin-top: 1rem
  }

  .custom-nav-link {
    display: block;
    padding: 0.75rem
  }
}

@media (max-width: 576px) {
  .navbar-brand span {
    font-size: 1.2rem
  }
}
</style>
