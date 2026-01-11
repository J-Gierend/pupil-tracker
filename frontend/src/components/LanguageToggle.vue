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
  border-radius: 0.5rem;
}

.lang-btn {
  padding: 0.375rem 0.75rem;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 0.875rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.lang-btn:hover {
  color: var(--text-color);
}

.lang-btn.active {
  background: var(--primary-color);
  color: white;
}
</style>
