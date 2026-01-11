<template>
  <div class="dashboard">
    <h1 class="page-title">{{ t('dashboard.title') }}</h1>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>

    <div v-else-if="error" class="error">
      <p>{{ t('common.error') }}</p>
      <button class="btn btn-primary" @click="loadData">
        {{ t('common.retry') }}
      </button>
    </div>

    <template v-else>
      <div class="stats-grid">
        <div class="stat-card">
          <span class="stat-value">{{ classes.length }}</span>
          <span class="stat-label">{{ t('dashboard.classes') }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-value">{{ pupils.length }}</span>
          <span class="stat-label">{{ t('dashboard.totalPupils') }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-value">{{ entries.length }}</span>
          <span class="stat-label">{{ t('dashboard.totalEntries') }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-value">{{ weekEntries }}</span>
          <span class="stat-label">{{ t('dashboard.thisWeek') }}</span>
        </div>
      </div>

      <div class="dashboard-grid">
        <section class="section">
          <h2 class="section-title">{{ t('dashboard.classes') }}</h2>
          <div v-if="classes.length === 0" class="empty">
            {{ t('dashboard.noClasses') }}
          </div>
          <div v-else class="class-list">
            <router-link
              v-for="cls in classes"
              :key="cls.id"
              :to="`/class/${cls.id}`"
              class="class-card"
            >
              <span class="class-name">{{ cls.name }}</span>
              <span class="class-count">
                {{ getPupilCount(cls.id) }} {{ t('class.pupils') }}
              </span>
            </router-link>
          </div>
        </section>

        <section class="section">
          <h2 class="section-title">{{ t('dashboard.recentEntries') }}</h2>
          <div v-if="recentEntries.length === 0" class="empty">
            {{ t('dashboard.noEntries') }}
          </div>
          <div v-else class="recent-list">
            <RecentEntryCard
              v-for="entry in recentEntries"
              :key="entry.id"
              :entry="entry"
              :pupil="getPupilById(entry.pupil_id)"
            />
          </div>
        </section>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { getClasses, getPupils, getEntries } from '../api'
import RecentEntryCard from '../components/RecentEntryCard.vue'

const { t } = useI18n()

const loading = ref(true)
const error = ref(false)
const classes = ref([])
const pupils = ref([])
const entries = ref([])

const weekEntries = computed(() => {
  const weekAgo = new Date()
  weekAgo.setDate(weekAgo.getDate() - 7)
  return entries.value.filter(e => new Date(e.date) >= weekAgo).length
})

const recentEntries = computed(() => {
  return [...entries.value]
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, 5)
})

function getPupilCount(classId) {
  return pupils.value.filter(p => p.class_id === classId).length
}

function getPupilById(id) {
  return pupils.value.find(p => p.id === id)
}

async function loadData() {
  loading.value = true
  error.value = false
  try {
    const [classRes, pupilRes, entryRes] = await Promise.all([
      getClasses(), getPupils(), getEntries()
    ])
    classes.value = classRes.data
    pupils.value = pupilRes.data
    entries.value = entryRes.data
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.page-title { margin: 0 0 1.5rem; font-size: 1.75rem; }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: var(--surface-color);
  padding: 1.25rem;
  border-radius: 0.75rem;
  border: 1px solid var(--border-color);
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

@media (max-width: 900px) {
  .dashboard-grid { grid-template-columns: 1fr; }
}

@media (max-width: 480px) {
  .page-title { font-size: 1.5rem; }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-value {
    font-size: 1.5rem;
  }

  .stat-label {
    font-size: 0.75rem;
  }

  .class-card {
    padding: 0.875rem;
  }
}

.section { min-width: 0; }

.section-title {
  font-size: 1.25rem;
  margin: 0 0 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-color);
}

.class-list { display: flex; flex-direction: column; gap: 0.75rem; }

.class-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s;
}

.class-card:hover {
  border-color: var(--primary-color);
  transform: translateX(4px);
}

.class-name { font-weight: 600; }
.class-count { font-size: 0.875rem; color: var(--text-secondary); }

.recent-list { display: flex; flex-direction: column; gap: 0.75rem; }

.loading, .empty, .error {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
}
</style>
