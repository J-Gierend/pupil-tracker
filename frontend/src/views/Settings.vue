<template>
  <div class="settings">
    <h1 class="page-title">{{ t('settings.title') }}</h1>

    <div class="settings-grid">
      <SettingsSchoolYears />
      <SettingsClasses />
      <SettingsCategories />
      <SettingsExport />
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import SettingsSchoolYears from '../components/SettingsSchoolYears.vue'
import SettingsClasses from '../components/SettingsClasses.vue'
import SettingsCategories from '../components/SettingsCategories.vue'
import SettingsExport from '../components/SettingsExport.vue'

const { t } = useI18n()
</script>

<style scoped>
.page-title { margin: 0 0 1.5rem; font-size: 1.75rem; }

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .settings-grid { grid-template-columns: 1fr; }
}
</style>
