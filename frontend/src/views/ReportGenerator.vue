<template>
  <div class="report-generator">
    <h1 class="page-title">{{ t('reports.title') }}</h1>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>

    <template v-else>
      <!-- Selection Form -->
      <div class="selection-panel">
        <div class="form-row">
          <div class="form-group">
            <label>{{ t('reports.selectClass') }}</label>
            <select v-model="selectedClass" @change="selectedPupil = null">
              <option :value="null">-- {{ t('reports.selectClass') }} --</option>
              <option v-for="cls in classes" :key="cls.id" :value="cls.id">
                {{ cls.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>{{ t('reports.selectPupil') }}</label>
            <select v-model="selectedPupil" :disabled="!selectedClass">
              <option :value="null">-- {{ t('reports.selectPupil') }} --</option>
              <option v-for="p in filteredPupils" :key="p.id" :value="p.id">
                {{ p.first_name }} {{ p.last_name }}
              </option>
            </select>
          </div>
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
      </div>

      <!-- No Selection Message -->
      <div v-if="!selectedPupil" class="info-message">
        <p>{{ t('reports.noSelection') }}</p>
      </div>

      <!-- Main Report Content -->
      <template v-else>
        <div class="report-content">
          <!-- Pupil Header -->
          <div class="pupil-header">
            <div class="pupil-avatar">{{ getInitials(currentPupil) }}</div>
            <div class="pupil-details">
              <h2>{{ currentPupil?.first_name }} {{ currentPupil?.last_name }}</h2>
              <p>{{ filteredEntries.length }} {{ t('pupil.entries') }} |
                 {{ locale === 'de' ? 'Zeitraum' : 'Period' }}: {{ formatDate(startDate) }} - {{ formatDate(endDate) }}</p>
            </div>
          </div>

          <!-- Entries Section -->
          <div class="entries-section">
            <div class="section-header">
              <h3>{{ t('pupil.entries') }}</h3>
              <button class="btn btn-sm btn-primary" @click="showAddEntry = true">
                + {{ t('pupil.addEntry') }}
              </button>
            </div>

            <div v-if="filteredEntries.length === 0" class="empty-entries">
              {{ t('pupil.noEntries') }}
            </div>

            <div v-else class="entries-list">
              <div v-for="entry in filteredEntries" :key="entry.id" class="entry-item">
                <div class="entry-meta">
                  <span class="entry-date">{{ formatDate(entry.date) }}</span>
                  <span class="entry-category">{{ getCategoryName(entry.category_id) }}</span>
                  <span v-if="entry.grade" class="entry-grade" :class="getGradeClass(entry.grade)">
                    {{ entry.grade }}
                  </span>
                </div>
                <p class="entry-notes">{{ entry.notes || '-' }}</p>
              </div>
            </div>
          </div>

          <!-- AI Instructions Section -->
          <div class="ai-section">
            <h3>{{ locale === 'de' ? 'KI-Anweisungen' : 'AI Instructions' }}</h3>
            <p class="ai-hint">
              {{ locale === 'de'
                ? 'Geben Sie hier spezielle Anweisungen fuer die Berichtserstellung ein (z.B. Fokus auf bestimmte Bereiche, Tonfall, etc.)'
                : 'Enter special instructions for report generation (e.g., focus areas, tone, etc.)' }}
            </p>
            <textarea
              v-model="aiInstructions"
              :placeholder="locale === 'de' ? 'z.B. Bitte betone die positiven Entwicklungen im Sozialverhalten...' : 'e.g., Please emphasize positive developments in social behavior...'"
              rows="3"
            ></textarea>
          </div>

          <!-- Mock AI Generated Report -->
          <div class="generated-report">
            <div class="report-header">
              <h3>{{ locale === 'de' ? 'Generierter Bericht' : 'Generated Report' }}</h3>
              <button class="btn btn-sm btn-secondary" @click="generateMockReport">
                {{ locale === 'de' ? 'Bericht generieren' : 'Generate Report' }}
              </button>
            </div>

            <div v-if="mockReport" class="report-text">
              <p>{{ mockReport }}</p>
            </div>
            <div v-else class="report-placeholder">
              {{ locale === 'de'
                ? 'Klicken Sie auf "Bericht generieren" um einen Beispielbericht zu erstellen.'
                : 'Click "Generate Report" to create a sample report.' }}
            </div>

            <div class="demo-notice">
              <strong>{{ locale === 'de' ? 'Hinweis' : 'Notice' }}:</strong>
              {{ locale === 'de'
                ? 'Dies ist ein Demo-Bericht. In der Vollversion wird dieser Text von einer KI basierend auf den Eintraegen generiert.'
                : 'This is a demo report. In the full version, this text will be generated by AI based on the entries.' }}
            </div>
          </div>

          <!-- Export Buttons -->
          <div class="export-section">
            <h3>{{ locale === 'de' ? 'Bericht exportieren' : 'Export Report' }}</h3>
            <div class="export-buttons">
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
        </div>
      </template>

      <!-- Add Entry Modal -->
      <div v-if="showAddEntry" class="modal-overlay" @click.self="showAddEntry = false">
        <div class="modal">
          <h3>{{ t('pupil.addEntry') }}</h3>
          <form @submit.prevent="addNewEntry">
            <div class="form-group">
              <label>{{ t('entry.date') }}</label>
              <input type="date" v-model="newEntry.date" required />
            </div>
            <div class="form-group">
              <label>{{ t('entry.category') }}</label>
              <select v-model="newEntry.category_id" required>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                  {{ getCategoryName(cat.id) }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>{{ t('entry.grade') }}</label>
              <div class="grade-buttons">
                <button
                  v-for="g in 6"
                  :key="g"
                  type="button"
                  :class="['grade-btn', { selected: newEntry.grade === g }]"
                  @click="newEntry.grade = g"
                >{{ g }}</button>
              </div>
            </div>
            <div class="form-group">
              <label>{{ t('entry.notes') }}</label>
              <textarea v-model="newEntry.notes" rows="3"></textarea>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="showAddEntry = false">
                {{ t('common.cancel') }}
              </button>
              <button type="submit" class="btn btn-primary">
                {{ t('common.save') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { getClasses, getPupils, getEntries, getCategories, createEntry } from '../api'
import { generatePDF, generateWord } from '../services/reportGenerator'

const { t, locale } = useI18n()

const loading = ref(true)
const generating = ref(false)
const errorMessage = ref('')
const classes = ref([])
const pupils = ref([])
const categories = ref([])
const allEntries = ref([])

const selectedClass = ref(null)
const selectedPupil = ref(null)
const startDate = ref(getDefaultStartDate())
const endDate = ref(new Date().toISOString().split('T')[0])
const aiInstructions = ref('')
const mockReport = ref('')
const showAddEntry = ref(false)

const newEntry = reactive({
  date: new Date().toISOString().split('T')[0],
  category_id: null,
  grade: 3,
  notes: ''
})

function getDefaultStartDate() {
  const d = new Date()
  d.setMonth(d.getMonth() - 6)
  return d.toISOString().split('T')[0]
}

const filteredPupils = computed(() => {
  if (!selectedClass.value) return []
  return pupils.value.filter(p => p.class_id === selectedClass.value)
})

const filteredEntries = computed(() => {
  if (!selectedPupil.value) return []
  return allEntries.value
    .filter(e => e.pupil_id === selectedPupil.value)
    .filter(e => {
      const date = new Date(e.date)
      const start = new Date(startDate.value)
      const end = new Date(endDate.value)
      return date >= start && date <= end
    })
    .sort((a, b) => new Date(b.date) - new Date(a.date))
})

const currentPupil = computed(() => {
  return pupils.value.find(p => p.id === selectedPupil.value)
})

function getInitials(pupil) {
  if (!pupil) return ''
  return (pupil.first_name?.[0] || '') + (pupil.last_name?.[0] || '')
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString(locale.value === 'de' ? 'de-DE' : 'en-US')
}

function getCategoryName(id) {
  const cat = categories.value.find(c => c.id === id)
  if (!cat) return ''
  return locale.value === 'de' ? (cat.name_de || '') : (cat.name_en || '')
}

function getGradeClass(grade) {
  if (grade <= 2) return 'grade-good'
  if (grade <= 3) return 'grade-ok'
  if (grade <= 4) return 'grade-warn'
  return 'grade-poor'
}

function generateMockReport() {
  const pupil = currentPupil.value
  if (!pupil) return

  const entries = filteredEntries.value
  const name = pupil.first_name

  // Generate mock report based on entries
  const gradeEntries = entries.filter(e => e.grade)
  const avgGrade = gradeEntries.length > 0
    ? (gradeEntries.reduce((sum, e) => sum + e.grade, 0) / gradeEntries.length).toFixed(1)
    : null

  if (locale.value === 'de') {
    mockReport.value = `Entwicklungsbericht fuer ${pupil.first_name} ${pupil.last_name}

Im Berichtszeitraum wurden ${entries.length} Beobachtungen dokumentiert.${avgGrade ? ` Der Notendurchschnitt liegt bei ${avgGrade}.` : ''}

${name} zeigt insgesamt eine positive Entwicklung. Die Arbeitsbereitschaft ist gut und die Beteiligung am Unterricht hat sich verbessert. Im sozialen Bereich faellt auf, dass ${name} gut mit Klassenkameraden zusammenarbeitet und hilfsbereit ist.

Die motorischen Faehigkeiten entsprechen dem Alter. Bei kreativen Aufgaben zeigt ${name} Phantasie und Eigeninitiative. Die sprachliche Entwicklung verlaeuft altersgemaess.

Empfehlung: ${name} sollte weiterhin ermutigt werden, sich aktiv am Unterricht zu beteiligen. Besondere Foerderung im Bereich der Selbststaendigkeit waere wuenschenswert.`
  } else {
    mockReport.value = `Development Report for ${pupil.first_name} ${pupil.last_name}

During the reporting period, ${entries.length} observations were documented.${avgGrade ? ` The average grade is ${avgGrade}.` : ''}

${name} shows overall positive development. Work ethic is good and participation in class has improved. In the social area, ${name} cooperates well with classmates and is helpful.

Motor skills are age-appropriate. ${name} shows imagination and initiative in creative tasks. Language development is progressing as expected.

Recommendation: ${name} should continue to be encouraged to actively participate in class. Special support in the area of independence would be desirable.`
  }
}

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

async function addNewEntry() {
  if (!selectedPupil.value) return
  await createEntry({
    pupil_id: selectedPupil.value,
    ...newEntry
  })
  showAddEntry.value = false
  // Reset form
  newEntry.date = new Date().toISOString().split('T')[0]
  newEntry.category_id = categories.value[0]?.id || null
  newEntry.grade = 3
  newEntry.notes = ''
  // Reload entries
  await loadData()
}

async function loadData() {
  loading.value = true
  const [classRes, pupilRes, catRes, entryRes] = await Promise.all([
    getClasses(), getPupils(), getCategories(), getEntries()
  ])
  classes.value = classRes.data
  pupils.value = pupilRes.data
  categories.value = catRes.data
  allEntries.value = entryRes.data
  if (categories.value.length > 0) {
    newEntry.category_id = categories.value[0].id
  }
  loading.value = false
}

onMounted(loadData)
</script>

<style scoped>
.page-title { margin: 0 0 1.5rem; font-size: 1.75rem; }

.selection-panel {
  background: var(--surface-color);
  padding: 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid var(--border-color);
  margin-bottom: 1.5rem;
}

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem; }
.form-row:last-child { margin-bottom: 0; }

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  color: var(--text-color);
  font-size: 1rem;
}

.info-message {
  padding: 3rem;
  background: var(--surface-color);
  border: 2px dashed var(--border-color);
  border-radius: 0.75rem;
  text-align: center;
  color: var(--text-secondary);
}

.report-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.pupil-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: linear-gradient(135deg, var(--primary-color), #14b8a6);
  padding: 1.5rem;
  border-radius: 0.75rem;
  color: white;
}

.pupil-avatar {
  width: 4rem;
  height: 4rem;
  background: rgba(255,255,255,0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.5rem;
}

.pupil-details h2 { margin: 0; font-size: 1.5rem; }
.pupil-details p { margin: 0.25rem 0 0; opacity: 0.9; font-size: 0.875rem; }

.entries-section,
.ai-section,
.generated-report,
.export-section {
  background: var(--surface-color);
  padding: 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid var(--border-color);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h3 { margin: 0; font-size: 1.125rem; }

.entries-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 400px;
  overflow-y: auto;
}

.entry-item {
  background: var(--bg-color);
  padding: 1rem;
  border-radius: 0.5rem;
}

.entry-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.entry-date { font-weight: 600; color: var(--primary-color); font-size: 0.875rem; }
.entry-category {
  background: var(--surface-color);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
}

.entry-grade {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.75rem;
}

.grade-good { background: #dcfce7; color: #166534; }
.grade-ok { background: #fef3c7; color: #92400e; }
.grade-warn { background: #fed7aa; color: #9a3412; }
.grade-poor { background: #fecaca; color: #991b1b; }

.entry-notes { margin: 0; font-size: 0.875rem; color: var(--text-secondary); }

.empty-entries {
  padding: 2rem;
  text-align: center;
  color: var(--text-secondary);
  font-style: italic;
}

.ai-section h3 { margin: 0 0 0.5rem; font-size: 1.125rem; }
.ai-hint { margin: 0 0 0.75rem; font-size: 0.875rem; color: var(--text-secondary); }

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.report-header h3 { margin: 0; font-size: 1.125rem; }

.report-text {
  background: var(--bg-color);
  padding: 1rem;
  border-radius: 0.5rem;
  white-space: pre-wrap;
  line-height: 1.6;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.report-placeholder {
  background: var(--bg-color);
  padding: 2rem;
  border-radius: 0.5rem;
  text-align: center;
  color: var(--text-secondary);
  font-style: italic;
  margin-bottom: 1rem;
}

.demo-notice {
  background: #fef3c7;
  color: #92400e;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.export-section h3 { margin: 0 0 1rem; font-size: 1.125rem; }

.export-buttons { display: flex; gap: 1rem; }

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

.loading { text-align: center; padding: 2rem; color: var(--text-secondary); }

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: var(--surface-color);
  padding: 1.5rem;
  border-radius: 0.75rem;
  width: 100%;
  max-width: 450px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal h3 { margin: 0 0 1.5rem; }

.grade-buttons { display: flex; gap: 0.5rem; }

.grade-btn {
  width: 2.5rem;
  height: 2.5rem;
  border: 2px solid var(--border-color);
  background: var(--bg-color);
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.grade-btn.selected {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.form-actions { display: flex; gap: 1rem; margin-top: 1.5rem; }

.btn-sm { padding: 0.5rem 1rem; font-size: 0.875rem; }
</style>
