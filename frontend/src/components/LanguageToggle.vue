<template>
  <div class="language-toggle">
    <button
      :class="['lang-btn', { active: locale === 'de' }]"
      @click="setLocale('de')"
    >
      DE
    </button>
    <button
      :class="['lang-btn', { active: locale === 'en' }]"
      @click="setLocale('en')"
    >
      EN
    </button>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

function setLocale(lang) {
  locale.value = lang
  localStorage.setItem('locale', lang)
}
</script>

<style scoped>
.language-toggle {
  display: flex;
  gap: 0.25rem;
  background: var(--bg-color);
  padding: 0.25rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
}

.lang-btn {
  padding: 0.5rem 0.875rem;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 0.8125rem;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  letter-spacing: 0.025em;
}

.lang-btn:hover {
  color: var(--primary-color);
  background: rgba(13, 148, 136, 0.1);
}

.lang-btn.active {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  color: white;
  box-shadow: 0 2px 4px rgba(13, 148, 136, 0.25);
}
</style>
