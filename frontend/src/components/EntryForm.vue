<template>
  <form class="entry-form" @submit.prevent="handleSubmit">
    <h3 class="form-title">
      {{ editing ? t('entry.edit') : t('pupil.addEntry') }}
    </h3>

    <div class="form-group">
      <label>{{ t('entry.date') }}</label>
      <input type="date" v-model="form.date" required />
    </div>

    <div class="form-group">
      <label>{{ t('entry.category') }}</label>
      <select v-model="form.category_id" required>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
          {{ cat.name }}
        </option>
      </select>
    </div>

    <div class="form-group">
      <label>{{ t('entry.grade') }}</label>
      <div class="grade-selector">
        <button
          v-for="g in 6"
          :key="g"
          type="button"
          :class="['grade-btn', { selected: form.grade === g }]"
          @click="form.grade = g"
        >
          {{ g }}
        </button>
      </div>
    </div>

    <div class="form-group">
      <label>{{ t('entry.notes') }}</label>
      <textarea v-model="form.notes" rows="3"></textarea>
    </div>

    <div class="form-actions">
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">
        {{ t('entry.cancel') }}
      </button>
      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ t('entry.save') }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { getCategories } from '../api'

const props = defineProps({
  pupilId: { type: Number, required: true },
  entry: { type: Object, default: null }
})

const emit = defineEmits(['save', 'cancel'])
const { t } = useI18n()

const loading = ref(false)
const categories = ref([])
const editing = ref(false)

const form = reactive({
  date: new Date().toISOString().split('T')[0],
  category_id: null,
  grade: 3,
  notes: ''
})

async function loadCategories() {
  const res = await getCategories()
  categories.value = res.data
  if (categories.value.length && !form.category_id) {
    form.category_id = categories.value[0].id
  }
}

function handleSubmit() {
  loading.value = true
  emit('save', { ...form, pupil_id: props.pupilId })
}

watch(() => props.entry, (val) => {
  if (val) {
    editing.value = true
    form.date = val.date
    form.category_id = val.category_id
    form.grade = val.grade
    form.notes = val.notes || ''
  }
}, { immediate: true })

onMounted(loadCategories)
</script>

<style scoped>
.entry-form {
  background: var(--surface-color);
  padding: 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid var(--border-color);
}

.form-title {
  margin: 0 0 1.5rem;
  font-size: 1.125rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-secondary);
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

.grade-selector {
  display: flex;
  gap: 0.5rem;
}

.grade-btn {
  width: 3rem;
  height: 3rem;
  border: 2px solid var(--border-color);
  background: var(--bg-color);
  color: var(--text-color);
  border-radius: 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.grade-btn:hover {
  border-color: var(--primary-color);
}

.grade-btn.selected {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}
</style>
