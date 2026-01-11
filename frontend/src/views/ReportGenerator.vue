<template>
  <div class="report-generator">
    <h1 class="page-title">{{ t('reports.title') }}</h1>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>

    <template v-else>
      <div class="report-form">
        <div class="form-group">
          <label>{{ t('reports.selectClass') }}</label>
          <select v-model="selectedClass" @change="selectedPupil = null">
            <option :value="null">--</option>
            <option v-for="cls in classes" :key="cls.id" :value="cls.id">
              {{ cls.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>{{ t('reports.selectPupil') }}</label>
          <select v-model="selectedPupil" :disabled="!selectedClass">
            <option :value="null">--</option>
            <option v-for="p in filteredPupils" :key="p.id" :value="p.id">
              {{ p.first_name }} {{ p.last_name }}
            </option>
          </select>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>{{ t('reports.startDate') }}</label>
            <input type="date" v-model="startDate" />
          </div>
          <div class="form-group">
            <label>{{ t('reports.endDate') }}</label>
            <input type="date" v-model="endDate" />
          </div>
        </div>

        <div v-if="!selectedPupil" class="info-message">
          {{ t('reports.noSelection') }}
        </div>

        <div v-else class="report-actions">
          <button class="btn btn-primary" @click="handleGeneratePdf" :disabled="generating">
            {{ t('reports.generatePdf') }}
          </button>
          <button class="btn btn-secondary" @click="handleGenerateWord" :disabled="generating">
            {{ t('reports.generateWord') }}
          </button>
        </div>

        <div v-if="generating" class="generating">
          {{ t('reports.generating') }}
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </div>

      <div v-if="selectedPupil" class="preview-section">
        <h2>{{ t('pupil.entries') }}</h2>
        <EntryList
          :entries="filteredEntries"
          :categories="categories"
          :loading="entriesLoading"
        />
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { getClasses, getPupils, getEntriesForPupil, getCategories } from '../api'
import { generatePDF, generateWord } from '../services/reportGenerator'
import EntryList from '../components/EntryList.vue'

const { t, locale } = useI18n()

const loading = ref(true)
const entriesLoading = ref(false)
const generating = ref(false)
const errorMessage = ref('')
const classes = ref([])
const pupils = ref([])
const categories = ref([])
const entries = ref([])

const selectedClass = ref(null)
const selectedPupil = ref(null)
const startDate = ref(getDefaultStartDate())
const endDate = ref(new Date().toISOString().split('T')[0])

function getDefaultStartDate() {
  const d = new Date()
  d.setMonth(d.getMonth() - 3)
  return d.toISOString().split('T')[0]
}

const filteredPupils = computed(() => {
  if (!selectedClass.value) return []
  return pupils.value.filter(p => p.class_id === selectedClass.value)
})

const filteredEntries = computed(() => {
  return entries.value.filter(e => {
    const date = new Date(e.date)
    const start = new Date(startDate.value)
    const end = new Date(endDate.value)
    return date >= start && date <= end
  })
})

const currentPupil = computed(() => {
  return pupils.value.find(p => p.id === selectedPupil.value)
})

async function handleGeneratePdf() {
  if (!selectedPupil.value || !currentPupil.value) return
  generating.value = true
  errorMessage.value = ''
  try {
    generatePDF(
      currentPupil.value,
      filteredEntries.value,
      categories.value,
      startDate.value,
      endDate.value,
      locale.value
    )
  } catch (e) {
    errorMessage.value = 'Failed to generate PDF: ' + e.message
  } finally {
    generating.value = false
  }
}

async function handleGenerateWord() {
  if (!selectedPupil.value || !currentPupil.value) return
  generating.value = true
  errorMessage.value = ''
  try {
    await generateWord(
      currentPupil.value,
      filteredEntries.value,
      categories.value,
      startDate.value,
      endDate.value,
      locale.value
    )
  } catch (e) {
    errorMessage.value = 'Failed to generate Word document: ' + e.message
  } finally {
    generating.value = false
  }
}

async function loadEntries() {
  if (!selectedPupil.value) {
    entries.value = []
    return
  }
  entriesLoading.value = true
  const res = await getEntriesForPupil(selectedPupil.value)
  entries.value = res.data
  entriesLoading.value = false
}

watch(selectedPupil, loadEntries)

async function loadData() {
  loading.value = true
  const [classRes, pupilRes, catRes] = await Promise.all([
    getClasses(), getPupils(), getCategories()
  ])
  classes.value = classRes.data
  pupils.value = pupilRes.data
  categories.value = catRes.data
  loading.value = false
}

onMounted(loadData)
</script>

<style scoped>
.page-title { margin: 0 0 1.5rem; font-size: 1.75rem; }

.report-form {
  background: var(--surface-color);
  padding: 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid var(--border-color);
  max-width: 500px;
  margin-bottom: 2rem;
}

.form-group { margin-bottom: 1rem; }

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  color: var(--text-color);
  font-size: 1rem;
}

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

.info-message {
  padding: 1rem;
  background: var(--bg-color);
  border-radius: 0.5rem;
  color: var(--text-secondary);
  text-align: center;
}

.report-actions { display: flex; gap: 1rem; margin-top: 1rem; }

.generating {
  margin-top: 1rem;
  color: var(--primary-color);
  text-align: center;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border-radius: 0.5rem;
  text-align: center;
}

.preview-section { margin-top: 2rem; }
.preview-section h2 { font-size: 1.25rem; margin-bottom: 1rem; }

.loading { text-align: center; padding: 2rem; color: var(--text-secondary); }
</style>
