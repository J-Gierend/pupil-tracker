<template>
  <router-link
    v-if="pupil"
    :to="`/pupil/${entry.pupil_id}`"
    class="recent-entry"
  >
    <div class="entry-info">
      <span class="entry-pupil">
        {{ pupil.first_name }} {{ pupil.last_name }}
      </span>
      <span class="entry-date">{{ formatDate(entry.date) }}</span>
    </div>
    <GradeDisplay :grade="entry.grade" />
  </router-link>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import GradeDisplay from './GradeDisplay.vue'

const props = defineProps({
  entry: { type: Object, required: true },
  pupil: { type: Object, default: null }
})

const { locale } = useI18n()

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString(locale.value === 'de' ? 'de-DE' : 'en-US')
}
</script>

<style scoped>
.recent-entry {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s;
}

.recent-entry:hover {
  border-color: var(--primary-color);
}

.entry-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.entry-pupil {
  font-weight: 500;
}

.entry-date {
  font-size: 0.875rem;
  color: var(--text-secondary);
}
</style>
