<template>
  <section class="settings-section">
    <h2 class="section-title">{{ t('settings.schoolYears') }}</h2>

    <div class="items-list">
      <div v-for="year in years" :key="year.id" class="item-row">
        <span>{{ year.name }}</span>
        <button class="btn-icon btn-danger" @click="confirmDelete(year)">
          [Del]
        </button>
      </div>
      <div v-if="years.length === 0" class="empty">
        No school years
      </div>
    </div>

    <form class="add-form" @submit.prevent="addYear">
      <input
        v-model="newName"
        :placeholder="t('settings.name')"
        required
      />
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
import { getSchoolYears, createSchoolYear, deleteSchoolYear } from '../api'
import ConfirmDialog from './ConfirmDialog.vue'

const { t } = useI18n()

const years = ref([])
const newName = ref('')
const showConfirm = ref(false)
const itemToDelete = ref(null)

async function loadYears() {
  const res = await getSchoolYears()
  years.value = res.data
}

async function addYear() {
  if (!newName.value.trim()) return
  await createSchoolYear({ name: newName.value })
  newName.value = ''
  await loadYears()
}

function confirmDelete(item) {
  itemToDelete.value = item
  showConfirm.value = true
}

async function doDelete() {
  await deleteSchoolYear(itemToDelete.value.id)
  showConfirm.value = false
  itemToDelete.value = null
  await loadYears()
}

onMounted(loadYears)
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
}

.add-form input {
  flex: 1;
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

  .add-form input {
    width: 100%;
  }

  .add-form .btn {
    width: 100%;
  }

  .settings-section {
    padding: 1rem;
  }
}
</style>
