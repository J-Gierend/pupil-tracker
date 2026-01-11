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
}

.brand-link {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-color);
  text-decoration: none;
}

.navbar-menu {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 0;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
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
}
</style>
