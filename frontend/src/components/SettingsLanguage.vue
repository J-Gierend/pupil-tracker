<template>
  <section class="settings-section">
    <h2 class="section-title">{{ t('settings.language') }}</h2>
    <div class="language-options">
      <button
        :class="['lang-option', { active: locale === 'de' }]"
        @click="setLocale('de')"
      >
        Deutsch
      </button>
      <button
        :class="['lang-option', { active: locale === 'en' }]"
        @click="setLocale('en')"
      >
        English
      </button>
    </div>
  </section>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()

function setLocale(lang) {
  locale.value = lang
  localStorage.setItem('locale', lang)
}
</script>

<style scoped>
.settings-section {
  background: var(--surface-color);
  padding: 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid var(--border-color);
}

.section-title {
  margin: 0 0 1rem;
  font-size: 1.125rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border-color);
}

.language-options {
  display: flex;
  gap: 0.5rem;
}

.lang-option {
  padding: 0.75rem 1.5rem;
  border: 2px solid var(--border-color);
  background: var(--bg-color);
  color: var(--text-color);
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.lang-option:hover {
  border-color: var(--primary-color);
}

.lang-option.active {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}
</style>
