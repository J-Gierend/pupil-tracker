<template>
  <div class="class-view">
    <div class="page-header">
      <router-link to="/" class="back-link">
        [Back] {{ t('class.back') }}
      </router-link>
      <h1 class="page-title">
        {{ t('class.title') }}: {{ classData?.name || '' }}
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
      <div class="actions">
        <button class="btn btn-primary" @click="showAddPupil = true">
          {{ t('class.addPupil') }}
        </button>
      </div>

      <div v-if="pupils.length === 0" class="empty">
        {{ t('class.noPupils') }}
      </div>

      <div v-else class="pupils-grid">
        <PupilCard
          v-for="pupil in pupils"
          :key="pupil.id"
          :pupil="pupil"
          :entry-count="getEntryCount(pupil.id)"
          :average-grade="getAverageGrade(pupil.id)"
          :recent-entries="getRecentEntries(pupil.id)"
        />
      </div>
    </template>

    <div v-if="showAddPupil" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h3>{{ t('class.addPupil') }}</h3>
        <form @submit.prevent="addPupil">
          <div class="form-group">
            <label>{{ t('pupil.firstName') }}</label>
            <input v-model="newPupil.first_name" required />
          </div>
          <div class="form-group">
            <label>{{ t('pupil.lastName') }}</label>
            <input v-model="newPupil.last_name" required />
          </div>
          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="closeModal">
              {{ t('common.cancel') }}
            </button>
            <button type="submit" class="btn btn-primary">
              {{ t('common.save') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { getClass, getPupils, getEntries, createPupil } from '../api'
import PupilCard from '../components/PupilCard.vue'

const props = defineProps({ id: { type: String, required: true } })
const { t } = useI18n()

const loading = ref(true)
const error = ref(false)
const classData = ref(null)
const pupils = ref([])
const entries = ref([])
const showAddPupil = ref(false)
const newPupil = reactive({ first_name: '', last_name: '' })

function getEntryCount(pupilId) {
  return entries.value.filter(e => e.pupil_id === pupilId).length
}

function getAverageGrade(pupilId) {
  const pupilEntries = entries.value.filter(e => e.pupil_id === pupilId && e.grade)
  if (pupilEntries.length === 0) return null
  const sum = pupilEntries.reduce((acc, e) => acc + e.grade, 0)
  return sum / pupilEntries.length
}

function getRecentEntries(pupilId) {
  return entries.value
    .filter(e => e.pupil_id === pupilId)
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, 2)
}

function closeModal() {
  showAddPupil.value = false
  newPupil.first_name = ''
  newPupil.last_name = ''
}

async function addPupil() {
  await createPupil({ ...newPupil, class_id: Number(props.id) })
  closeModal()
  await loadData()
}

async function loadData() {
  loading.value = true
  error.value = false
  try {
    const [classRes, pupilRes, entryRes] = await Promise.all([
      getClass(props.id), getPupils(), getEntries()
    ])
    classData.value = classRes.data
    pupils.value = pupilRes.data.filter(p => p.class_id === Number(props.id))
    entries.value = entryRes.data
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

.actions { margin-bottom: 1.5rem; }

.pupils-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr));
  gap: 1rem;
}

.loading, .empty, .error {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 1rem;
}

.modal {
  background: var(--surface-color);
  padding: 1.5rem;
  border-radius: 0.75rem;
  width: 100%;
  max-width: 400px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal h3 { margin: 0 0 1rem; }

.form-group { margin-bottom: 1rem; }

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  color: var(--text-color);
  font-size: 1rem;
}

.form-actions { display: flex; gap: 1rem; margin-top: 1.5rem; }

/* Mobile */
@media (max-width: 480px) {
  .page-title { font-size: 1.5rem; }

  .modal {
    padding: 1rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions .btn {
    width: 100%;
  }

  .actions .btn {
    width: 100%;
  }
}
</style>
