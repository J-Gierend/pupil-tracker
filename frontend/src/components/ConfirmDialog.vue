<template>
  <div class="confirm-overlay" @click.self="$emit('cancel')">
    <div class="confirm-dialog">
      <p class="confirm-message">{{ message }}</p>
      <div class="confirm-actions">
        <button class="btn btn-secondary" @click="$emit('cancel')">
          {{ t('common.no') }}
        </button>
        <button class="btn btn-danger" @click="$emit('confirm')">
          {{ t('common.yes') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

defineProps({
  message: { type: String, required: true }
})

defineEmits(['confirm', 'cancel'])

const { t } = useI18n()
</script>

<style scoped>
.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.confirm-dialog {
  background: var(--surface-color);
  padding: 1.5rem;
  border-radius: 0.75rem;
  max-width: 300px;
  width: 90%;
}

.confirm-message {
  margin: 0 0 1rem;
  text-align: center;
}

.confirm-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}
</style>
