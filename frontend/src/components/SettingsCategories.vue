<template>
  <section class="settings-section">
    <h2 class="section-title">{{ t('settings.categories') }}</h2>

    <div class="items-list">
      <div v-for="cat in categories" :key="cat.id" class="item-row">
        <span>{{ getCategoryName(cat) }}</span>
        <button
          v-if="cat.is_custom"
          class="btn-icon btn-danger"
          @click="confirmDelete(cat)"
        >
          [Del]
        </button>
        <span v-else class="badge">{{ t('settings.builtIn') }}</span>
      </div>
      <div v-if="categories.length === 0" class="empty">
        {{ t('settings.noCategories') }}
      </div>
    </div>

    <form class="add-form" @submit.prevent="addCategory">
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
import { getCategories, createCategory, deleteCategory } from '../api'
import ConfirmDialog from './ConfirmDialog.vue'

const { t, locale } = useI18n()

function getCategoryName(cat) {
  return locale.value === 'de' ? (cat.name_de || '') : (cat.name_en || '')
}

const categories = ref([])
const newName = ref('')
const showConfirm = ref(false)
const itemToDelete = ref(null)

async function loadCategories() {
  const res = await getCategories()
  categories.value = res.data
}

async function addCategory() {
  if (!newName.value.trim()) return
  const name = newName.value.trim()
  await createCategory({ name_de: name, name_en: name, is_custom: true })
  newName.value = ''
  await loadCategories()
}

function confirmDelete(item) {
  itemToDelete.value = item
  showConfirm.value = true
}

async function doDelete() {
  await deleteCategory(itemToDelete.value.id)
  showConfirm.value = false
  itemToDelete.value = null
  await loadCategories()
}

onMounted(loadCategories)
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

.badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  background: var(--bg-color);
  border-radius: 0.25rem;
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
}

.btn-icon:hover { color: #ef4444; }
</style>
