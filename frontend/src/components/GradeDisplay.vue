<template>
  <div :class="['grade-display', `grade-${grade}`]">
    <span class="grade-badge">{{ grade }}</span>
    <span class="grade-text">{{ t(`grades.${grade}`) }}</span>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const props = defineProps({
  grade: { type: Number, required: true }
})

const { t } = useI18n()
</script>

<style scoped>
.grade-display {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.375rem 1rem 0.375rem 0.375rem;
  border-radius: 2rem;
  font-weight: 500;
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.grade-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  font-size: 1rem;
  font-weight: 700;
  border-radius: 50%;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

.grade-text {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-color);
}

/* Grade 1 - Excellent (Green) */
.grade-1 .grade-badge {
  background: linear-gradient(135deg, #10b981, #059669);
}
.grade-1 { border-color: #d1fae5; background: #f0fdf4; }

/* Grade 2 - Good (Light Green) */
.grade-2 .grade-badge {
  background: linear-gradient(135deg, #22c55e, #16a34a);
}
.grade-2 { border-color: #dcfce7; background: #f0fdf4; }

/* Grade 3 - Satisfactory (Yellow/Amber) */
.grade-3 .grade-badge {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}
.grade-3 { border-color: #fef3c7; background: #fffbeb; }

/* Grade 4 - Adequate (Orange) */
.grade-4 .grade-badge {
  background: linear-gradient(135deg, #f97316, #ea580c);
}
.grade-4 { border-color: #fed7aa; background: #fff7ed; }

/* Grade 5 - Poor (Red-Orange) */
.grade-5 .grade-badge {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}
.grade-5 { border-color: #fecaca; background: #fef2f2; }

/* Grade 6 - Insufficient (Red) */
.grade-6 .grade-badge {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
}
.grade-6 { border-color: #fecaca; background: #fef2f2; }
</style>
