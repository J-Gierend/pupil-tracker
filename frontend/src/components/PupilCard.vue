<template>
  <router-link :to="`/pupil/${pupil.id}`" class="pupil-card">
    <div class="pupil-avatar">
      {{ initials }}
    </div>
    <div class="pupil-info">
      <h3 class="pupil-name">{{ pupil.first_name }} {{ pupil.last_name }}</h3>
      <p class="pupil-stats">
        {{ entryCount }} {{ t('pupil.entries').toLowerCase() }}
      </p>
    </div>
    <div v-if="averageGrade" class="pupil-grade">
      <GradeDisplay :grade="averageGrade" />
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import GradeDisplay from './GradeDisplay.vue'

const props = defineProps({
  pupil: { type: Object, required: true },
  entryCount: { type: Number, default: 0 },
  averageGrade: { type: Number, default: null }
})

const { t } = useI18n()

const initials = computed(() => {
  const first = props.pupil.first_name?.[0] || ''
  const last = props.pupil.last_name?.[0] || ''
  return (first + last).toUpperCase()
})
</script>

<style scoped>
.pupil-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s;
}

.pupil-card:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.pupil-avatar {
  width: 3rem;
  height: 3rem;
  background: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1rem;
  flex-shrink: 0;
}

.pupil-info {
  flex: 1;
  min-width: 0;
}

.pupil-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.pupil-stats {
  margin: 0.25rem 0 0;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.pupil-grade {
  flex-shrink: 0;
}
</style>
