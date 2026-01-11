<template>
  <section class="settings-section">
    <h2 class="section-title">{{ t('settings.classes') }}</h2>

    <div class="items-list">
      <div v-for="cls in classes" :key="cls.id" class="item-row">
        <span>{{ cls.name }}</span>
        <button class="btn-icon btn-danger" @click="confirmDelete(cls)">
          [Del]
        </button>
      </div>
      <div v-if="classes.length === 0" class="empty">
        No classes
      </div>
    </div>

    <form class="add-form" @submit.prevent="addClass">
      <input
        v-model="newName"
        :placeholder="t('settings.name')"
        required
      />
      <select v-model="selectedYear" required>
        <option :value="null" disabled>{{ t('settings.year') }}</option>
        <option v-for="year in years" :key="year.id" :value="year.id">
          {{ year.name }}
        </option>
      </select>
      <button type="submit" class="btn btn-primary btn-sm">
        {{ t('common.add') }}
      </button>
    </form>

    <ConfirmDialog
      v-if="showConfirm"
      :message="t('settings.confirmDelete')"
      @confirm="doDelete"
      @cancel="showConfirm = false"
    />
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { getClasses, createClass, deleteClass, getSchoolYears } from '../api'
import ConfirmDialog from './ConfirmDialog.vue'

const { t } = useI18n()

const classes = ref([])
const years = ref([])
const newName = ref('')
const selectedYear = ref(null)
const showConfirm = ref(false)
const itemToDelete = ref(null)

async function loadData() {
  const [classRes, yearRes] = await Promise.all([getClasses(), getSchoolYears()])
  classes.value = classRes.data
  years.value = yearRes.data
}

async function addClass() {
  if (!newName.value.trim() || !selectedYear.value) return
  await createClass({ name: newName.value, school_year_id: selectedYear.value })
  newName.value = ''
  selectedYear.value = null
  await loadData()
}

function confirmDelete(item) {
  itemToDelete.value = item
  showConfirm.value = true
}

async function doDelete() {
  await deleteClass(itemToDelete.value.id)
  showConfirm.value = false
  itemToDelete.value = null
  await loadData()
}

onMounted(loadData)
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

.items-list {
  margin-bottom: 1rem;
  max-height: 200px;
  overflow-y: auto;
}

.item-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--border-color);
}

.empty {
  padding: 1rem;
  text-align: center;
  color: var(--text-secondary);
}

.add-form {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.add-form input,
.add-form select {
  flex: 1;
  min-width: 100px;
  padding: 0.5rem 0.75rem;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 0.375rem;
  color: var(--text-color);
}

.btn-sm { padding: 0.5rem 1rem; }

.btn-icon {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  min-width: 44px;
  min-height: 44px;
}

.btn-icon:hover { color: #ef4444; }

/* Mobile */
@media (max-width: 480px) {
  .add-form {
    flex-direction: column;
  }

  .add-form input,
  .add-form select {
    width: 100%;
    min-width: auto;
  }

  .add-form .btn {
    width: 100%;
  }

  .settings-section {
    padding: 1rem;
  }
}
</style>
