<template>
  <div class="pupil-view">
    <div class="page-header">
      <router-link v-if="pupil" :to="`/class/${pupil.class_id}`" class="back-link">
        [Back] {{ t('pupil.back') }}
      </router-link>
      <h1 class="page-title">
        {{ pupil?.first_name }} {{ pupil?.last_name }}
      </h1>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>

    <div v-else-if="error" class="error">
      <p>{{ t('common.error') }}</p>
      <button class="btn btn-primary" @click="loadData">
        {{ t('common.retry') }}
      </button>
    </div>

    <template v-else>
      <div class="pupil-content">
        <div class="entries-section">
          <div class="section-header">
            <h2>{{ t('pupil.entries') }}</h2>
            <button class="btn btn-primary" @click="showForm = true">
              {{ t('pupil.addEntry') }}
            </button>
          </div>

          <EntryList
            :entries="entries"
            :categories="categories"
            :loading="entriesLoading"
            @edit="editEntry"
            @delete="handleDelete"
          />
        </div>

        <div v-if="showForm" class="form-section">
          <EntryForm
            :pupil-id="Number(id)"
            :entry="editingEntry"
            @save="handleSave"
            @cancel="closeForm"
          />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import {
  getPupil, getEntriesForPupil, getCategories,
  createEntry, updateEntry, deleteEntry
} from '../api'
import EntryList from '../components/EntryList.vue'
import EntryForm from '../components/EntryForm.vue'

const props = defineProps({ id: { type: String, required: true } })
const { t } = useI18n()

const loading = ref(true)
const entriesLoading = ref(false)
const error = ref(false)
const pupil = ref(null)
const entries = ref([])
const categories = ref([])
const showForm = ref(false)
const editingEntry = ref(null)

function closeForm() {
  showForm.value = false
  editingEntry.value = null
}

function editEntry(entry) {
  editingEntry.value = entry
  showForm.value = true
}

async function handleSave(data) {
  if (editingEntry.value) {
    await updateEntry(editingEntry.value.id, data)
  } else {
    await createEntry(data)
  }
  closeForm()
  await loadEntries()
}

async function handleDelete(entryId) {
  await deleteEntry(entryId)
  await loadEntries()
}

async function loadEntries() {
  entriesLoading.value = true
  const res = await getEntriesForPupil(props.id)
  entries.value = res.data
  entriesLoading.value = false
}

async function loadData() {
  loading.value = true
  error.value = false
  try {
    const [pupilRes, catRes] = await Promise.all([
      getPupil(props.id), getCategories()
    ])
    pupil.value = pupilRes.data
    categories.value = catRes.data
    await loadEntries()
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.page-header { margin-bottom: 1.5rem; }

.back-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.875rem;
}

.back-link:hover { color: var(--primary-color); }

.page-title { margin: 0.5rem 0 0; font-size: 1.75rem; }

.pupil-content {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 2rem;
}

@media (max-width: 900px) {
  .pupil-content { grid-template-columns: 1fr; }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h2 { margin: 0; font-size: 1.25rem; }

.loading, .error {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
}

/* Mobile */
@media (max-width: 480px) {
  .page-title { font-size: 1.375rem; }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .section-header .btn {
    width: 100%;
  }
}
</style>
