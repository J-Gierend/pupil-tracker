<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <router-link to="/" class="brand-link">
        Pupil Tracker
      </router-link>
    </div>
    <button class="menu-toggle" @click="menuOpen = !menuOpen" aria-label="Toggle menu">
      <span class="menu-icon" :class="{ open: menuOpen }"></span>
    </button>
    <div class="navbar-menu" :class="{ open: menuOpen }">
      <router-link to="/" class="nav-link" @click="menuOpen = false">
        {{ t('nav.dashboard') }}
      </router-link>
      <router-link to="/reports" class="nav-link" @click="menuOpen = false">
        {{ t('nav.reports') }}
      </router-link>
      <router-link to="/settings" class="nav-link" @click="menuOpen = false">
        {{ t('nav.settings') }}
      </router-link>
    </div>
    <div class="navbar-end">
      <LanguageToggle />
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import LanguageToggle from './LanguageToggle.vue'

const { t } = useI18n()
const menuOpen = ref(false)
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: var(--surface-color);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 50;
}

.brand-link {
  font-size: 1.375rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-decoration: none;
  letter-spacing: -0.02em;
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  width: 44px;
  height: 44px;
  align-items: center;
  justify-content: center;
}

.menu-icon {
  display: block;
  width: 24px;
  height: 2px;
  background: var(--text-color);
  position: relative;
  transition: background 0.2s;
}

.menu-icon::before,
.menu-icon::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 2px;
  background: var(--text-color);
  left: 0;
  transition: transform 0.2s;
}

.menu-icon::before { top: -7px; }
.menu-icon::after { top: 7px; }

.menu-icon.open {
  background: transparent;
}

.menu-icon.open::before {
  transform: rotate(45deg);
  top: 0;
}

.menu-icon.open::after {
  transform: rotate(-45deg);
  top: 0;
}

.navbar-menu {
  display: flex;
  gap: 0.5rem;
}

.nav-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 600;
  padding: 0.625rem 1rem;
  border-radius: var(--radius-lg);
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: var(--primary-color);
  background: rgba(13, 148, 136, 0.1);
}

.nav-link.router-link-active {
  color: var(--primary-color);
  background: var(--primary-light);
}

/* Tablet */
@media (max-width: 768px) {
  .navbar {
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
  }

  .navbar-menu {
    order: 3;
    width: 100%;
    justify-content: center;
    gap: 0.25rem;
  }

  .nav-link {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
  }

  .navbar-end {
    margin-left: auto;
  }
}

/* Mobile - hamburger menu */
@media (max-width: 480px) {
  .navbar {
    flex-wrap: nowrap;
    padding: 0.75rem 1rem;
  }

  .menu-toggle {
    display: flex;
    order: 2;
  }

  .navbar-end {
    order: 1;
    margin-left: auto;
    margin-right: 0.5rem;
  }

  .navbar-menu {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--surface-color);
    border-bottom: 1px solid var(--border-color);
    box-shadow: var(--shadow-md);
    flex-direction: column;
    padding: 0.5rem;
    gap: 0;
  }

  .navbar-menu.open {
    display: flex;
  }

  .nav-link {
    padding: 0.875rem 1rem;
    border-radius: 0.5rem;
    text-align: center;
  }

  .nav-link:active {
    background: var(--primary-light);
  }
}
</style>
