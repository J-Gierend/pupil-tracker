<template>
  <section class="settings-section">
    <h2 class="section-title">{{ t('settings.export') }} / {{ t('settings.import') }}</h2>

    <div class="export-buttons">
      <button class="btn btn-secondary" @click="handleExportJson">
        {{ t('settings.exportJson') }}
      </button>
      <button class="btn btn-secondary" @click="handleExportCsv">
        {{ t('settings.exportCsv') }}
      </button>
    </div>

    <div class="import-section">
      <label class="import-label">
        {{ t('settings.importJson') }}
        <input
          type="file"
          accept=".json"
          @change="handleImport"
          class="file-input"
        />
      </label>
    </div>

    <p v-if="message" :class="['message', messageType]">
      {{ message }}
    </p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { exportJson, exportCsv, importJson } from '../api'

const { t } = useI18n()

const message = ref('')
const messageType = ref('')

function showMessage(text, type = 'success') {
  message.value = text
  messageType.value = type
  setTimeout(() => { message.value = '' }, 3000)
}

async function handleExportJson() {
  try {
    const res = await exportJson()
    downloadFile(JSON.stringify(res.data, null, 2), 'export.json', 'application/json')
    showMessage('Exported successfully')
  } catch (e) {
    showMessage('Export failed', 'error')
  }
}

async function handleExportCsv() {
  try {
    const res = await exportCsv()
    downloadFile(res.data, 'export.csv', 'text/csv')
    showMessage('Exported successfully')
  } catch (e) {
    showMessage('Export failed', 'error')
  }
}

function downloadFile(content, filename, type) {
  const blob = new Blob([content], { type })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

async function handleImport(event) {
  const file = event.target.files[0]
  if (!file) return

  try {
    const text = await file.text()
    const data = JSON.parse(text)
    await importJson(data)
    showMessage('Imported successfully')
  } catch (e) {
    showMessage('Import failed', 'error')
  }

  event.target.value = ''
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

.export-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.import-section {
  margin-top: 1rem;
}

.import-label {
  display: block;
  padding: 1rem;
  background: var(--bg-color);
  border: 2px dashed var(--border-color);
  border-radius: 0.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.import-label:hover {
  border-color: var(--primary-color);
}

.file-input {
  display: none;
}

.message {
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  text-align: center;
}

.message.success {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.message.error {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

/* Mobile */
@media (max-width: 480px) {
  .export-buttons {
    flex-direction: column;
  }

  .export-buttons .btn {
    width: 100%;
  }

  .settings-section {
    padding: 1rem;
  }
}
</style>
