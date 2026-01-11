<template>
  <router-link :to="`/pupil/${pupil.id}`" class="pupil-card">
    <div class="card-header">
      <div class="pupil-avatar">
        {{ initials }}
      </div>
      <div class="pupil-identity">
        <h3 class="pupil-name">{{ pupil.first_name }} {{ pupil.last_name }}</h3>
        <span class="entry-count">{{ entryCount }} {{ t('pupil.entries') }}</span>
      </div>
      <div v-if="averageGrade" class="grade-badge" :class="gradeClass">
        {{ averageGrade.toFixed(1) }}
      </div>
    </div>

    <div v-if="recentEntries.length > 0" class="recent-entries">
      <div v-for="entry in recentEntries.slice(0, 2)" :key="entry.id" class="entry-preview">
        <span class="entry-date">{{ formatDate(entry.date) }}</span>
        <span class="entry-text">{{ truncateText(entry.notes || t('entry.noNotes'), 50) }}</span>
      </div>
    </div>

    <div v-else class="no-entries">
      {{ t('pupil.noEntries') }}
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  pupil: { type: Object, required: true },
  entryCount: { type: Number, default: 0 },
  averageGrade: { type: Number, default: null },
  recentEntries: { type: Array, default: () => [] }
})

const { t, locale } = useI18n()

const initials = computed(() => {
  const first = props.pupil.first_name?.[0] || ''
  const last = props.pupil.last_name?.[0] || ''
  return (first + last).toUpperCase()
})

const gradeClass = computed(() => {
  if (!props.averageGrade) return ''
  if (props.averageGrade <= 2) return 'grade-good'
  if (props.averageGrade <= 3) return 'grade-ok'
  if (props.averageGrade <= 4) return 'grade-warn'
  return 'grade-poor'
})

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString(locale.value === 'de' ? 'de-DE' : 'en-US', {
    day: '2-digit',
    month: 'short'
  })
}

function truncateText(text, maxLength) {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}
</script>

<style scoped>
.pupil-card {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s;
  min-height: 140px;
}

.pupil-card:hover {
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.pupil-avatar {
  width: 2.5rem;
  height: 2.5rem;
  background: linear-gradient(135deg, var(--primary-color), #14b8a6);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.pupil-identity {
  flex: 1;
  min-width: 0;
}

.pupil-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.3;
  color: var(--text-primary);
}

.entry-count {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.grade-badge {
  width: 2rem;
  height: 2rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.grade-good { background: #dcfce7; color: #166534; }
.grade-ok { background: #fef3c7; color: #92400e; }
.grade-warn { background: #fed7aa; color: #9a3412; }
.grade-poor { background: #fecaca; color: #991b1b; }

.recent-entries {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.entry-preview {
  display: flex;
  flex-direction: column;
  padding: 0.5rem;
  background: var(--bg-color);
  border-radius: 0.5rem;
  font-size: 0.8rem;
}

.entry-date {
  font-weight: 600;
  color: var(--primary-color);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.entry-text {
  color: var(--text-secondary);
  line-height: 1.3;
  margin-top: 0.125rem;
}

.no-entries {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-style: italic;
}

/* Touch devices - remove hover effects that don't work well */
@media (hover: none) and (pointer: coarse) {
  .pupil-card:hover {
    transform: none;
    box-shadow: var(--shadow-sm);
  }

  .pupil-card:active {
    background: var(--surface-hover);
  }
}

/* Mobile adjustments */
@media (max-width: 480px) {
  .pupil-card {
    min-height: auto;
    padding: 0.875rem;
  }

  .pupil-avatar {
    width: 2.25rem;
    height: 2.25rem;
    font-size: 0.8rem;
  }

  .pupil-name {
    font-size: 0.9375rem;
  }

  .entry-preview {
    padding: 0.375rem;
  }
}
</style>
