<template>
  <div class="entry-list">
    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>

    <div v-else-if="entries.length === 0" class="empty">
      {{ t('pupil.noEntries') }}
    </div>

    <div v-else class="entries">
      <div v-for="entry in sortedEntries" :key="entry.id" class="entry-card">
        <div class="entry-header">
          <span class="entry-date">{{ formatDate(entry.date) }}</span>
          <span class="entry-category">{{ getCategoryName(entry.category_id) }}</span>
        </div>

        <div class="entry-body">
          <GradeDisplay :grade="entry.grade" />
          <p v-if="entry.notes" class="entry-notes">{{ entry.notes }}</p>
        </div>

        <div class="entry-actions">
          <button class="btn-icon" @click="$emit('edit', entry)" title="Edit">
            [Edit]
          </button>
          <button class="btn-icon btn-danger" @click="confirmDelete(entry)" title="Delete">
            [Del]
          </button>
        </div>
      </div>
    </div>

    <div v-if="showConfirm" class="confirm-dialog">
      <div class="confirm-content">
        <p>{{ t('entry.confirmDelete') }}</p>
        <div class="confirm-actions">
          <button class="btn btn-secondary" @click="showConfirm = false">
            {{ t('common.no') }}
          </button>
          <button class="btn btn-danger" @click="doDelete">
            {{ t('common.yes') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import GradeDisplay from './GradeDisplay.vue'

const props = defineProps({
  entries: { type: Array, default: () => [] },
  categories: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['edit', 'delete'])
const { t, locale } = useI18n()

const showConfirm = ref(false)
const entryToDelete = ref(null)

const sortedEntries = computed(() => {
  return [...props.entries].sort((a, b) => new Date(b.date) - new Date(a.date))
})

function getCategoryName(id) {
  const cat = props.categories.find(c => c.id === id)
  if (!cat) return ''
  return locale.value === 'de' ? (cat.name_de || '') : (cat.name_en || '')
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString(locale.value === 'de' ? 'de-DE' : 'en-US')
}

function confirmDelete(entry) {
  entryToDelete.value = entry
  showConfirm.value = true
}

function doDelete() {
  emit('delete', entryToDelete.value.id)
  showConfirm.value = false
  entryToDelete.value = null
}
</script>

<style scoped>
.entry-list { position: relative; }

.loading, .empty {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
}

.entries { display: flex; flex-direction: column; gap: 1rem; }

.entry-card {
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  padding: 1rem;
}

.entry-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.entry-date { font-weight: 600; }
.entry-category {
  background: var(--bg-color);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
}

.entry-body { margin-bottom: 0.75rem; }
.entry-notes {
  margin: 0.75rem 0 0;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.entry-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.btn-icon {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-icon:hover { color: var(--primary-color); }
.btn-icon.btn-danger:hover { color: #ef4444; }

.confirm-dialog {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.confirm-content {
  background: var(--surface-color);
  padding: 1.5rem;
  border-radius: 0.75rem;
  max-width: 300px;
}

.confirm-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
</style>
