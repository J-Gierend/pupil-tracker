<template>
  <div :class="['grade-display', gradeClass]">
    <span class="grade-number">{{ grade }}</span>
    <span class="grade-text">{{ t(`grades.${grade}`) }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  grade: { type: Number, required: true }
})

const { t } = useI18n()

const gradeClass = computed(() => {
  if (props.grade <= 2) return 'grade-good'
  if (props.grade <= 4) return 'grade-medium'
  return 'grade-poor'
})
</script>

<style scoped>
.grade-display {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
  font-weight: 500;
}

.grade-number {
  font-size: 1.125rem;
  font-weight: 700;
}

.grade-text {
  font-size: 0.875rem;
}

.grade-good {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.grade-medium {
  background: rgba(234, 179, 8, 0.2);
  color: #eab308;
}

.grade-poor {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}
</style>
