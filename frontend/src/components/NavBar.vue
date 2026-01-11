<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <router-link to="/" class="brand-link">
        Pupil Tracker
      </router-link>
    </div>
    <div class="navbar-menu">
      <router-link to="/" class="nav-link">
        {{ t('nav.dashboard') }}
      </router-link>
      <router-link to="/reports" class="nav-link">
        {{ t('nav.reports') }}
      </router-link>
      <router-link to="/settings" class="nav-link">
        {{ t('nav.settings') }}
      </router-link>
    </div>
    <div class="navbar-end">
      <LanguageToggle />
    </div>
  </nav>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import LanguageToggle from './LanguageToggle.vue'

const { t } = useI18n()
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
  background: var(--primary-light);
  background: rgba(13, 148, 136, 0.1);
}

.nav-link.router-link-active {
  color: var(--primary-color);
  background: var(--primary-light);
}

@media (max-width: 768px) {
  .navbar {
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1rem;
  }
  .navbar-menu {
    order: 3;
    width: 100%;
    justify-content: center;
  }
  .nav-link {
    padding: 0.5rem 0.75rem;
    font-size: 0.9375rem;
  }
}
</style>
